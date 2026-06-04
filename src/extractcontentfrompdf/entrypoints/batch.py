"""Ponto de entrada da linha de comando para processamento em lote."""

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
    """Le os argumentos da CLI para processamento hierarquico."""
    parser = argparse.ArgumentParser(
        prog="extract-pdf-hierarchical",
        description=(
            "Extrai texto de PDFs preservando a hierarquia de um ou mais "
            "diretorios raiz e gera um Markdown por raiz informada."
        ),
    )
    parser.add_argument(
        "root_dirs",
        nargs="+",
        type=Path,
        help="Um ou mais diretorios raiz para consolidacao hierarquica.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Diretorio onde os arquivos Markdown serao salvos.",
    )
    parser.add_argument(
        "--check-security",
        dest="check_security",
        action="store_true",
        default=True,
        help="Executa a triagem de seguranca dos PDFs antes da extracao.",
    )
    parser.add_argument(
        "--no-check-security",
        dest="check_security",
        action="store_false",
        help="Ignora a triagem de seguranca dos PDFs antes da extracao.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Executa o fluxo principal da aplicacao em modo batch."""
    configure_logging()
    args = parse_args(argv)
    converter = build_converter()

    try:
        output_paths = converter.convert_hierarchical(
            root_dirs=args.root_dirs,
            output_dir=args.output_dir,
            check_security=args.check_security,
        )
    except (FileNotFoundError, PermissionError, ValueError, PdfSecurityError) as error:
        logging.error("Falha ao preparar o processamento hierarquico: %s", error)
        return 1

    for output_path in output_paths:
        logging.info("Markdown hierarquico gerado com sucesso em: %s", output_path)
    return 0
