"""Extrai texto de um PDF nativo e salva o resultado em Markdown."""

from __future__ import annotations

import logging
import re
from pathlib import Path

import pdfplumber

ARQUIVO_PDF_ENTRADA = Path(
    "data/in/Fase01/00 Intro/Pos_Tech - Cap Projeto - Fase1- Machine Learning Engineering.pdf"
)
DIRETORIO_SAIDA = Path("data/out")


def configurar_logging() -> None:
    """Configura o formato padrao de logs do script."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def garantir_diretorios(caminho_pdf: Path, diretorio_saida: Path) -> None:
    """Valida o PDF de entrada e garante que o diretorio de saida exista."""
    if not caminho_pdf.exists():
        raise FileNotFoundError(f"Arquivo PDF nao encontrado: {caminho_pdf}")

    if caminho_pdf.suffix.lower() != ".pdf":
        raise ValueError(f"O arquivo informado nao possui extensao PDF: {caminho_pdf}")

    diretorio_saida.mkdir(parents=True, exist_ok=True)


def sanitizar_texto(texto: str) -> str:
    """Remove ruidos comuns de extracao e enxuga espacos e quebras excessivas."""
    texto_limpo = texto.replace("\x00", "")
    texto_limpo = re.sub(r"[\ud800-\udfff]", "", texto_limpo)
    texto_limpo = re.sub(r"[^\S\r\n]+", " ", texto_limpo)
    texto_limpo = re.sub(r"\n{3,}", "\n\n", texto_limpo)

    linhas = [linha.strip() for linha in texto_limpo.splitlines()]
    return "\n".join(linhas).strip()


def extrair_texto_pdf(caminho_pdf: Path) -> tuple[str, int]:
    """Extrai e sanitiza o texto de todas as paginas do PDF informado."""
    textos_paginas: list[str] = []

    with pdfplumber.open(caminho_pdf) as pdf:
        total_paginas = len(pdf.pages)

        for indice, pagina in enumerate(pdf.pages, start=1):
            texto = pagina.extract_text() or ""
            texto_limpo = sanitizar_texto(texto)

            if not texto_limpo:
                logging.warning("Pagina %s sem texto util em %s", indice, caminho_pdf.name)
                continue

            textos_paginas.append(f"## Pagina {indice}\n\n{texto_limpo}")

    return "\n\n".join(textos_paginas).strip(), total_paginas


def montar_markdown(nome_arquivo: str, total_paginas: int, conteudo: str) -> str:
    """Monta o corpo final do arquivo Markdown com metadados simples."""
    secoes = [
        f"# {nome_arquivo}",
        "",
        f"**Paginas processadas:** {total_paginas}",
        "",
    ]

    if conteudo:
        secoes.append(conteudo)
    else:
        secoes.append("_Nenhum texto util foi extraido do PDF._")

    return "\n".join(secoes).strip() + "\n"


def salvar_markdown(caminho_saida: Path, conteudo_markdown: str) -> None:
    """Salva o arquivo Markdown em UTF-8."""
    caminho_saida.write_text(conteudo_markdown, encoding="utf-8")


def processar_pdf_unico(caminho_pdf: Path, diretorio_saida: Path) -> Path:
    """Executa o fluxo completo de extracao e persistencia para um unico PDF."""
    garantir_diretorios(caminho_pdf, diretorio_saida)
    conteudo, total_paginas = extrair_texto_pdf(caminho_pdf)
    markdown = montar_markdown(caminho_pdf.stem, total_paginas, conteudo)

    caminho_saida = diretorio_saida / f"{caminho_pdf.stem}.md"
    salvar_markdown(caminho_saida, markdown)
    return caminho_saida


def main() -> int:
    """Ponto de entrada do script."""
    configurar_logging()

    try:
        caminho_saida = processar_pdf_unico(ARQUIVO_PDF_ENTRADA, DIRETORIO_SAIDA)
    except (FileNotFoundError, PermissionError, ValueError) as erro:
        logging.error("Falha ao preparar o processamento: %s", erro)
        return 1
    except Exception as erro:  # pragma: no cover - protecao para PDFs inesperados
        logging.error("Falha inesperada ao processar o PDF: %s", erro)
        return 1

    logging.info("Markdown gerado com sucesso em: %s", caminho_saida)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
