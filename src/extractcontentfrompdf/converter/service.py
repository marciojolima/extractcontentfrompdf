"""Servico para executar estrategias de conversao."""

from __future__ import annotations

from extractcontentfrompdf.converter.strategies.base import ConversionStrategy


class PdfConversionService:
    """Orquestra a execucao de uma estrategia de conversao."""

    def execute(self, strategy: ConversionStrategy, request: object) -> object:
        """Delega a conversao para a estrategia informada."""
        return strategy.execute(request)
