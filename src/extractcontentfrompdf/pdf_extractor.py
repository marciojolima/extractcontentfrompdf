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
            total_pages = len(pdf.pages)
            resolved_interval = document.resolve_page_interval(total_pages)

            if resolved_interval is None:
                return ExtractionResult(
                    total_pages=0,
                    processed_pages=0,
                    content="",
                )

            start_page, end_page = resolved_interval

            for page_number in range(start_page, end_page + 1):
                page = pdf.pages[page_number - 1]
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
        return ExtractionResult(
            total_pages=total_pages,
            processed_pages=end_page - start_page + 1,
            content=content,
        )

    def _build_page_section(self, page_number: int, content: str) -> str:
        """Monta a secao referente a uma pagina extraida."""
        return f"## Pagina {page_number}\n\n{content}"
