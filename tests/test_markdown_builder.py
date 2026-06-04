from pathlib import Path

from extractcontentfrompdf.markdown_builder import MarkdownDocumentBuilder
from extractcontentfrompdf.models import ExtractionResult, PdfDocument


def test_build_gera_markdown_com_conteudo_extraido() -> None:
    builder = MarkdownDocumentBuilder()
    document = PdfDocument(path=Path("apostila.pdf"))
    extraction_result = ExtractionResult(
        total_pages=5,
        processed_pages=3,
        content="## Pagina 1\n\nTexto",
    )

    markdown = builder.build(document, extraction_result)

    assert markdown.title == "apostila"
    assert markdown.body == "**Paginas do PDF:** 5\n**Paginas processadas:** 3\n\n## Pagina 1\n\nTexto"
    assert (
        markdown.content
        == "# apostila\n\n**Paginas do PDF:** 5\n**Paginas processadas:** 3\n\n## Pagina 1\n\nTexto\n"
    )


def test_build_gera_mensagem_padrao_quando_nao_ha_conteudo() -> None:
    builder = MarkdownDocumentBuilder()
    document = PdfDocument(path=Path("vazio.pdf"))
    extraction_result = ExtractionResult(total_pages=0, processed_pages=0, content="")

    markdown = builder.build(document, extraction_result)

    assert MarkdownDocumentBuilder.EMPTY_CONTENT_MESSAGE in markdown.content
