"""Orquestracao do fluxo de conversao de PDF para Markdown."""

from __future__ import annotations

from pathlib import Path

from extractcontentfrompdf.file_repository import MarkdownFileRepository
from extractcontentfrompdf.markdown_builder import MarkdownDocumentBuilder
from extractcontentfrompdf.models import PdfDocument
from extractcontentfrompdf.pdf_extractor import PdfTextExtractor


class PdfToMarkdownConverter:
    """Coordena validacao, extracao, transformacao e persistencia."""

    def __init__(
        self,
        extractor: PdfTextExtractor,
        markdown_builder: MarkdownDocumentBuilder,
        repository: MarkdownFileRepository,
    ) -> None:
        self._extractor = extractor
        self._markdown_builder = markdown_builder
        self._repository = repository

    def convert(self, pdf_path: Path, output_dir: Path) -> Path:
        """Executa o fluxo completo de processamento para um unico PDF."""
        document = PdfDocument(path=pdf_path)
        self._repository.validate_source(document)
        self._repository.ensure_output_directory(output_dir)

        extraction_result = self._extractor.extract(document)
        markdown_document = self._markdown_builder.build(document, extraction_result)
        return self._repository.save(output_dir, markdown_document)
