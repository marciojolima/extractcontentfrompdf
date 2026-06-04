from pathlib import Path

from extractcontentfrompdf.converter.hierarchical_document_builder import (
    DirectoryMarkdownNode,
    HierarchicalMarkdownDocumentBuilder,
)
from extractcontentfrompdf.models import MarkdownDocument


def test_build_preserva_hierarquia_sem_duplicar_titulos() -> None:
    builder = HierarchicalMarkdownDocumentBuilder()
    root = DirectoryMarkdownNode(
        path=Path("Fase01"),
        markdown_documents=(
            MarkdownDocument(
                title="aula1",
                body="**Paginas do PDF:** 1\n**Paginas processadas:** 1\n\nConteudo",
                content="# aula1\n\n**Paginas do PDF:** 1\n**Paginas processadas:** 1\n\nConteudo\n",
            ),
        ),
        child_nodes=(
            DirectoryMarkdownNode(
                path=Path("ModuloA"),
                markdown_documents=(),
                child_nodes=(),
            ),
        ),
    )

    markdown = builder.build(root)

    assert markdown.title == "Fase01"
    assert markdown.content.startswith("# Fase01\n")
    assert markdown.content.count("# Fase01") == 1
    assert "## aula1" in markdown.content
    assert "# aula1\n\n# aula1" not in markdown.content
