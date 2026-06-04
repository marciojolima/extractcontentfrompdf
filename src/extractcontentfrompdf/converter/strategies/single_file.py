"""Estrategia para converter um unico arquivo PDF."""

from __future__ import annotations

from pathlib import Path

from extractcontentfrompdf.converter.processor import PdfDocumentProcessor
from extractcontentfrompdf.converter.requests import SingleFileConversionRequest
from extractcontentfrompdf.file_repository import MarkdownFileRepository


class SingleFileConversionStrategy:
    """Processa e persiste o Markdown de um unico PDF."""

    def __init__(
        self,
        document_processor: PdfDocumentProcessor,
        repository: MarkdownFileRepository,
    ) -> None:
        self._document_processor = document_processor
        self._repository = repository

    def execute(self, request: SingleFileConversionRequest) -> Path:
        """Executa a conversao individual a partir da requisicao."""
        self._repository.ensure_output_directory(request.output_dir)
        markdown_document = self._document_processor.process(
            pdf_path=request.pdf_path,
            start_page=request.start_page,
            end_page=request.end_page,
            check_security=request.check_security,
        )
        return self._repository.save(request.output_dir, markdown_document)
