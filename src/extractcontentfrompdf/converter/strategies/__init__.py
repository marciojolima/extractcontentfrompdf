"""Estrategias de conversao disponiveis."""

from extractcontentfrompdf.converter.strategies.base import ConversionStrategy
from extractcontentfrompdf.converter.strategies.hierarchical_batch import (
    HierarchicalBatchConversionStrategy,
)
from extractcontentfrompdf.converter.strategies.single_file import (
    SingleFileConversionStrategy,
)

__all__ = [
    "ConversionStrategy",
    "HierarchicalBatchConversionStrategy",
    "SingleFileConversionStrategy",
]
