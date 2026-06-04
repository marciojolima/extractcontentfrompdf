"""Orquestracao do fluxo de conversao de PDF para Markdown."""

from __future__ import annotations

from pathlib import Path

from extractcontentfrompdf.file_repository import MarkdownFileRepository
from extractcontentfrompdf.markdown_builder import MarkdownDocumentBuilder
from extractcontentfrompdf.models import PdfDocument
from extractcontentfrompdf.pdf_extractor import PdfTextExtractor
from extractcontentfrompdf.security.policy import PdfSecurityPolicy
from extractcontentfrompdf.security.scanner import PdfSecurityScanner


class PdfToMarkdownConverter:
    """Coordena validacao, extracao, transformacao e persistencia."""

    def __init__(
        self,
        extractor: PdfTextExtractor,
        markdown_builder: MarkdownDocumentBuilder,
        repository: MarkdownFileRepository,
        security_scanner: PdfSecurityScanner,
        security_policy: PdfSecurityPolicy,
    ) -> None:
        self._extractor = extractor
        self._markdown_builder = markdown_builder
        self._repository = repository
        self._security_scanner = security_scanner
        self._security_policy = security_policy

    def convert(self, pdf_path: Path, output_dir: Path) -> Path:
        """Executa o fluxo completo de processamento para um unico PDF."""
        document = PdfDocument(path=pdf_path)
        self._repository.validate_source(document)
        self._repository.ensure_output_directory(output_dir)
        security_report = self._security_scanner.scan(document)
        self._security_policy.enforce(document, security_report)

        extraction_result = self._extractor.extract(document)
        markdown_document = self._markdown_builder.build(document, extraction_result)
        return self._repository.save(output_dir, markdown_document)
