"""Politicas para decidir se um PDF pode seguir para extracao."""

from __future__ import annotations

from extractcontentfrompdf.models import PdfDocument
from extractcontentfrompdf.security.exceptions import PdfSecurityError
from extractcontentfrompdf.security.models import PdfSecurityReport


class PdfSecurityPolicy:
    """Aplica as regras de bloqueio a partir do relatorio de seguranca."""

    def enforce(self, document: PdfDocument, report: PdfSecurityReport) -> None:
        """Interrompe o fluxo quando ha sinais bloqueantes no documento."""
        blocking_issues = [
            issue.description for issue in report.issues if issue.blocking
        ]
        if not blocking_issues:
            return

        reasons = "; ".join(blocking_issues)
        raise PdfSecurityError(
            "PDF bloqueado por regra conservadora da triagem de seguranca "
            f"({document.name}). Sinais detectados: {reasons}. "
            "Se voce confiar na origem do arquivo, rode novamente com "
            "--no-check-security para ignorar essa etapa."
        )
