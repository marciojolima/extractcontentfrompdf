import logging
from pathlib import Path
from unittest.mock import Mock

from extractcontentfrompdf.converter import PdfToMarkdownConverter
from extractcontentfrompdf.models import ExtractionResult, MarkdownDocument
from extractcontentfrompdf.security.models import PdfSecurityIssue, PdfSecurityReport


def test_convert_orquestra_fluxo_entre_dependencias() -> None:
    extractor = Mock()
    markdown_builder = Mock()
    repository = Mock()
    security_scanner = Mock()
    security_policy = Mock()
    converter = PdfToMarkdownConverter(
        extractor=extractor,
        markdown_builder=markdown_builder,
        repository=repository,
        security_scanner=security_scanner,
        security_policy=security_policy,
    )
    pdf_path = Path("entrada.pdf")
    output_dir = Path("saida")
    extraction_result = ExtractionResult(
        total_pages=5,
        processed_pages=2,
        content="conteudo",
    )
    markdown_document = MarkdownDocument(title="entrada", content="# entrada\n")
    security_report = PdfSecurityReport(issues=())
    repository.save.return_value = output_dir / "entrada.md"
    extractor.extract.return_value = extraction_result
    markdown_builder.build.return_value = markdown_document
    security_scanner.scan.return_value = security_report

    resultado = converter.convert(pdf_path, output_dir, start_page=2, end_page=3)

    document = repository.validate_source.call_args.args[0]
    assert document == extractor.extract.call_args.args[0]
    assert document == markdown_builder.build.call_args.args[0]
    assert document.path == pdf_path
    assert document.start_page == 2
    assert document.end_page == 3
    repository.validate_source.assert_called_once()
    repository.ensure_output_directory.assert_called_once_with(output_dir)
    security_scanner.scan.assert_called_once()
    security_policy.enforce.assert_called_once()
    extractor.extract.assert_called_once()
    markdown_builder.build.assert_called_once()
    repository.save.assert_called_once_with(output_dir, markdown_document)
    assert resultado == output_dir / "entrada.md"


def test_convert_ignora_triagem_quando_parametro_esta_desabilitado() -> None:
    extractor = Mock()
    markdown_builder = Mock()
    repository = Mock()
    security_scanner = Mock()
    security_policy = Mock()
    converter = PdfToMarkdownConverter(
        extractor=extractor,
        markdown_builder=markdown_builder,
        repository=repository,
        security_scanner=security_scanner,
        security_policy=security_policy,
    )
    repository.save.return_value = Path("saida/entrada.md")
    extractor.extract.return_value = ExtractionResult(
        total_pages=1,
        processed_pages=1,
        content="conteudo",
    )
    markdown_builder.build.return_value = MarkdownDocument(
        title="entrada",
        content="# entrada\n",
    )

    resultado = converter.convert(
        Path("entrada.pdf"),
        Path("saida"),
        check_security=False,
    )

    security_scanner.scan.assert_not_called()
    security_policy.enforce.assert_not_called()
    assert resultado == Path("saida/entrada.md")


def test_convert_registra_log_quando_triagem_esta_limpa(
    caplog,
) -> None:
    extractor = Mock()
    markdown_builder = Mock()
    repository = Mock()
    security_scanner = Mock()
    security_policy = Mock()
    converter = PdfToMarkdownConverter(
        extractor=extractor,
        markdown_builder=markdown_builder,
        repository=repository,
        security_scanner=security_scanner,
        security_policy=security_policy,
    )
    repository.save.return_value = Path("saida/entrada.md")
    extractor.extract.return_value = ExtractionResult(
        total_pages=1,
        processed_pages=1,
        content="conteudo",
    )
    markdown_builder.build.return_value = MarkdownDocument(
        title="entrada",
        content="# entrada\n",
    )
    security_scanner.scan.return_value = PdfSecurityReport(issues=())

    with caplog.at_level(logging.INFO):
        converter.convert(Path("entrada.pdf"), Path("saida"))

    assert "Triagem de seguranca limpa para entrada.pdf" in caplog.text


def test_convert_registra_log_quando_triagem_encontra_risco(
    caplog,
) -> None:
    extractor = Mock()
    markdown_builder = Mock()
    repository = Mock()
    security_scanner = Mock()
    security_policy = Mock()
    converter = PdfToMarkdownConverter(
        extractor=extractor,
        markdown_builder=markdown_builder,
        repository=repository,
        security_scanner=security_scanner,
        security_policy=security_policy,
    )
    repository.save.return_value = Path("saida/entrada.md")
    extractor.extract.return_value = ExtractionResult(
        total_pages=1,
        processed_pages=1,
        content="conteudo",
    )
    markdown_builder.build.return_value = MarkdownDocument(
        title="entrada",
        content="# entrada\n",
    )
    security_scanner.scan.return_value = PdfSecurityReport(
        issues=(
            PdfSecurityIssue(
                code="javascript",
                description="codigo JavaScript embutido",
                blocking=True,
            ),
        )
    )

    with caplog.at_level(logging.WARNING):
        converter.convert(Path("entrada.pdf"), Path("saida"))

    assert "Triagem de seguranca encontrou sinais bloqueantes em entrada.pdf" in caplog.text
    assert "Bloqueio preventivo por regra conservadora" in caplog.text
    assert "[javascript] codigo JavaScript embutido" in caplog.text
