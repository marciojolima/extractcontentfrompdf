"""Estrategia para consolidacao em batch de uma ou mais arvores."""

from __future__ import annotations

from pathlib import Path

from extractcontentfrompdf.converter.hierarchical_document_builder import (
    DirectoryMarkdownNode,
    HierarchicalMarkdownDocumentBuilder,
)
from extractcontentfrompdf.converter.processor import PdfDocumentProcessor
from extractcontentfrompdf.converter.requests import BatchConversionRequest
from extractcontentfrompdf.file_repository import MarkdownFileRepository


class BatchConversionStrategy:
    """Processa diretorios raiz em batch preservando a hierarquia na saida."""

    def __init__(
        self,
        document_processor: PdfDocumentProcessor,
        repository: MarkdownFileRepository,
        hierarchical_document_builder: HierarchicalMarkdownDocumentBuilder,
    ) -> None:
        self._document_processor = document_processor
        self._repository = repository
        self._hierarchical_document_builder = hierarchical_document_builder

    def execute(self, request: BatchConversionRequest) -> list[Path]:
        """Executa a conversao em batch para cada raiz informada."""
        if not request.root_dirs:
            raise ValueError(
                "Nenhum diretorio raiz foi informado para o processamento em batch."
            )

        self._repository.ensure_output_directory(request.output_dir)
        output_paths: list[Path] = []

        for root_dir in request.root_dirs:
            root_node = self._build_directory_node(
                root_dir=root_dir,
                check_security=request.check_security,
            )
            if root_node is None:
                raise ValueError(f"Nenhum arquivo PDF foi encontrado em: {root_dir}")
            markdown_document = self._hierarchical_document_builder.build(root_node)
            output_paths.append(self._repository.save(request.output_dir, markdown_document))

        return output_paths

    def _build_directory_node(
        self,
        root_dir: Path,
        check_security: bool,
    ) -> DirectoryMarkdownNode | None:
        """Constroi a representacao consolidada de um diretorio quando houver conteudo."""
        if not root_dir.exists():
            raise FileNotFoundError(f"Diretorio raiz nao encontrado: {root_dir}")

        if not root_dir.is_dir():
            raise ValueError(f"O caminho informado nao e um diretorio: {root_dir}")

        markdown_documents = tuple(
            self._document_processor.process(
                pdf_path=pdf_path,
                check_security=check_security,
            )
            for pdf_path in self._list_pdf_files(root_dir)
        )
        child_nodes = tuple(
            child_node
            for child_dir in self._list_child_directories(root_dir)
            if (child_node := self._build_directory_node(child_dir, check_security))
            is not None
        )

        if not markdown_documents and not child_nodes:
            return None

        return DirectoryMarkdownNode(
            path=root_dir,
            markdown_documents=markdown_documents,
            child_nodes=child_nodes,
        )

    def _list_pdf_files(self, root_dir: Path) -> list[Path]:
        """Lista apenas os PDFs do diretorio atual em ordem deterministica."""
        return sorted(
            path
            for path in root_dir.iterdir()
            if path.is_file() and path.suffix.lower() == ".pdf"
        )

    def _list_child_directories(self, root_dir: Path) -> list[Path]:
        """Lista apenas os subdiretorios imediatos em ordem deterministica."""
        return sorted(path for path in root_dir.iterdir() if path.is_dir())
