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
    def has_issues(self) -> bool:
        """Indica se a triagem encontrou qualquer sinal relevante."""
        return bool(self.issues)

    @property
    def has_blocking_issues(self) -> bool:
        """Indica se a triagem encontrou sinais que impedem o processamento."""
        return any(issue.blocking for issue in self.issues)

    @property
    def is_safe(self) -> bool:
        """Indica se o documento passou pela triagem sem bloqueios."""
        return not self.has_blocking_issues
