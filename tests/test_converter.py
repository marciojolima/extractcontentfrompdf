import logging
from pathlib import Path
from unittest.mock import Mock

from extractcontentfrompdf.converter import (
    HierarchicalMarkdownDocumentBuilder,
    PdfConversionService,
    PdfDocumentProcessor,
    PdfToMarkdownConverter,
)
from extractcontentfrompdf.converter.strategies import (
    HierarchicalBatchConversionStrategy,
    SingleFileConversionStrategy,
)
from extractcontentfrompdf.models import ExtractionResult, MarkdownDocument
from extractcontentfrompdf.security.models import PdfSecurityIssue, PdfSecurityReport


def test_convert_orquestra_fluxo_entre_dependencias() -> None:
    extractor = Mock()
    markdown_builder = Mock()
    repository = Mock()
    security_scanner = Mock()
    security_policy = Mock()
    document_processor = PdfDocumentProcessor(
        extractor=extractor,
        markdown_builder=markdown_builder,
        repository=repository,
        security_scanner=security_scanner,
        security_policy=security_policy,
    )
    converter = PdfToMarkdownConverter(
        document_processor=document_processor,
        single_file_strategy=SingleFileConversionStrategy(
            document_processor=document_processor,
            repository=repository,
        ),
        hierarchical_batch_strategy=HierarchicalBatchConversionStrategy(
            document_processor=document_processor,
            repository=repository,
            hierarchical_document_builder=HierarchicalMarkdownDocumentBuilder(),
        ),
        service=PdfConversionService(),
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
    document_processor = PdfDocumentProcessor(
        extractor=extractor,
        markdown_builder=markdown_builder,
        repository=repository,
        security_scanner=security_scanner,
        security_policy=security_policy,
    )
    converter = PdfToMarkdownConverter(
        document_processor=document_processor,
        single_file_strategy=SingleFileConversionStrategy(
            document_processor=document_processor,
            repository=repository,
        ),
        hierarchical_batch_strategy=HierarchicalBatchConversionStrategy(
            document_processor=document_processor,
            repository=repository,
            hierarchical_document_builder=HierarchicalMarkdownDocumentBuilder(),
        ),
        service=PdfConversionService(),
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
    document_processor = PdfDocumentProcessor(
        extractor=extractor,
        markdown_builder=markdown_builder,
        repository=repository,
        security_scanner=security_scanner,
        security_policy=security_policy,
    )
    converter = PdfToMarkdownConverter(
        document_processor=document_processor,
        single_file_strategy=SingleFileConversionStrategy(
            document_processor=document_processor,
            repository=repository,
        ),
        hierarchical_batch_strategy=HierarchicalBatchConversionStrategy(
            document_processor=document_processor,
            repository=repository,
            hierarchical_document_builder=HierarchicalMarkdownDocumentBuilder(),
        ),
        service=PdfConversionService(),
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
    document_processor = PdfDocumentProcessor(
        extractor=extractor,
        markdown_builder=markdown_builder,
        repository=repository,
        security_scanner=security_scanner,
        security_policy=security_policy,
    )
    converter = PdfToMarkdownConverter(
        document_processor=document_processor,
        single_file_strategy=SingleFileConversionStrategy(
            document_processor=document_processor,
            repository=repository,
        ),
        hierarchical_batch_strategy=HierarchicalBatchConversionStrategy(
            document_processor=document_processor,
            repository=repository,
            hierarchical_document_builder=HierarchicalMarkdownDocumentBuilder(),
        ),
        service=PdfConversionService(),
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


def test_convert_document_gera_markdown_sem_persistir() -> None:
    extractor = Mock()
    markdown_builder = Mock()
    repository = Mock()
    security_scanner = Mock()
    security_policy = Mock()
    document_processor = PdfDocumentProcessor(
        extractor=extractor,
        markdown_builder=markdown_builder,
        repository=repository,
        security_scanner=security_scanner,
        security_policy=security_policy,
    )
    converter = PdfToMarkdownConverter(
        document_processor=document_processor,
        single_file_strategy=SingleFileConversionStrategy(
            document_processor=document_processor,
            repository=repository,
        ),
        hierarchical_batch_strategy=HierarchicalBatchConversionStrategy(
            document_processor=document_processor,
            repository=repository,
            hierarchical_document_builder=HierarchicalMarkdownDocumentBuilder(),
        ),
        service=PdfConversionService(),
    )
    extraction_result = ExtractionResult(
        total_pages=3,
        processed_pages=3,
        content="conteudo",
    )
    markdown_document = MarkdownDocument(title="entrada", content="# entrada\n")
    extractor.extract.return_value = extraction_result
    markdown_builder.build.return_value = markdown_document
    security_scanner.scan.return_value = PdfSecurityReport(issues=())

    resultado = converter.convert_document(Path("entrada.pdf"), check_security=True)

    repository.validate_source.assert_called_once()
    repository.save.assert_not_called()
    extractor.extract.assert_called_once()
    markdown_builder.build.assert_called_once()
    assert resultado == markdown_document


def test_convert_batch_consolida_varios_pdfs_em_um_unico_arquivo() -> None:
    extractor = Mock()
    markdown_builder = Mock()
    repository = Mock()
    security_scanner = Mock()
    security_policy = Mock()
    document_processor = PdfDocumentProcessor(
        extractor=extractor,
        markdown_builder=markdown_builder,
        repository=repository,
        security_scanner=security_scanner,
        security_policy=security_policy,
    )
    converter = PdfToMarkdownConverter(
        document_processor=document_processor,
        single_file_strategy=SingleFileConversionStrategy(
            document_processor=document_processor,
            repository=repository,
        ),
        hierarchical_batch_strategy=HierarchicalBatchConversionStrategy(
            document_processor=document_processor,
            repository=repository,
            hierarchical_document_builder=HierarchicalMarkdownDocumentBuilder(),
        ),
        service=PdfConversionService(),
    )


def test_convert_hierarchical_gera_um_arquivo_por_raiz(tmp_path: Path) -> None:
    extractor = Mock()
    markdown_builder = Mock()
    repository = Mock()
    security_scanner = Mock()
    security_policy = Mock()
    document_processor = PdfDocumentProcessor(
        extractor=extractor,
        markdown_builder=markdown_builder,
        repository=repository,
        security_scanner=security_scanner,
        security_policy=security_policy,
    )
    converter = PdfToMarkdownConverter(
        document_processor=document_processor,
        single_file_strategy=SingleFileConversionStrategy(
            document_processor=document_processor,
            repository=repository,
        ),
        hierarchical_batch_strategy=HierarchicalBatchConversionStrategy(
            document_processor=document_processor,
            repository=repository,
            hierarchical_document_builder=HierarchicalMarkdownDocumentBuilder(),
        ),
        service=PdfConversionService(),
    )
    repository.save.side_effect = [Path("saida/Fase01.md"), Path("saida/Fase02.md")]
    extractor.extract.side_effect = [
        ExtractionResult(total_pages=1, processed_pages=1, content="conteudo A"),
        ExtractionResult(total_pages=1, processed_pages=1, content="conteudo B"),
    ]
    markdown_builder.build.side_effect = [
        MarkdownDocument(title="aula1", content="# aula1\n\nconteudo A\n"),
        MarkdownDocument(title="aula2", content="# aula2\n\nconteudo B\n"),
    ]
    security_scanner.scan.return_value = PdfSecurityReport(issues=())

    root_a = tmp_path / "Fase01"
    root_b = tmp_path / "Fase02"
    root_a.mkdir()
    root_b.mkdir()
    (root_a / "aula1.pdf").write_text("fake", encoding="utf-8")
    (root_b / "aula2.pdf").write_text("fake", encoding="utf-8")

    output_paths = converter.convert_hierarchical(
        root_dirs=[root_a, root_b],
        output_dir=Path("saida"),
    )

    assert output_paths == [Path("saida/Fase01.md"), Path("saida/Fase02.md")]
    assert repository.ensure_output_directory.call_count == 1
    assert repository.save.call_count == 2
