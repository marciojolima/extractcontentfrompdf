import logging
from pathlib import Path

import pytest

from extractcontentfrompdf.entrypoints import single
from extractcontentfrompdf.entrypoints.bootstrap import DEFAULT_OUTPUT_DIR
from extractcontentfrompdf.security.exceptions import PdfSecurityError


def test_parse_args_exige_pdf_de_entrada() -> None:
    with pytest.raises(SystemExit):
        single.parse_args([])


def test_parse_args_le_pdf_e_intervalo_informados() -> None:
    args = single.parse_args(["arquivo.pdf", "2", "5", "--output-dir", "saida"])

    assert args.pdf_path == Path("arquivo.pdf")
    assert args.start_page == 2
    assert args.end_page == 5
    assert args.output_dir == Path("saida")
    assert args.check_security is True


def test_parse_args_aplica_defaults_restantes() -> None:
    args = single.parse_args(["arquivo.pdf"])

    assert args.pdf_path == Path("arquivo.pdf")
    assert args.start_page is None
    assert args.end_page is None
    assert args.output_dir == DEFAULT_OUTPUT_DIR
    assert args.check_security is True


def test_parse_args_permite_desabilitar_triagem() -> None:
    args = single.parse_args(["arquivo.pdf", "--no-check-security"])

    assert args.pdf_path == Path("arquivo.pdf")
    assert args.check_security is False


def test_main_retorna_zero_quando_conversao_tem_sucesso(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeConverter:
        def convert(
            self,
            pdf_path: Path,
            output_dir: Path,
            start_page: int | None = None,
            end_page: int | None = None,
            check_security: bool = True,
        ) -> Path:
            assert pdf_path == Path("arquivo.pdf")
            assert output_dir == Path("saida")
            assert start_page == 2
            assert end_page == 5
            assert check_security is True
            return output_dir / "arquivo.md"

    monkeypatch.setattr(single, "build_converter", lambda: FakeConverter())

    assert single.main(["arquivo.pdf", "2", "5", "--output-dir", "saida"]) == 0


def test_main_retorna_um_quando_ha_erro_esperado(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeConverter:
        def convert(
            self,
            pdf_path: Path,
            output_dir: Path,
            start_page: int | None = None,
            end_page: int | None = None,
            check_security: bool = True,
        ) -> Path:
            raise FileNotFoundError("nao encontrado")

    monkeypatch.setattr(single, "build_converter", lambda: FakeConverter())

    assert single.main(["arquivo.pdf"]) == 1


def test_main_retorna_um_quando_triagem_bloqueia_pdf(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeConverter:
        def convert(
            self,
            pdf_path: Path,
            output_dir: Path,
            start_page: int | None = None,
            end_page: int | None = None,
            check_security: bool = True,
        ) -> Path:
            raise PdfSecurityError("bloqueado")

    monkeypatch.setattr(single, "build_converter", lambda: FakeConverter())

    assert single.main(["arquivo.pdf"]) == 1


def test_configure_logging_define_formato_basico(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    chamadas: dict[str, object] = {}

    def fake_basic_config(**kwargs: object) -> None:
        chamadas.update(kwargs)

    monkeypatch.setattr(logging, "basicConfig", fake_basic_config)

    single.configure_logging()

    assert chamadas == {"level": logging.INFO, "format": "%(levelname)s: %(message)s"}


def test_main_repassa_parametro_para_ignorar_triagem(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeConverter:
        def convert(
            self,
            pdf_path: Path,
            output_dir: Path,
            start_page: int | None = None,
            end_page: int | None = None,
            check_security: bool = True,
        ) -> Path:
            assert check_security is False
            return output_dir / "arquivo.md"

    monkeypatch.setattr(single, "build_converter", lambda: FakeConverter())

    assert single.main(["arquivo.pdf", "--no-check-security", "--output-dir", "saida"]) == 0
