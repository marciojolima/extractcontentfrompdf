from pathlib import Path

import pytest

from extractcontentfrompdf.models import PdfDocument
from extractcontentfrompdf.validation import PdfSourceValidator


def test_validate_falha_quando_arquivo_nao_existe(tmp_path: Path) -> None:
    validator = PdfSourceValidator()
    document = PdfDocument(path=tmp_path / "inexistente.pdf")

    with pytest.raises(FileNotFoundError):
        validator.validate(document)


def test_validate_falha_quando_caminho_nao_e_arquivo(tmp_path: Path) -> None:
    validator = PdfSourceValidator()
    document = PdfDocument(path=tmp_path)

    with pytest.raises(ValueError, match="nao e um arquivo"):
        validator.validate(document)


def test_validate_falha_quando_extensao_nao_e_pdf(tmp_path: Path) -> None:
    validator = PdfSourceValidator()
    source_path = tmp_path / "arquivo.txt"
    source_path.write_text("conteudo", encoding="utf-8")
    document = PdfDocument(path=source_path)

    with pytest.raises(ValueError, match="extensao PDF"):
        validator.validate(document)


def test_validate_aceita_pdf_existente(tmp_path: Path) -> None:
    validator = PdfSourceValidator()
    source_path = tmp_path / "arquivo.pdf"
    source_path.write_text("conteudo", encoding="utf-8")

    validator.validate(PdfDocument(path=source_path))
