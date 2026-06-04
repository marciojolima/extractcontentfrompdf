from pathlib import Path

import pytest

from extractcontentfrompdf.entrypoints import batch


def test_parse_args_le_varias_raizes_para_processamento_hierarquico() -> None:
    args = batch.parse_args(
        ["entrada/Fase01", "entrada/Fase02", "--output-dir", "saida", "--no-check-security"]
    )

    assert args.root_dirs == [Path("entrada/Fase01"), Path("entrada/Fase02")]
    assert args.output_dir == Path("saida")
    assert args.check_security is False


def test_main_retorna_zero_quando_conversao_hierarquica_tem_sucesso(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeConverter:
        def convert_hierarchical(
            self,
            root_dirs: list[Path],
            output_dir: Path,
            check_security: bool = True,
        ) -> list[Path]:
            assert root_dirs == [Path("entrada/Fase01"), Path("entrada/Fase02")]
            assert output_dir == Path("saida")
            assert check_security is False
            return [output_dir / "Fase01.md", output_dir / "Fase02.md"]

    monkeypatch.setattr(batch, "build_converter", lambda: FakeConverter())

    assert (
        batch.main(
            [
                "entrada/Fase01",
                "entrada/Fase02",
                "--output-dir",
                "saida",
                "--no-check-security",
            ]
        )
        == 0
    )


def test_main_retorna_um_quando_ha_erro_esperado(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeConverter:
        def convert_hierarchical(
            self,
            root_dirs: list[Path],
            output_dir: Path,
            check_security: bool = True,
        ) -> list[Path]:
            raise FileNotFoundError("nao encontrado")

    monkeypatch.setattr(batch, "build_converter", lambda: FakeConverter())

    assert batch.main(["entrada/Fase01"]) == 1
