"""Modelos de dominio para o fluxo de extracao de PDF."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class PdfDocument:
    """Representa um documento PDF de entrada."""

    path: Path

    @property
    def name(self) -> str:
        """Retorna o nome do arquivo com extensao."""
        return self.path.name

    @property
    def stem(self) -> str:
        """Retorna o nome do arquivo sem extensao."""
        return self.path.stem


@dataclass(frozen=True, slots=True)
class ExtractionResult:
    """Representa o resultado da extracao textual do PDF."""

    page_count: int
    content: str


@dataclass(frozen=True, slots=True)
class MarkdownDocument:
    """Representa o documento Markdown pronto para persistencia."""

    title: str
    content: str
