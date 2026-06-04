"""Modelos de dominio para o fluxo de extracao de PDF."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class PdfDocument:
    """Representa um documento PDF de entrada."""

    path: Path
    start_page: int | None = None
    end_page: int | None = None

    def __post_init__(self) -> None:
        """Valida apenas a consistencia basica do intervalo solicitado."""
        if self.start_page is not None and self.start_page < 1:
            raise ValueError("A pagina inicial deve ser maior ou igual a 1.")

        if self.end_page is not None and self.end_page < 1:
            raise ValueError("A pagina final deve ser maior ou igual a 1.")

        if (
            self.start_page is not None
            and self.end_page is not None
            and self.start_page > self.end_page
        ):
            raise ValueError(
                "A pagina inicial nao pode ser maior do que a pagina final."
            )

    @property
    def name(self) -> str:
        """Retorna o nome do arquivo com extensao."""
        return self.path.name

    @property
    def stem(self) -> str:
        """Retorna o nome do arquivo sem extensao."""
        return self.path.stem

    def resolve_page_interval(self, total_pages: int) -> tuple[int, int] | None:
        """Resolve o intervalo efetivo respeitando o total de paginas do PDF."""
        if total_pages < 1:
            return None

        start_page = self.start_page or 1
        end_page = self.end_page or total_pages

        if start_page > total_pages:
            raise ValueError(
                f"A pagina inicial {start_page} excede o total de paginas do PDF ({total_pages})."
            )

        if end_page > total_pages:
            raise ValueError(
                f"A pagina final {end_page} excede o total de paginas do PDF ({total_pages})."
            )

        return start_page, end_page


@dataclass(frozen=True, slots=True)
class ExtractionResult:
    """Representa o resultado da extracao textual do PDF."""

    total_pages: int
    processed_pages: int
    content: str


@dataclass(frozen=True, slots=True)
class MarkdownDocument:
    """Representa o documento Markdown pronto para persistencia."""

    title: str
    body: str
    content: str
