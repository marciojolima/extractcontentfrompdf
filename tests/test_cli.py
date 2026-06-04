import logging
from pathlib import Path

import pytest

from extractcontentfrompdf import cli
from extractcontentfrompdf.converter import PdfDocumentProcessor, PdfToMarkdownConverter
from extractcontentfrompdf.converter.strategies import (
    HierarchicalBatchConversionStrategy,
    SingleFileConversionStrategy,
)
from extractcontentfrompdf.file_repository import MarkdownFileRepository
from extractcontentfrompdf.markdown_builder import MarkdownDocumentBuilder
from extractcontentfrompdf.pdf_extractor import PdfTextExtractor
from extractcontentfrompdf.security.policy import PdfSecurityPolicy
from extractcontentfrompdf.security.scanner import PdfSecurityScanner
from extractcontentfrompdf.sanitizer import TextSanitizer


def test_build_converter_monta_dependencias_esperadas() -> None:
    converter = cli.build_converter()

    assert isinstance(converter, PdfToMarkdownConverter)
    assert isinstance(converter._document_processor, PdfDocumentProcessor)
    assert isinstance(converter._document_processor._extractor, PdfTextExtractor)
    assert isinstance(converter._document_processor._extractor._sanitizer, TextSanitizer)
    assert isinstance(converter._document_processor._markdown_builder, MarkdownDocumentBuilder)
    assert isinstance(converter._document_processor._repository, MarkdownFileRepository)
    assert isinstance(converter._document_processor._security_scanner, PdfSecurityScanner)
    assert isinstance(converter._document_processor._security_policy, PdfSecurityPolicy)
    assert isinstance(converter._single_file_strategy, SingleFileConversionStrategy)
    assert isinstance(converter._hierarchical_batch_strategy, HierarchicalBatchConversionStrategy)


def test_parse_args_usa_defaults_quando_nenhum_argumento_e_informado() -> None:
    args = cli.parse_args([])

    assert args.pdf_path == cli.INPUT_PDF_PATH
    assert args.start_page is None
    assert args.end_page is None
    assert args.output_dir == cli.OUTPUT_DIR
    assert args.check_security is True


def test_parse_args_le_pdf_e_intervalo_informados() -> None:
    args = cli.parse_args(["arquivo.pdf", "2", "5", "--output-dir", "saida"])

    assert args.pdf_path == Path("arquivo.pdf")
    assert args.start_page == 2
    assert args.end_page == 5
    assert args.output_dir == Path("saida")
    assert args.check_security is True


def test_parse_args_permite_desabilitar_triagem() -> None:
    args = cli.parse_args(["arquivo.pdf", "--no-check-security"])

    assert args.pdf_path == Path("arquivo.pdf")
    assert args.check_security is False


def test_main_retorna_zero_quando_conversao_tem_sucesso(monkeypatch: pytest.MonkeyPatch) -> None:
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

    monkeypatch.setattr(cli, "build_converter", lambda: FakeConverter())

    assert cli.main(["arquivo.pdf", "2", "5", "--output-dir", "saida"]) == 0


def test_main_retorna_um_quando_ha_erro_esperado(monkeypatch: pytest.MonkeyPatch) -> None:
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

    monkeypatch.setattr(cli, "build_converter", lambda: FakeConverter())

    assert cli.main(["arquivo.pdf"]) == 1


def test_configure_logging_define_formato_basico(monkeypatch: pytest.MonkeyPatch) -> None:
    chamadas: dict[str, object] = {}

    def fake_basic_config(**kwargs: object) -> None:
        chamadas.update(kwargs)

    monkeypatch.setattr(logging, "basicConfig", fake_basic_config)

    cli.configure_logging()

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

    monkeypatch.setattr(cli, "build_converter", lambda: FakeConverter())

    assert cli.main(["arquivo.pdf", "--no-check-security", "--output-dir", "saida"]) == 0
