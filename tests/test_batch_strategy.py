from pathlib import Path

from extractcontentfrompdf.converter.hierarchical_document_builder import (
    HierarchicalMarkdownDocumentBuilder,
)
from extractcontentfrompdf.converter.processor import PdfDocumentProcessor
from extractcontentfrompdf.converter.strategies.batch import BatchConversionStrategy


def test_batch_strategy_existe_com_nome_alinhado() -> None:
    assert BatchConversionStrategy.__name__ == "BatchConversionStrategy"
    assert HierarchicalMarkdownDocumentBuilder.__name__ == "HierarchicalMarkdownDocumentBuilder"
    assert PdfDocumentProcessor.__name__ == "PdfDocumentProcessor"
