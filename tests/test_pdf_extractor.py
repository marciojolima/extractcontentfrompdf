from pathlib import Path

import pytest

from extractcontentfrompdf.models import PdfDocument
from extractcontentfrompdf.pdf_extractor import PdfTextExtractor
from extractcontentfrompdf.sanitizer import TextSanitizer


class FakePage:
    def __init__(self, text: str | None) -> None:
        self._text = text

    def extract_text(self) -> str | None:
        return self._text


class FakePdf:
    def __init__(self, pages: list[FakePage]) -> None:
        self.pages = pages

    def __enter__(self) -> "FakePdf":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None


def test_extract_monta_sessoes_apenas_para_paginas_com_texto(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_open(path: Path) -> FakePdf:
        assert path == Path("arquivo.pdf")
        return FakePdf([FakePage("Pagina 1"), FakePage("   "), FakePage("Pagina 3")])

    monkeypatch.setattr("extractcontentfrompdf.pdf_extractor.pdfplumber.open", fake_open)
    extractor = PdfTextExtractor(sanitizer=TextSanitizer())
    document = PdfDocument(path=Path("arquivo.pdf"))

    resultado = extractor.extract(document)

    assert resultado.page_count == 3
    assert resultado.content == "## Pagina 1\n\nPagina 1\n\n## Pagina 3\n\nPagina 3"


def test_extract_registra_warning_para_pagina_sem_texto_util(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    def fake_open(path: Path) -> FakePdf:
        return FakePdf([FakePage(None)])

    monkeypatch.setattr("extractcontentfrompdf.pdf_extractor.pdfplumber.open", fake_open)
    extractor = PdfTextExtractor(sanitizer=TextSanitizer())

    with caplog.at_level("WARNING"):
        extractor.extract(PdfDocument(path=Path("vazio.pdf")))

    assert "Pagina 1 sem texto util em vazio.pdf" in caplog.text
