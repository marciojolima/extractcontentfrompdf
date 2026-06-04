"""Ponto de entrada da linha de comando para conversao individual."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Sequence

from extractcontentfrompdf.entrypoints.bootstrap import (
    DEFAULT_OUTPUT_DIR,
    build_converter,
    configure_logging,
)
from extractcontentfrompdf.security.exceptions import PdfSecurityError


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Le os argumentos do entrypoint para processamento de um unico PDF."""
    parser = argparse.ArgumentParser(
        prog="extract-pdf",
        description="Extrai texto de um arquivo PDF e salva o resultado em Markdown.",
    )
    parser.add_argument(
        "pdf_path",
        type=Path,
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
        default=DEFAULT_OUTPUT_DIR,
        help="Diretorio onde o arquivo Markdown sera salvo.",
    )
    parser.add_argument(
        "--check-security",
        dest="check_security",
        action="store_true",
        default=True,
        help="Executa a triagem de seguranca do PDF antes da extracao.",
    )
    parser.add_argument(
        "--no-check-security",
        dest="check_security",
        action="store_false",
        help="Ignora a triagem de seguranca do PDF antes da extracao.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Executa o fluxo principal da aplicacao para um unico PDF."""
    configure_logging()
    args = parse_args(argv)
    converter = build_converter()

    try:
        output_path = converter.convert(
            args.pdf_path,
            args.output_dir,
            start_page=args.start_page,
            end_page=args.end_page,
            check_security=args.check_security,
        )
    except (FileNotFoundError, PermissionError, ValueError, PdfSecurityError) as error:
        logging.error("Falha ao preparar o processamento: %s", error)
        return 1

    logging.info("Markdown gerado com sucesso em: %s", output_path)
    return 0
