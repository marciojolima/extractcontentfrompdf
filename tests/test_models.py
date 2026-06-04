from pathlib import Path

from extractcontentfrompdf.models import PdfDocument


def test_pdf_document_expoe_nome_e_stem() -> None:
    document = PdfDocument(path=Path("pasta/exemplo.pdf"))

    assert document.name == "exemplo.pdf"
    assert document.stem == "exemplo"
