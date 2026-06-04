from pathlib import Path

import pytest

from extractcontentfrompdf.models import PdfDocument
from extractcontentfrompdf.security.exceptions import PdfSecurityError
from extractcontentfrompdf.security.models import PdfSecurityIssue, PdfSecurityReport
from extractcontentfrompdf.security.policy import PdfSecurityPolicy


def test_enforce_nao_falha_quando_relatorio_esta_limpo() -> None:
    policy = PdfSecurityPolicy()
    report = PdfSecurityReport(issues=())

    policy.enforce(PdfDocument(path=Path("seguro.pdf")), report)


def test_enforce_bloqueia_quando_existe_issue_bloqueante() -> None:
    policy = PdfSecurityPolicy()
    report = PdfSecurityReport(
        issues=(
            PdfSecurityIssue(
                code="javascript",
                description="codigo JavaScript embutido",
                blocking=True,
            ),
        )
    )

    with pytest.raises(PdfSecurityError, match="codigo JavaScript embutido"):
        policy.enforce(PdfDocument(path=Path("suspeito.pdf")), report)
