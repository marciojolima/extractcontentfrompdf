"""Modelos de dominio para a triagem de seguranca de PDFs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PdfSecurityIssue:
    """Representa um sinal encontrado durante a triagem do PDF."""

    code: str
    description: str
    blocking: bool


@dataclass(frozen=True, slots=True)
class PdfSecurityReport:
    """Consolida os sinais encontrados durante a analise basica."""

    issues: tuple[PdfSecurityIssue, ...]

    @property
    def is_safe(self) -> bool:
        """Indica se o documento passou pela triagem sem bloqueios."""
        return not any(issue.blocking for issue in self.issues)
