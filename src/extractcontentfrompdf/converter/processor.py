"""Pipeline comum para processar um PDF individual."""

from __future__ import annotations

import logging
from pathlib import Path

from extractcontentfrompdf.file_repository import MarkdownFileRepository
from extractcontentfrompdf.markdown_builder import MarkdownDocumentBuilder
from extractcontentfrompdf.models import MarkdownDocument, PdfDocument
from extractcontentfrompdf.pdf_extractor import PdfTextExtractor
from extractcontentfrompdf.security.policy import PdfSecurityPolicy
from extractcontentfrompdf.security.models import PdfSecurityReport
from extractcontentfrompdf.security.scanner import PdfSecurityScanner


class PdfDocumentProcessor:
    """Executa validacao, triagem, extracao e montagem de um PDF."""

    def __init__(
        self,
        extractor: PdfTextExtractor,
        markdown_builder: MarkdownDocumentBuilder,
        repository: MarkdownFileRepository,
        security_scanner: PdfSecurityScanner,
        security_policy: PdfSecurityPolicy,
    ) -> None:
        self._extractor = extractor
        self._markdown_builder = markdown_builder
        self._repository = repository
        self._security_scanner = security_scanner
        self._security_policy = security_policy

    def process(
        self,
        pdf_path: Path,
        start_page: int | None = None,
        end_page: int | None = None,
        check_security: bool = True,
    ) -> MarkdownDocument:
        """Gera o Markdown de um unico PDF sem persistir o resultado."""
        document = PdfDocument(
            path=pdf_path,
            start_page=start_page,
            end_page=end_page,
        )
        self._repository.validate_source(document)

        if check_security:
            security_report = self._security_scanner.scan(document)
            self._log_security_report(document, security_report)
            self._security_policy.enforce(document, security_report)
        else:
            logging.info(
                "Triagem de seguranca ignorada por parametro para %s",
                document.name,
            )

        extraction_result = self._extractor.extract(document)
        return self._markdown_builder.build(document, extraction_result)

    def _log_security_report(
        self,
        document: PdfDocument,
        report: PdfSecurityReport,
    ) -> None:
        """Registra o resultado da triagem para monitoramento operacional."""
        if not report.has_issues:
            logging.info("Triagem de seguranca limpa para %s", document.name)
            return

        reasons = ", ".join(
            f"[{issue.code}] {issue.description}"
            for issue in report.issues
        )
        if report.has_blocking_issues:
            logging.warning(
                "Triagem de seguranca encontrou sinais bloqueantes em %s. "
                "Bloqueio preventivo por regra conservadora. Detalhes: %s",
                document.name,
                reasons,
            )
            return

        logging.info(
            "Triagem de seguranca encontrou sinais nao bloqueantes em %s. "
            "Detalhes: %s",
            document.name,
            reasons,
        )
