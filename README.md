# ExtractContentFromPdf

Projeto em Python para extrair texto de PDFs nativos e salvar o resultado em Markdown.

## Testes unitarios

O projeto usa `pytest` como dependencia de desenvolvimento.

### Instalar dependencias

```bash
poetry install
```

### Executar testes

```bash
poetry run pytest
```

Esse comando tambem gera o relatorio de cobertura em HTML no diretorio `htmlcov/`.

### Escopo inicial recomendado

Os testes unitarios foram preparados para focar apenas metodos publicos:

- `TextSanitizer.sanitize`
- `MarkdownDocumentBuilder.build`
- `MarkdownFileRepository.ensure_output_directory`
- `MarkdownFileRepository.validate_source`
- `MarkdownFileRepository.save`
- `PdfToMarkdownConverter.convert`
- `PdfTextExtractor.extract`
- `configure_logging`, `build_converter` e `main` em `cli.py`
