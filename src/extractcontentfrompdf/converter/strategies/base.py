"""Contratos de estrategias de conversao."""

from __future__ import annotations

from typing import Protocol


class ConversionStrategy(Protocol):
    """Define o contrato minimo para uma estrategia de conversao."""

    def execute(self, request: object) -> object:
        """Executa a estrategia com a requisicao informada."""
