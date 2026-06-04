# ExtractContentFromPdf

Projeto em Python para extrair texto de PDFs nativos e salvar o resultado em Markdown enxuto.

O foco e transformar PDFs em texto limpo, sem imagens, fundos ou elementos visuais desnecessarios, gerando arquivos `.md` mais leves e mais faceis de consumir por aplicacoes com LLMs e RAG.

Isso ajuda a:

- reduzir ruido no conteudo extraido
- economizar tokens no processamento
- simplificar a leitura e a indexacao por modelos
- preservar o texto util para busca semantica e recuperacao de contexto

## Linha de comando

### PDF individual

```bash
poetry run extract-pdf caminho/arquivo.pdf
```

Converte um unico PDF em Markdown.

### Lote hierarquico

```bash
poetry run extract-pdf-hierarchical data/in/Fase01 data/in/Fase02
```

Recebe um ou mais diretorios raiz explicitos, busca PDFs recursivamente e gera um arquivo Markdown por raiz informada, preservando a organizacao das subpastas no resultado final.

Esse modo e util quando o conteudo esta organizado em trilhas, fases, modulos ou colecoes de documentos.

## Instalacao

### Requisito

- Python 3.13+

### Passos

```bash
poetry install
```

Depois disso, os comandos podem ser executados com `poetry run`.

## Resultado esperado

Os arquivos gerados em Markdown ficam mais enxutos do que o PDF original, priorizando apenas o texto util extraido.

Na pratica, isso torna o material mais adequado para:

- pipelines de RAG
- chunking e indexacao vetorial
- sumarizacao
- leitura automatizada por LLMs
- reducao de custo com tokens

## Testes unitarios

O projeto usa `pytest` como dependencia de desenvolvimento.

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
