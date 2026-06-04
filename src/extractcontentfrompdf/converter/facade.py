"""Fachada de compatibilidade para os fluxos de conversao."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from extractcontentfrompdf.converter.processor import PdfDocumentProcessor
from extractcontentfrompdf.converter.requests import (
    BatchConversionRequest,
    SingleFileConversionRequest,
)
from extractcontentfrompdf.converter.strategies.batch import BatchConversionStrategy
from extractcontentfrompdf.converter.strategies.single_file import (
    SingleFileConversionStrategy,
)
from extractcontentfrompdf.models import MarkdownDocument


class PdfToMarkdownConverter:
    """Fachada para conversao individual e em lote com estrategias."""

    def __init__(
        self,
        document_processor: PdfDocumentProcessor,
        single_file_strategy: SingleFileConversionStrategy,
        batch_strategy: BatchConversionStrategy,
    ) -> None:
        self._document_processor = document_processor
        self._single_file_strategy = single_file_strategy
        self._batch_strategy = batch_strategy

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
        return self._single_file_strategy.execute(request)

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
        root_dirs: Sequence[Path],
        output_dir: Path,
        check_security: bool = True,
    ) -> list[Path]:
        """Processa uma ou mais arvores e gera um Markdown por raiz informada."""
        request = BatchConversionRequest(
            root_dirs=tuple(root_dirs),
            output_dir=output_dir,
            check_security=check_security,
        )
        return self._batch_strategy.execute(request)
