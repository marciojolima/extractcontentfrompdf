"""Persistencia de documentos Markdown em disco."""

from __future__ import annotations

from pathlib import Path

from extractcontentfrompdf.models import MarkdownDocument


class MarkdownFileRepository:
    """Persiste documentos Markdown no sistema de arquivos."""

    def ensure_output_directory(self, output_dir: Path) -> None:
        """Garante que o diretorio de saida exista."""
        output_dir.mkdir(parents=True, exist_ok=True)

    def save(self, output_dir: Path, document: MarkdownDocument) -> Path:
        """Salva o conteudo Markdown em UTF-8 e retorna o caminho gerado."""
        if output_dir.exists() and not output_dir.is_dir():
            raise ValueError(
                f"O caminho de saida precisa ser um diretorio: {output_dir}"
            )

        output_path = output_dir / f"{self._sanitize_filename(document.title)}.md"
        output_path.write_text(document.content, encoding="utf-8")
        return output_path

    def _sanitize_filename(self, value: str) -> str:
        """Normaliza o nome do arquivo para evitar separadores de caminho."""
        sanitized = value.replace("/", "_").replace("\\", "_").strip()
        return sanitized or "documento"
