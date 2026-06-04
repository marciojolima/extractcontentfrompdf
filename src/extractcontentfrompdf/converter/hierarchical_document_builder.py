"""Construcao de documentos Markdown a partir de uma arvore de diretorios."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

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
        sections = [f"# {root_node.path.name}", ""]
        sections.extend(self._build_directory_sections(root_node, heading_level=2))
        content = "\n".join(section for section in sections if section is not None).strip() + "\n"
        return MarkdownDocument(title=root_node.path.name, content=content)

    def _build_directory_sections(
        self,
        node: DirectoryMarkdownNode,
        heading_level: int,
    ) -> list[str]:
        """Monta recursivamente as secoes de um diretorio."""
        sections = [f"{'#' * heading_level} {node.path.name}", ""]

        for markdown_document in node.markdown_documents:
            sections.extend(
                [
                    f"{'#' * (heading_level + 1)} {markdown_document.title}",
                    "",
                    markdown_document.content.rstrip(),
                    "",
                ]
            )

        for child_node in node.child_nodes:
            sections.extend(self._build_directory_sections(child_node, heading_level + 1))
            sections.append("")

        return sections
