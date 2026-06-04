import logging
from pathlib import Path

import pytest

from extractcontentfrompdf import cli
from extractcontentfrompdf.converter import PdfToMarkdownConverter
from extractcontentfrompdf.file_repository import MarkdownFileRepository
from extractcontentfrompdf.markdown_builder import MarkdownDocumentBuilder
from extractcontentfrompdf.pdf_extractor import PdfTextExtractor
from extractcontentfrompdf.security.policy import PdfSecurityPolicy
from extractcontentfrompdf.security.scanner import PdfSecurityScanner
from extractcontentfrompdf.sanitizer import TextSanitizer


def test_build_converter_monta_dependencias_esperadas() -> None:
    converter = cli.build_converter()

    assert isinstance(converter, PdfToMarkdownConverter)
    assert isinstance(converter._extractor, PdfTextExtractor)
    assert isinstance(converter._extractor._sanitizer, TextSanitizer)
    assert isinstance(converter._markdown_builder, MarkdownDocumentBuilder)
    assert isinstance(converter._repository, MarkdownFileRepository)
    assert isinstance(converter._security_scanner, PdfSecurityScanner)
    assert isinstance(converter._security_policy, PdfSecurityPolicy)


def test_main_retorna_zero_quando_conversao_tem_sucesso(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeConverter:
        def convert(self, pdf_path: Path, output_dir: Path) -> Path:
            assert pdf_path == cli.INPUT_PDF_PATH
            assert output_dir == cli.OUTPUT_DIR
            return output_dir / "arquivo.md"

    monkeypatch.setattr(cli, "build_converter", lambda: FakeConverter())

    assert cli.main() == 0


def test_main_retorna_um_quando_ha_erro_esperado(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeConverter:
        def convert(self, pdf_path: Path, output_dir: Path) -> Path:
            raise FileNotFoundError("nao encontrado")

    monkeypatch.setattr(cli, "build_converter", lambda: FakeConverter())

    assert cli.main() == 1


def test_configure_logging_define_formato_basico(monkeypatch: pytest.MonkeyPatch) -> None:
    chamadas: dict[str, object] = {}

    def fake_basic_config(**kwargs: object) -> None:
        chamadas.update(kwargs)

    monkeypatch.setattr(logging, "basicConfig", fake_basic_config)

    cli.configure_logging()

    assert chamadas == {"level": logging.INFO, "format": "%(levelname)s: %(message)s"}
