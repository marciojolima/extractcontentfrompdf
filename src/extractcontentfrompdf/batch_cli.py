"""Ponto de entrada da linha de comando para processamento em lote."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Sequence

from extractcontentfrompdf.cli import OUTPUT_DIR, build_converter, configure_logging


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Le os argumentos da CLI para processamento de varios PDFs."""
    parser = argparse.ArgumentParser(
        prog="extract-pdf-batch",
        description=(
            "Extrai texto de varios arquivos PDF a partir de uma pasta raiz "
            "e salva o resultado consolidado em um unico Markdown."
        ),
    )
    parser.add_argument(
        "root_dir",
        type=Path,
        help="Diretorio raiz que sera varrido recursivamente em busca de PDFs.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help="Diretorio onde o arquivo Markdown consolidado sera salvo.",
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


def find_pdf_files(root_dir: Path) -> list[Path]:
    """Retorna os PDFs encontrados recursivamente em ordem deterministica."""
    if not root_dir.exists():
        raise FileNotFoundError(f"Diretorio raiz nao encontrado: {root_dir}")

    if not root_dir.is_dir():
        raise ValueError(f"O caminho informado nao e um diretorio: {root_dir}")

    pdf_files = sorted(
        path
        for path in root_dir.rglob("*")
        if path.is_file() and path.suffix.lower() == ".pdf"
    )
    if not pdf_files:
        raise ValueError(f"Nenhum arquivo PDF foi encontrado em: {root_dir}")

    return pdf_files


def main(argv: Sequence[str] | None = None) -> int:
    """Executa o fluxo principal da aplicacao em lote."""
    configure_logging()
    args = parse_args(argv)
    converter = build_converter()

    try:
        pdf_files = find_pdf_files(args.root_dir)
        output_path = converter.convert_batch(
            pdf_paths=pdf_files,
            output_dir=args.output_dir,
            bundle_name=args.root_dir.name,
            check_security=args.check_security,
        )
    except (FileNotFoundError, PermissionError, ValueError) as error:
        logging.error("Falha ao preparar o processamento em lote: %s", error)
        return 1
    except Exception as error:  # pragma: no cover - protecao para PDFs inesperados
        logging.error("Falha inesperada ao processar os PDFs em lote: %s", error)
        return 1

    logging.info("Markdown consolidado gerado com sucesso em: %s", output_path)
    return 0
