from pathlib import Path
from unittest.mock import Mock

from extractcontentfrompdf.converter import PdfToMarkdownConverter
from extractcontentfrompdf.models import ExtractionResult, MarkdownDocument


def test_convert_orquestra_fluxo_entre_dependencias() -> None:
    extractor = Mock()
    markdown_builder = Mock()
    repository = Mock()
    converter = PdfToMarkdownConverter(
        extractor=extractor,
        markdown_builder=markdown_builder,
        repository=repository,
    )
    pdf_path = Path("entrada.pdf")
    output_dir = Path("saida")
    extraction_result = ExtractionResult(page_count=2, content="conteudo")
    markdown_document = MarkdownDocument(title="entrada", content="# entrada\n")
    repository.save.return_value = output_dir / "entrada.md"
    extractor.extract.return_value = extraction_result
    markdown_builder.build.return_value = markdown_document

    resultado = converter.convert(pdf_path, output_dir)

    repository.validate_source.assert_called_once()
    repository.ensure_output_directory.assert_called_once_with(output_dir)
    extractor.extract.assert_called_once()
    markdown_builder.build.assert_called_once()
    repository.save.assert_called_once_with(output_dir, markdown_document)
    assert resultado == output_dir / "entrada.md"
