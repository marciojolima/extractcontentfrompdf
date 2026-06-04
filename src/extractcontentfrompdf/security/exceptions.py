"""Excecoes especificas da camada de seguranca."""

from __future__ import annotations


class PdfSecurityError(ValueError):
    """Indica que o PDF foi bloqueado pelas regras basicas de seguranca."""
