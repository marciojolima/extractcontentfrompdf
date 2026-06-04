"""Servicos de sanitizacao de texto extraido."""

from __future__ import annotations

import re


class TextSanitizer:
    """Centraliza as regras de limpeza aplicadas ao texto extraido."""

    NULL_CHARACTER = "\x00"

    def __init__(self) -> None:
        self._invalid_surrogates_pattern = re.compile(r"[\ud800-\udfff]")
        self._horizontal_whitespace_pattern = re.compile(r"[^\S\r\n]+")
        self._excessive_breaks_pattern = re.compile(r"\n{3,}")

    def sanitize(self, text: str) -> str:
        """Remove ruidos comuns e normaliza espacos sem perder estrutura basica."""
        text_without_nulls = text.replace(self.NULL_CHARACTER, "")
        text_without_surrogates = self._remove_invalid_surrogates(text_without_nulls)
        text_with_normalized_spaces = self._normalize_horizontal_spaces(
            text_without_surrogates
        )
        text_with_compact_breaks = self._collapse_excessive_line_breaks(
            text_with_normalized_spaces
        )
        stripped_lines = [line.strip() for line in text_with_compact_breaks.splitlines()]
        return "\n".join(stripped_lines).strip()

    def _remove_invalid_surrogates(self, text: str) -> str:
        """Descarta code points surrogate isolados que podem quebrar a serializacao."""
        return self._invalid_surrogates_pattern.sub("", text)

    def _normalize_horizontal_spaces(self, text: str) -> str:
        """Normaliza sequencias de espacos e tabs sem alterar quebras de linha."""
        return self._horizontal_whitespace_pattern.sub(" ", text)

    def _collapse_excessive_line_breaks(self, text: str) -> str:
        """Reduz blocos grandes de linhas em branco para uma linha vazia."""
        return self._excessive_breaks_pattern.sub("\n\n", text)
