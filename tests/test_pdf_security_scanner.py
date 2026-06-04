from pathlib import Path

import pytest

from extractcontentfrompdf.models import PdfDocument
from extractcontentfrompdf.security.scanner import PdfSecurityScanner


class FakePdfReader:
    def __init__(self, path: str, strict: bool, *, encrypted: bool, root_object: dict) -> None:
        self.path = path
        self.strict = strict
        self.is_encrypted = encrypted
        self.root_object = root_object


def test_scan_identifica_sinais_bloqueantes(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_reader(path: str, strict: bool) -> FakePdfReader:
        return FakePdfReader(
            path,
            strict,
            encrypted=True,
            root_object={
                "/OpenAction": {"/S": "/JavaScript"},
                "/Names": {"/EmbeddedFiles": object()},
            },
        )

    monkeypatch.setattr("extractcontentfrompdf.security.scanner.PdfReader", fake_reader)
    scanner = PdfSecurityScanner()

    report = scanner.scan(PdfDocument(path=Path("suspeito.pdf")))

    assert report.is_safe is False
    assert [issue.code for issue in report.issues] == [
        "encrypted",
        "open_action",
        "javascript",
        "embedded_files",
    ]


def test_scan_retorna_relatorio_seguro_quando_nao_ha_sinais(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_reader(path: str, strict: bool) -> FakePdfReader:
        return FakePdfReader(path, strict, encrypted=False, root_object={})

    monkeypatch.setattr("extractcontentfrompdf.security.scanner.PdfReader", fake_reader)
    scanner = PdfSecurityScanner()

    report = scanner.scan(PdfDocument(path=Path("seguro.pdf")))

    assert report.is_safe is True
    assert report.issues == ()


def test_scan_detecta_arquivos_embutidos_sem_bloquear(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_reader(path: str, strict: bool) -> FakePdfReader:
        return FakePdfReader(
            path,
            strict,
            encrypted=False,
            root_object={"/Names": {"/EmbeddedFiles": object()}},
        )

    monkeypatch.setattr("extractcontentfrompdf.security.scanner.PdfReader", fake_reader)
    scanner = PdfSecurityScanner()

    report = scanner.scan(PdfDocument(path=Path("anexo.pdf")))

    assert report.is_safe is True
    assert report.issues[0].code == "embedded_files"
    assert report.issues[0].blocking is False
