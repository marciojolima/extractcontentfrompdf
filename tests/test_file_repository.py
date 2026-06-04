from pathlib import Path

import pytest

from extractcontentfrompdf.file_repository import MarkdownFileRepository
from extractcontentfrompdf.models import MarkdownDocument


def test_ensure_output_directory_cria_diretorio(tmp_path: Path) -> None:
    repository = MarkdownFileRepository()
    output_dir = tmp_path / "saida" / "markdown"

    repository.ensure_output_directory(output_dir)

    assert output_dir.exists()
    assert output_dir.is_dir()


def test_save_persiste_markdown_no_caminho_esperado(tmp_path: Path) -> None:
    repository = MarkdownFileRepository()
    document = MarkdownDocument(
        title="resultado",
        body="Corpo",
        content="# Conteudo\n",
    )

    output_path = repository.save(tmp_path, document)

    assert output_path == tmp_path / "resultado.md"
    assert output_path.read_text(encoding="utf-8") == "# Conteudo\n"


def test_save_sanitiza_nome_do_arquivo(tmp_path: Path) -> None:
    repository = MarkdownFileRepository()
    document = MarkdownDocument(
        title="fase/01\\aula",
        body="Corpo",
        content="# Conteudo\n",
    )

    output_path = repository.save(tmp_path, document)

    assert output_path == tmp_path / "fase_01_aula.md"


def test_save_falha_quando_saida_nao_e_diretorio(tmp_path: Path) -> None:
    repository = MarkdownFileRepository()
    output_file = tmp_path / "saida.md"
    output_file.write_text("x", encoding="utf-8")
    document = MarkdownDocument(
        title="resultado",
        body="Corpo",
        content="# Conteudo\n",
    )

    with pytest.raises(ValueError, match="precisa ser um diretorio"):
        repository.save(output_file, document)
