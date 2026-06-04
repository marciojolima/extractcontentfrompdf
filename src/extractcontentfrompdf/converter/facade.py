"""Fachada de compatibilidade para os fluxos de conversao."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from extractcontentfrompdf.converter.processor import PdfDocumentProcessor
from extractcontentfrompdf.converter.requests import (
    BatchConversionRequest,
    SingleFileConversionRequest,
)
from extractcontentfrompdf.converter.service import PdfConversionService
from extractcontentfrompdf.converter.strategies.base import ConversionStrategy
from extractcontentfrompdf.models import MarkdownDocument


class PdfToMarkdownConverter:
    """Fachada para conversao individual e em lote com estrategias."""

    def __init__(
        self,
        document_processor: PdfDocumentProcessor,
        single_file_strategy: ConversionStrategy,
        batch_strategy: ConversionStrategy,
        service: PdfConversionService,
    ) -> None:
        self._document_processor = document_processor
        self._single_file_strategy = single_file_strategy
        self._batch_strategy = batch_strategy
        self._service = service

    def convert(
        self,
        pdf_path: Path,
        output_dir: Path,
        start_page: int | None = None,
        end_page: int | None = None,
        check_security: bool = True,
    ) -> Path:
        """Executa o fluxo completo de processamento para um unico PDF."""
        request = SingleFileConversionRequest(
            pdf_path=pdf_path,
            output_dir=output_dir,
            start_page=start_page,
            end_page=end_page,
            check_security=check_security,
        )
        return self._service.execute(self._single_file_strategy, request)

    def convert_document(
        self,
        pdf_path: Path,
        start_page: int | None = None,
        end_page: int | None = None,
        check_security: bool = True,
    ) -> MarkdownDocument:
        """Gera o Markdown de um unico PDF sem persistir o resultado."""
        return self._document_processor.process(
            pdf_path=pdf_path,
            start_page=start_page,
            end_page=end_page,
            check_security=check_security,
        )

    def convert_batch(
        self,
        pdf_paths: Sequence[Path],
        output_dir: Path,
        bundle_name: str,
        check_security: bool = True,
    ) -> Path:
        """Processa varios PDFs e consolida o resultado em um unico Markdown."""
        request = BatchConversionRequest(
            pdf_paths=tuple(pdf_paths),
            output_dir=output_dir,
            bundle_name=bundle_name,
            check_security=check_security,
        )
        return self._service.execute(self._batch_strategy, request)
