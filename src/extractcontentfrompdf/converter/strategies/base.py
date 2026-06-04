"""Contratos de estrategias de conversao."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol


class ConversionStrategy(Protocol):
    """Define o contrato minimo para uma estrategia de conversao."""

    def execute(self, request: object) -> Path:
        """Executa a estrategia com a requisicao informada."""
