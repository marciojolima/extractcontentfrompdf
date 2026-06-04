"""Construcao do documento consolidado para processamentos em lote."""

from __future__ import annotations

from typing import Sequence

from extractcontentfrompdf.models import MarkdownDocument


class BatchMarkdownDocumentBuilder:
    """Consolida varios documentos Markdown em um unico arquivo."""

    def build(
        self,
        bundle_name: str,
        markdown_documents: Sequence[MarkdownDocument],
    ) -> MarkdownDocument:
        """Monta o documento final do lote."""
        sections = [
            f"# {bundle_name}",
            "",
            f"**Arquivos processados:** {len(markdown_documents)}",
        ]

        for markdown_document in markdown_documents:
            sections.extend(["", "---", "", markdown_document.content.rstrip()])

        content = "\n".join(sections).strip() + "\n"
        return MarkdownDocument(title=bundle_name, content=content)
