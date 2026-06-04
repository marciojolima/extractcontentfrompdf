from pathlib import Path

import pytest

from extractcontentfrompdf.models import PdfDocument


def test_pdf_document_expoe_nome_e_stem() -> None:
    document = PdfDocument(path=Path("pasta/exemplo.pdf"))

    assert document.name == "exemplo.pdf"
    assert document.stem == "exemplo"


def test_pdf_document_valida_intervalo_basico() -> None:
    with pytest.raises(ValueError, match="pagina inicial"):
        PdfDocument(path=Path("exemplo.pdf"), start_page=0)

    with pytest.raises(ValueError, match="pagina final"):
        PdfDocument(path=Path("exemplo.pdf"), end_page=0)

    with pytest.raises(ValueError, match="inicial nao pode ser maior"):
        PdfDocument(path=Path("exemplo.pdf"), start_page=3, end_page=2)


def test_pdf_document_resolve_intervalo_com_defaults() -> None:
    document = PdfDocument(path=Path("exemplo.pdf"))

    assert document.resolve_page_interval(total_pages=5) == (1, 5)


def test_pdf_document_falha_quando_intervalo_excede_total_de_paginas() -> None:
    document = PdfDocument(path=Path("exemplo.pdf"), start_page=2, end_page=6)

    with pytest.raises(ValueError, match="pagina final 6 excede o total"):
        document.resolve_page_interval(total_pages=5)
