"""Orquestracao do fluxo de conversao de PDF para Markdown."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Sequence

from extractcontentfrompdf.file_repository import MarkdownFileRepository
from extractcontentfrompdf.markdown_builder import MarkdownDocumentBuilder
from extractcontentfrompdf.models import MarkdownDocument, PdfDocument
from extractcontentfrompdf.pdf_extractor import PdfTextExtractor
from extractcontentfrompdf.security.policy import PdfSecurityPolicy
from extractcontentfrompdf.security.models import PdfSecurityReport
from extractcontentfrompdf.security.scanner import PdfSecurityScanner


class PdfToMarkdownConverter:
    """Coordena validacao, extracao, transformacao e persistencia."""

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

    def convert(
        self,
        pdf_path: Path,
        output_dir: Path,
        start_page: int | None = None,
        end_page: int | None = None,
        check_security: bool = True,
    ) -> Path:
        """Executa o fluxo completo de processamento para um unico PDF."""
        self._repository.ensure_output_directory(output_dir)
        markdown_document = self.convert_document(
            pdf_path=pdf_path,
            start_page=start_page,
            end_page=end_page,
            check_security=check_security,
        )
        return self._repository.save(output_dir, markdown_document)

    def convert_document(
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

    def convert_batch(
        self,
        pdf_paths: Sequence[Path],
        output_dir: Path,
        bundle_name: str,
        check_security: bool = True,
    ) -> Path:
        """Processa varios PDFs e consolida o resultado em um unico Markdown."""
        if not pdf_paths:
            raise ValueError("Nenhum arquivo PDF foi informado para o processamento em lote.")

        self._repository.ensure_output_directory(output_dir)
        markdown_documents = [
            self.convert_document(pdf_path=pdf_path, check_security=check_security)
            for pdf_path in pdf_paths
        ]
        batch_document = self._build_batch_document(bundle_name, markdown_documents)
        return self._repository.save(output_dir, batch_document)

    def _build_batch_document(
        self,
        bundle_name: str,
        markdown_documents: Sequence[MarkdownDocument],
    ) -> MarkdownDocument:
        """Consolida varios documentos Markdown em um unico arquivo."""
        sections = [f"# {bundle_name}", "", f"**Arquivos processados:** {len(markdown_documents)}"]

        for markdown_document in markdown_documents:
            sections.extend(["", "---", "", markdown_document.content.rstrip()])

        content = "\n".join(sections).strip() + "\n"
        return MarkdownDocument(title=bundle_name, content=content)

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
