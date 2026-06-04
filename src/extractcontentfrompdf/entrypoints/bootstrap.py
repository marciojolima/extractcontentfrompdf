"""Ponto de composicao da aplicacao."""

from __future__ import annotations

import logging
from pathlib import Path

from extractcontentfrompdf.converter import (
    HierarchicalMarkdownDocumentBuilder,
    PdfDocumentProcessor,
    PdfToMarkdownConverter,
)
from extractcontentfrompdf.converter.strategies import (
    HierarchicalBatchConversionStrategy,
    SingleFileConversionStrategy,
)
from extractcontentfrompdf.file_repository import MarkdownFileRepository
from extractcontentfrompdf.markdown_builder import MarkdownDocumentBuilder
from extractcontentfrompdf.pdf_extractor import PdfTextExtractor
from extractcontentfrompdf.security.policy import PdfSecurityPolicy
from extractcontentfrompdf.security.scanner import PdfSecurityScanner
from extractcontentfrompdf.sanitizer import TextSanitizer
from extractcontentfrompdf.validation import PdfSourceValidator

DEFAULT_OUTPUT_DIR = Path("data/out")


def configure_logging() -> None:
    """Configura o formato padrao de logs da aplicacao."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def build_converter() -> PdfToMarkdownConverter:
    """Monta as dependencias da aplicacao no ponto de composicao."""
    sanitizer = TextSanitizer()
    extractor = PdfTextExtractor(sanitizer=sanitizer)
    markdown_builder = MarkdownDocumentBuilder()
    repository = MarkdownFileRepository()
    source_validator = PdfSourceValidator()
    security_scanner = PdfSecurityScanner()
    security_policy = PdfSecurityPolicy()
    document_processor = PdfDocumentProcessor(
        extractor=extractor,
        source_validator=source_validator,
        security_scanner=security_scanner,
        security_policy=security_policy,
        markdown_builder=markdown_builder,
    )
    return PdfToMarkdownConverter(
        document_processor=document_processor,
        single_file_strategy=SingleFileConversionStrategy(
            document_processor=document_processor,
            repository=repository,
        ),
        hierarchical_batch_strategy=HierarchicalBatchConversionStrategy(
            document_processor=document_processor,
            repository=repository,
            hierarchical_document_builder=HierarchicalMarkdownDocumentBuilder(),
        ),
    )
