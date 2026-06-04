"""Objetos de requisicao para os fluxos de conversao."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class SingleFileConversionRequest:
    """Parametros necessarios para converter um unico PDF."""

    pdf_path: Path
    output_dir: Path
    start_page: int | None = None
    end_page: int | None = None
    check_security: bool = True


@dataclass(frozen=True, slots=True)
class HierarchicalBatchConversionRequest:
    """Parametros necessarios para converter uma ou mais arvores de diretorios."""

    root_dirs: tuple[Path, ...]
    output_dir: Path
    check_security: bool = True
