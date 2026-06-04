"""Construcao do conteudo Markdown de saida."""

from __future__ import annotations

from extractcontentfrompdf.models import ExtractionResult, MarkdownDocument, PdfDocument


class MarkdownDocumentBuilder:
    """Transforma o resultado da extracao em um documento Markdown."""

    EMPTY_CONTENT_MESSAGE = "_Nenhum texto util foi extraido do PDF._"

    def build(
        self,
        document: PdfDocument,
        extraction_result: ExtractionResult,
    ) -> MarkdownDocument:
        """Monta o corpo final do arquivo Markdown com metadados simples."""
        body_sections = [
            f"**Paginas do PDF:** {extraction_result.total_pages}",
            f"**Paginas processadas:** {extraction_result.processed_pages}",
            "",
        ]

        if extraction_result.content:
            body_sections.append(extraction_result.content)
        else:
            body_sections.append(self.EMPTY_CONTENT_MESSAGE)

        body = "\n".join(body_sections).strip()
        content = f"# {document.stem}\n\n{body}\n"
        return MarkdownDocument(title=document.stem, body=body, content=content)
