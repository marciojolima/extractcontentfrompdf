"""Persistencia e validacoes relacionadas a arquivos."""

from __future__ import annotations

from pathlib import Path

from extractcontentfrompdf.models import MarkdownDocument, PdfDocument


class MarkdownFileRepository:
    """Valida caminhos e persiste documentos Markdown no sistema de arquivos."""

    def ensure_output_directory(self, output_dir: Path) -> None:
        """Garante que o diretorio de saida exista."""
        output_dir.mkdir(parents=True, exist_ok=True)

    def validate_source(self, document: PdfDocument) -> None:
        """Valida se o arquivo de entrada existe e possui extensao PDF."""
        if not document.path.exists():
            raise FileNotFoundError(f"Arquivo PDF nao encontrado: {document.path}")

        if document.path.suffix.lower() != ".pdf":
            raise ValueError(
                f"O arquivo informado nao possui extensao PDF: {document.path}"
            )

    def save(self, output_dir: Path, document: MarkdownDocument) -> Path:
        """Salva o conteudo Markdown em UTF-8 e retorna o caminho gerado."""
        output_path = output_dir / f"{document.title}.md"
        output_path.write_text(document.content, encoding="utf-8")
        return output_path
