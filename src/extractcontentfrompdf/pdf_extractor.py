"""Extracao de texto a partir de documentos PDF."""

from __future__ import annotations

import logging

import pdfplumber

from extractcontentfrompdf.models import ExtractionResult, PdfDocument
from extractcontentfrompdf.sanitizer import TextSanitizer


class PdfTextExtractor:
    """Extrai e sanitiza o texto de um PDF pagina por pagina."""

    def __init__(self, sanitizer: TextSanitizer) -> None:
        self._sanitizer = sanitizer

    def extract(self, document: PdfDocument) -> ExtractionResult:
        """Retorna o conteudo util extraido do documento informado."""
        page_sections: list[str] = []

        with pdfplumber.open(document.path) as pdf:
            page_count = len(pdf.pages)

            for page_number, page in enumerate(pdf.pages, start=1):
                raw_text = page.extract_text() or ""
                sanitized_text = self._sanitizer.sanitize(raw_text)

                if not sanitized_text:
                    logging.warning(
                        "Pagina %s sem texto util em %s",
                        page_number,
                        document.name,
                    )
                    continue

                page_sections.append(
                    self._build_page_section(page_number=page_number, content=sanitized_text)
                )

        content = "\n\n".join(page_sections).strip()
        return ExtractionResult(page_count=page_count, content=content)

    def _build_page_section(self, page_number: int, content: str) -> str:
        """Monta a secao referente a uma pagina extraida."""
        return f"## Pagina {page_number}\n\n{content}"
