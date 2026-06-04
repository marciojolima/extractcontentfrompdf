import logging
from pathlib import Path
from unittest.mock import Mock

from extractcontentfrompdf.converter import (
    HierarchicalMarkdownDocumentBuilder,
    PdfDocumentProcessor,
    PdfToMarkdownConverter,
)
from extractcontentfrompdf.converter.strategies import (
    BatchConversionStrategy,
    SingleFileConversionStrategy,
)
from extractcontentfrompdf.models import ExtractionResult, MarkdownDocument
from extractcontentfrompdf.security.models import PdfSecurityIssue, PdfSecurityReport


def _make_converter() -> tuple[
    PdfToMarkdownConverter,
    Mock,
    Mock,
    Mock,
    Mock,
    Mock,
    Mock,
]:
    extractor = Mock()
    source_validator = Mock()
    security_scanner = Mock()
    security_policy = Mock()
    markdown_builder = Mock()
    repository = Mock()
    document_processor = PdfDocumentProcessor(
        extractor=extractor,
        source_validator=source_validator,
        security_scanner=security_scanner,
        security_policy=security_policy,
        markdown_builder=markdown_builder,
    )
    converter = PdfToMarkdownConverter(
        document_processor=document_processor,
        single_file_strategy=SingleFileConversionStrategy(
            document_processor=document_processor,
            repository=repository,
        ),
        batch_strategy=BatchConversionStrategy(
            document_processor=document_processor,
            repository=repository,
            hierarchical_document_builder=HierarchicalMarkdownDocumentBuilder(),
        ),
    )
    return (
        converter,
        extractor,
        source_validator,
        security_scanner,
        security_policy,
        markdown_builder,
        repository,
    )


def _make_markdown_document(title: str, body: str) -> MarkdownDocument:
    return MarkdownDocument(
        title=title,
        body=body,
        content=f"# {title}\n\n{body}\n",
    )


def test_convert_orquestra_fluxo_entre_dependencias() -> None:
    (
        converter,
        extractor,
        source_validator,
        security_scanner,
        security_policy,
        markdown_builder,
        repository,
    ) = _make_converter()
    pdf_path = Path("entrada.pdf")
    output_dir = Path("saida")
    extraction_result = ExtractionResult(
        total_pages=5,
        processed_pages=2,
        content="conteudo",
    )
    markdown_document = _make_markdown_document("entrada", "**Paginas do PDF:** 5")
    security_report = PdfSecurityReport(issues=())
    repository.save.return_value = output_dir / "entrada.md"
    extractor.extract.return_value = extraction_result
    markdown_builder.build.return_value = markdown_document
    security_scanner.scan.return_value = security_report

    resultado = converter.convert(pdf_path, output_dir, start_page=2, end_page=3)

    document = source_validator.validate.call_args.args[0]
    assert document == extractor.extract.call_args.args[0]
    assert document == markdown_builder.build.call_args.args[0]
    assert document.path == pdf_path
    assert document.start_page == 2
    assert document.end_page == 3
    source_validator.validate.assert_called_once()
    repository.ensure_output_directory.assert_called_once_with(output_dir)
    security_scanner.scan.assert_called_once()
    security_policy.enforce.assert_called_once()
    extractor.extract.assert_called_once()
    markdown_builder.build.assert_called_once()
    repository.save.assert_called_once_with(output_dir, markdown_document)
    assert resultado == output_dir / "entrada.md"


def test_convert_ignora_triagem_quando_parametro_esta_desabilitado() -> None:
    (
        converter,
        extractor,
        source_validator,
        security_scanner,
        security_policy,
        markdown_builder,
        repository,
    ) = _make_converter()
    repository.save.return_value = Path("saida/entrada.md")
    extractor.extract.return_value = ExtractionResult(
        total_pages=1,
        processed_pages=1,
        content="conteudo",
    )
    markdown_builder.build.return_value = _make_markdown_document(
        "entrada",
        "**Paginas do PDF:** 1",
    )

    resultado = converter.convert(
        Path("entrada.pdf"),
        Path("saida"),
        check_security=False,
    )

    source_validator.validate.assert_called_once()
    security_scanner.scan.assert_not_called()
    security_policy.enforce.assert_not_called()
    assert resultado == Path("saida/entrada.md")


