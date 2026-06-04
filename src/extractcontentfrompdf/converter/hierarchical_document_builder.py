"""Construcao de documentos Markdown a partir de uma arvore de diretorios."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from extractcontentfrompdf.models import MarkdownDocument


@dataclass(frozen=True, slots=True)
class DirectoryMarkdownNode:
    """Representa um diretorio consolidado com seus PDFs e subdiretorios."""

    path: Path
    markdown_documents: tuple[MarkdownDocument, ...]
    child_nodes: tuple["DirectoryMarkdownNode", ...]


class HierarchicalMarkdownDocumentBuilder:
    """Transforma uma arvore de diretorios em um unico Markdown."""

    def build(self, root_node: DirectoryMarkdownNode) -> MarkdownDocument:
        """Monta o documento final preservando a hierarquia de diretorios."""
        content = self._build_directory_section(root_node, heading_level=1).strip() + "\n"
        return MarkdownDocument(
            title=root_node.path.name,
            body=content.strip(),
            content=content,
        )

    def _build_directory_section(
        self,
        node: DirectoryMarkdownNode,
        heading_level: int,
    ) -> str:
        """Monta recursivamente a secao de um diretorio."""
        sections = [f"{'#' * heading_level} {node.path.name}", ""]

        for markdown_document in node.markdown_documents:
            sections.extend(
                [
                    f"{'#' * (heading_level + 1)} {markdown_document.title}",
                    "",
                    markdown_document.body,
                    "",
                ]
            )

        for child_node in node.child_nodes:
            sections.append(self._build_directory_section(child_node, heading_level + 1))
            sections.append("")

        return "\n".join(section.rstrip() for section in sections).strip()
