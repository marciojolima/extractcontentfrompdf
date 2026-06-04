"""Ponto de entrada da linha de comando."""

from __future__ import annotations

import logging
from pathlib import Path

from extractcontentfrompdf.converter import PdfToMarkdownConverter
from extractcontentfrompdf.file_repository import MarkdownFileRepository
from extractcontentfrompdf.markdown_builder import MarkdownDocumentBuilder
from extractcontentfrompdf.pdf_extractor import PdfTextExtractor
from extractcontentfrompdf.security.policy import PdfSecurityPolicy
from extractcontentfrompdf.security.scanner import PdfSecurityScanner
from extractcontentfrompdf.sanitizer import TextSanitizer

INPUT_PDF_PATH = Path(
    "data/in/Fase01/02 Fundamentos Python e ML/POSTECH - Aula 02 - Introdução a Python e Fundamentos da Programação.pdf"
)
OUTPUT_DIR = Path("data/out")


def configure_logging() -> None:
    """Configura o formato padrao de logs do script."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def build_converter() -> PdfToMarkdownConverter:
    """Monta as dependencias da aplicacao no ponto de composicao."""
    sanitizer = TextSanitizer()
    extractor = PdfTextExtractor(sanitizer=sanitizer)
    markdown_builder = MarkdownDocumentBuilder()
    repository = MarkdownFileRepository()
    security_scanner = PdfSecurityScanner()
    security_policy = PdfSecurityPolicy()
    return PdfToMarkdownConverter(
        extractor=extractor,
        markdown_builder=markdown_builder,
        repository=repository,
        security_scanner=security_scanner,
        security_policy=security_policy,
    )


def main() -> int:
    """Executa o fluxo principal da aplicacao."""
    configure_logging()
    converter = build_converter()

    try:
        output_path = converter.convert(INPUT_PDF_PATH, OUTPUT_DIR)
    except (FileNotFoundError, PermissionError, ValueError) as error:
        logging.error("Falha ao preparar o processamento: %s", error)
        return 1
    except Exception as error:  # pragma: no cover - protecao para PDFs inesperados
        logging.error("Falha inesperada ao processar o PDF: %s", error)
        return 1

    logging.info("Markdown gerado com sucesso em: %s", output_path)
    return 0
