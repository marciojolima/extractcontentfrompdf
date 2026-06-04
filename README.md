# ExtractContentFromPdf

Projeto em Python para extrair texto de PDFs nativos e salvar o resultado em Markdown.

## Linha de comando

### PDF individual

```bash
poetry run extract-pdf caminho/arquivo.pdf
```

### Lote de PDFs

```bash
poetry run extract-pdf-batch caminho/pasta-raiz
```

O comando em lote busca PDFs recursivamente dentro da pasta raiz informada e gera um unico arquivo Markdown com o nome desse diretorio.

### Lote hierarquico

```bash
poetry run extract-pdf-hierarchical data/in/Fase01 data/in/Fase02
```

O comando hierarquico recebe um ou mais diretorios raiz explicitos, preserva a estrutura de subpastas na consolidacao e gera um arquivo Markdown por raiz informada.

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
