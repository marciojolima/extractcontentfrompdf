import logging

from extractcontentfrompdf.bootstrap import build_converter, configure_logging
from extractcontentfrompdf.converter import PdfToMarkdownConverter


def test_build_converter_retorna_fachada_pronta_para_uso() -> None:
    converter = build_converter()

    assert isinstance(converter, PdfToMarkdownConverter)


def test_configure_logging_define_formato_basico(
    monkeypatch,
) -> None:
    chamadas: dict[str, object] = {}

    def fake_basic_config(**kwargs: object) -> None:
        chamadas.update(kwargs)

    monkeypatch.setattr(logging, "basicConfig", fake_basic_config)

    configure_logging()

    assert chamadas == {"level": logging.INFO, "format": "%(levelname)s: %(message)s"}
