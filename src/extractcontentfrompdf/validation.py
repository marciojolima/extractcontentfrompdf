"""Validacoes de entrada para o fluxo de processamento."""

from __future__ import annotations

from extractcontentfrompdf.models import PdfDocument


class PdfSourceValidator:
    """Valida o arquivo de origem antes do processamento."""

    def validate(self, document: PdfDocument) -> None:
        """Garante que a origem exista, seja arquivo e tenha extensao PDF."""
        if not document.path.exists():
            raise FileNotFoundError(f"Arquivo PDF nao encontrado: {document.path}")

        if not document.path.is_file():
            raise ValueError(f"O caminho informado nao e um arquivo: {document.path}")

        if document.path.suffix.lower() != ".pdf":
            raise ValueError(
                f"O arquivo informado nao possui extensao PDF: {document.path}"
            )
