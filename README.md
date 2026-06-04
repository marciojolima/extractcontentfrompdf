# ExtractContentFromPdf

Projeto em Python para extrair texto de PDFs nativos e gerar arquivos Markdown simples, leves e prontos para consumo por fluxos de busca, RAG e LLMs.

## Objetivo de negocio

O projeto existe para transformar documentos PDF em conteudo textual mais facil de armazenar, indexar e reutilizar em processos automatizados.

Na pratica, ele ajuda a:

- reduzir ruido no conteudo extraido
- preservar o texto relevante para consulta e recuperacao
- facilitar a preparacao de base documental para RAG
- diminuir custo de processamento em pipelines com LLM

## Instalacao

Requisitos:

- Python 3.13+
- Poetry

Instalacao:

```bash
poetry install
```

## Uso

Conversao de um unico PDF:

```bash
poetry run extract-pdf caminho/arquivo.pdf
```

Conversao de um unico PDF com intervalo de paginas:

```bash
poetry run extract-pdf caminho/arquivo.pdf 1 10
```

Conversao hierarquica de uma ou mais pastas raiz:

```bash
poetry run extract-pdf-hierarchical data/in/Fase01 data/in/Fase02
```

Por padrao, os arquivos Markdown sao gerados em `data/out`.

Se quiser definir outro diretorio de saida:

```bash
poetry run extract-pdf caminho/arquivo.pdf --output-dir resultado
```

Tambem e possivel desativar a triagem de seguranca do PDF:

```bash
poetry run extract-pdf caminho/arquivo.pdf --no-check-security
```

## Documentacao tecnica

Detalhes tecnicos e decisoes de arquitetura estao em `docs/architecture.md`.
