"""Ponto de entrada da linha de comando."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Sequence

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


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Le os argumentos da CLI para processamento de um unico PDF."""
    parser = argparse.ArgumentParser(
        prog="extract-pdf",
        description="Extrai texto de um arquivo PDF e salva o resultado em Markdown.",
    )
    parser.add_argument(
        "pdf_path",
        nargs="?",
        type=Path,
        default=INPUT_PDF_PATH,
        help="Caminho do arquivo PDF de entrada.",
    )
    parser.add_argument(
        "start_page",
        nargs="?",
        type=int,
        default=None,
        help="Pagina inicial para extracao.",
    )
    parser.add_argument(
        "end_page",
        nargs="?",
        type=int,
        default=None,
        help="Pagina final para extracao.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help="Diretorio onde o arquivo Markdown sera salvo.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Executa o fluxo principal da aplicacao."""
    configure_logging()
    args = parse_args(argv)
    converter = build_converter()

    try:
        output_path = converter.convert(
            args.pdf_path,
            args.output_dir,
            start_page=args.start_page,
            end_page=args.end_page,
        )
    except (FileNotFoundError, PermissionError, ValueError) as error:
        logging.error("Falha ao preparar o processamento: %s", error)
        return 1
    except Exception as error:  # pragma: no cover - protecao para PDFs inesperados
        logging.error("Falha inesperada ao processar o PDF: %s", error)
        return 1

    logging.info("Markdown gerado com sucesso em: %s", output_path)
    return 0