def test_convert_registra_log_quando_triagem_esta_limpa(caplog) -> None:
    (
        converter,
        extractor,
        _source_validator,
        security_scanner,
        _security_policy,
        markdown_builder,
        repository,
    ) = _make_converter()
    repository.save.return_value = Path("saida/entrada.md")
    extractor.extract.return_value = ExtractionResult(
        total_pages=1,
        processed_pages=1,
        content="conteudo",
    )
    markdown_builder.build.return_value = _make_markdown_document(
        "entrada",
        "**Paginas do PDF:** 1",
    )
    security_scanner.scan.return_value = PdfSecurityReport(issues=())

    with caplog.at_level(logging.INFO):
        converter.convert(Path("entrada.pdf"), Path("saida"))

    assert "Triagem de seguranca limpa para entrada.pdf" in caplog.text


def test_convert_registra_log_quando_triagem_encontra_risco(caplog) -> None:
    (
        converter,
        extractor,
        _source_validator,
        security_scanner,
        _security_policy,
        markdown_builder,
        repository,
    ) = _make_converter()
    repository.save.return_value = Path("saida/entrada.md")
    extractor.extract.return_value = ExtractionResult(
        total_pages=1,
        processed_pages=1,
        content="conteudo",
    )
    markdown_builder.build.return_value = _make_markdown_document(
        "entrada",
        "**Paginas do PDF:** 1",
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


def test_convert_document_gera_markdown_sem_persistir() -> None:
    (
        converter,
        extractor,
        source_validator,
        security_scanner,
        _security_policy,
        markdown_builder,
        repository,
    ) = _make_converter()
    extraction_result = ExtractionResult(
        total_pages=3,
        processed_pages=3,
        content="conteudo",
    )
    markdown_document = _make_markdown_document("entrada", "**Paginas do PDF:** 3")
    extractor.extract.return_value = extraction_result
    markdown_builder.build.return_value = markdown_document
    security_scanner.scan.return_value = PdfSecurityReport(issues=())

    resultado = converter.convert_document(Path("entrada.pdf"), check_security=True)

    source_validator.validate.assert_called_once()
    repository.save.assert_not_called()
    extractor.extract.assert_called_once()
    markdown_builder.build.assert_called_once()
    assert resultado == markdown_document


def test_convert_batch_ignora_subdiretorios_vazios(tmp_path: Path) -> None:
    (
        converter,
        extractor,
        source_validator,
        security_scanner,
        _security_policy,
        markdown_builder,
        repository,
    ) = _make_converter()
    repository.save.return_value = Path("saida/Fase01.md")
    extractor.extract.return_value = ExtractionResult(
        total_pages=1,
        processed_pages=1,
        content="conteudo A",
    )
    markdown_builder.build.return_value = _make_markdown_document(
        "aula1",
        "**Paginas do PDF:** 1\n**Paginas processadas:** 1\n\nconteudo A",
    )
    security_scanner.scan.return_value = PdfSecurityReport(issues=())

    root_dir = tmp_path / "Fase01"
    empty_child = root_dir / "vazio"
    root_dir.mkdir()
    empty_child.mkdir()
    (root_dir / "aula1.pdf").write_text("fake", encoding="utf-8")

    output_paths = converter.convert_batch(
        root_dirs=[root_dir],
        output_dir=Path("saida"),
    )

    assert output_paths == [Path("saida/Fase01.md")]
    assert source_validator.validate.call_count == 1
    assert repository.ensure_output_directory.call_count == 1
    assert repository.save.call_count == 1


def test_convert_batch_falha_quando_raiz_nao_tem_pdfs(tmp_path: Path) -> None:
    (
        converter,
        _extractor,
        _source_validator,
        _security_scanner,
        _security_policy,
        _markdown_builder,
        _repository,
    ) = _make_converter()
    root_dir = tmp_path / "Fase01"
    (root_dir / "subdir").mkdir(parents=True)

    try:
        converter.convert_batch(
            root_dirs=[root_dir],
            output_dir=Path("saida"),
        )
    except ValueError as error:
        assert str(error) == f"Nenhum arquivo PDF foi encontrado em: {root_dir}"
    else:
        raise AssertionError("Era esperado erro para raiz sem nenhum PDF.")
