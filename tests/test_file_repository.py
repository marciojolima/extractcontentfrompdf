from pathlib import Path

import pytest

from extractcontentfrompdf.file_repository import MarkdownFileRepository
from extractcontentfrompdf.models import MarkdownDocument, PdfDocument


def test_ensure_output_directory_cria_diretorio(tmp_path: Path) -> None:
    repository = MarkdownFileRepository()
    output_dir = tmp_path / "saida" / "markdown"

    repository.ensure_output_directory(output_dir)

    assert output_dir.exists()
    assert output_dir.is_dir()


def test_validate_source_falha_quando_arquivo_nao_existe(tmp_path: Path) -> None:
    repository = MarkdownFileRepository()
    document = PdfDocument(path=tmp_path / "inexistente.pdf")

    with pytest.raises(FileNotFoundError):
        repository.validate_source(document)


def test_validate_source_falha_quando_extensao_nao_e_pdf(tmp_path: Path) -> None:
    repository = MarkdownFileRepository()
    source_path = tmp_path / "arquivo.txt"
    source_path.write_text("conteudo", encoding="utf-8")
    document = PdfDocument(path=source_path)

    with pytest.raises(ValueError):
        repository.validate_source(document)


def test_save_persiste_markdown_no_caminho_esperado(tmp_path: Path) -> None:
    repository = MarkdownFileRepository()
    document = MarkdownDocument(title="resultado", content="# Conteudo\n")

    output_path = repository.save(tmp_path, document)

    assert output_path == tmp_path / "resultado.md"
    assert output_path.read_text(encoding="utf-8") == "# Conteudo\n"
