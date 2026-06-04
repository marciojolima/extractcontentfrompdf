"""Estrategia para converter varios PDFs em um unico Markdown."""

from __future__ import annotations

from pathlib import Path

from extractcontentfrompdf.converter.batch_document_builder import (
    BatchMarkdownDocumentBuilder,
)
from extractcontentfrompdf.converter.processor import PdfDocumentProcessor
from extractcontentfrompdf.converter.requests import BatchConversionRequest
from extractcontentfrompdf.file_repository import MarkdownFileRepository


class BatchConversionStrategy:
    """Processa varios PDFs e persiste um unico documento consolidado."""

    def __init__(
        self,
        document_processor: PdfDocumentProcessor,
        repository: MarkdownFileRepository,
        batch_document_builder: BatchMarkdownDocumentBuilder,
    ) -> None:
        self._document_processor = document_processor
        self._repository = repository
        self._batch_document_builder = batch_document_builder

    def execute(self, request: BatchConversionRequest) -> Path:
        """Executa a conversao em lote a partir da requisicao."""
        if not request.pdf_paths:
            raise ValueError("Nenhum arquivo PDF foi informado para o processamento em lote.")

        self._repository.ensure_output_directory(request.output_dir)
        markdown_documents = [
            self._document_processor.process(
                pdf_path=pdf_path,
                check_security=request.check_security,
            )
            for pdf_path in request.pdf_paths
        ]
        batch_document = self._batch_document_builder.build(
            request.bundle_name,
            markdown_documents,
        )
        return self._repository.save(request.output_dir, batch_document)
