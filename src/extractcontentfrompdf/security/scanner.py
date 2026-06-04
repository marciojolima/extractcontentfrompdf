"""Triagem basica de seguranca para PDFs antes da extracao."""

from __future__ import annotations

from pypdf import PdfReader

from extractcontentfrompdf.models import PdfDocument
from extractcontentfrompdf.security.models import PdfSecurityIssue, PdfSecurityReport


class PdfSecurityScanner:
    """Inspeciona apenas sinais leves e de baixo custo no catalogo do PDF."""

    def scan(self, document: PdfDocument) -> PdfSecurityReport:
        """Retorna um relatorio com os sinais de risco encontrados."""
        reader = PdfReader(str(document.path), strict=False)
        catalog = reader.root_object
        issues: list[PdfSecurityIssue] = []

        if reader.is_encrypted:
            issues.append(
                PdfSecurityIssue(
                    code="encrypted",
                    description="documento criptografado",
                    blocking=True,
                )
            )

        if self._has_open_action(catalog):
            issues.append(
                PdfSecurityIssue(
                    code="open_action",
                    description="acao automatica ao abrir o arquivo",
                    blocking=True,
                )
            )

        if self._has_javascript(catalog):
            issues.append(
                PdfSecurityIssue(
                    code="javascript",
                    description="codigo JavaScript embutido",
                    blocking=True,
                )
            )

        if self._has_embedded_files(catalog):
            issues.append(
                PdfSecurityIssue(
                    code="embedded_files",
                    description="arquivos anexados ou embutidos",
                    blocking=False,
                )
            )

        return PdfSecurityReport(issues=tuple(issues))

    def _has_open_action(self, catalog: object) -> bool:
        """Detecta a presenca de acao automatica disparada na abertura."""
        return self._contains_key(catalog, "/OpenAction") or self._contains_key(
            catalog, "/AA"
        )

    def _has_javascript(self, catalog: object) -> bool:
        """Procura apenas marcadores conhecidos de JavaScript no catalogo."""
        if self._contains_key(catalog, "/JavaScript"):
            return True

        open_action = self._safe_get(catalog, "/OpenAction")
        action_type = self._safe_get(open_action, "/S")
        return action_type == "/JavaScript"

    def _has_embedded_files(self, catalog: object) -> bool:
        """Verifica a arvore de nomes por anexos sem percorrer o documento todo."""
        names = self._safe_get(catalog, "/Names")
        return self._safe_get(names, "/EmbeddedFiles") is not None

    def _contains_key(self, mapping: object, key: str) -> bool:
        """Trata dicionarios do pypdf e doubles simples usados nos testes."""
        if not hasattr(mapping, "keys"):
            return False
        return key in mapping.keys()

    def _safe_get(self, mapping: object, key: str) -> object | None:
        """Le um valor quando o objeto se comporta como um mapeamento."""
        if not hasattr(mapping, "get"):
            return None
        return mapping.get(key)
