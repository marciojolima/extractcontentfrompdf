from pathlib import Path

import pytest

from extractcontentfrompdf import batch_cli


def test_parse_args_le_argumentos_do_processamento_em_lote() -> None:
    args = batch_cli.parse_args(["./entrada", "--output-dir", "saida", "--no-check-security"])

    assert args.root_dir == Path("./entrada")
    assert args.output_dir == Path("saida")
    assert args.check_security is False


def test_find_pdf_files_varre_subdiretorios_e_ignora_outros_arquivos(tmp_path: Path) -> None:
    root_dir = tmp_path / "entrada"
    nested_dir = root_dir / "a" / "b"
    nested_dir.mkdir(parents=True)
    primeiro_pdf = root_dir / "01.pdf"
    segundo_pdf = nested_dir / "02.PDF"
    primeiro_pdf.write_text("fake", encoding="utf-8")
    segundo_pdf.write_text("fake", encoding="utf-8")
    (nested_dir / "ignorar.txt").write_text("nao", encoding="utf-8")

    pdf_files = batch_cli.find_pdf_files(root_dir)

    assert pdf_files == [primeiro_pdf, segundo_pdf]


def test_find_pdf_files_falha_quando_nao_encontra_pdfs(tmp_path: Path) -> None:
    root_dir = tmp_path / "vazio"
    root_dir.mkdir()

    with pytest.raises(ValueError):
        batch_cli.find_pdf_files(root_dir)


def test_main_retorna_zero_quando_conversao_em_lote_tem_sucesso(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeConverter:
        def convert_batch(
            self,
            pdf_paths: list[Path],
            output_dir: Path,
            bundle_name: str,
            check_security: bool = True,
        ) -> Path:
            assert pdf_paths == [Path("entrada/a.pdf"), Path("entrada/sub/b.pdf")]
            assert output_dir == Path("saida")
            assert bundle_name == "entrada"
            assert check_security is False
            return output_dir / "entrada.md"

    monkeypatch.setattr(batch_cli, "build_converter", lambda: FakeConverter())
    monkeypatch.setattr(
        batch_cli,
        "find_pdf_files",
        lambda root_dir: [root_dir / "a.pdf", root_dir / "sub" / "b.pdf"],
    )

    assert batch_cli.main(["entrada", "--output-dir", "saida", "--no-check-security"]) == 0


def test_main_retorna_um_quando_ha_erro_esperado(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(batch_cli, "build_converter", lambda: object())
    monkeypatch.setattr(
        batch_cli,
        "find_pdf_files",
        lambda root_dir: (_ for _ in ()).throw(FileNotFoundError("nao encontrado")),
    )

    assert batch_cli.main(["entrada"]) == 1
