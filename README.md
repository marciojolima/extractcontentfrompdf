# ExtractContentFromPdf

Projeto em Python para extrair texto de PDFs nativos e gerar arquivos Markdown simples, leves e prontos para consumo por fluxos de busca, RAG e LLMs.

## Objetivo de negócio

O projeto existe para transformar documentos PDF em conteúdo textual mais fácil de armazenar, indexar e reutilizar em processos automatizados.

Na prática, ele ajuda a:

- reduzir ruído no conteúdo extraído
- preservar o texto relevante para consulta e recuperação
- facilitar a preparação de base documental para RAG
- diminuir custo de processamento em pipelines com LLM

## Instalação

Requisitos:

- Python 3.13+
- Poetry

Instalação:

```bash
poetry install
```

## Uso

Conversão de um único PDF:

```bash
poetry run extract-pdf caminho/arquivo.pdf
```

Conversão de um único PDF com intervalo de páginas:

```bash
poetry run extract-pdf caminho/arquivo.pdf 1 10
```

Conversão hierárquica de uma ou mais pastas raiz:

```bash
poetry run extract-pdf-hierarchical data/in/Fase01 data/in/Fase02
```

Por padrão, os arquivos Markdown são gerados em `data/out`.

Se quiser definir outro diretório de saída:

```bash
poetry run extract-pdf caminho/arquivo.pdf --output-dir resultado
```

Também é possível desativar a triagem de segurança do PDF:

```bash
poetry run extract-pdf caminho/arquivo.pdf --no-check-security
```

## Documentação técnica

Detalhes técnicos e decisões de arquitetura estão em
<a href="./docs/architecture.md">docs/architecture.md</a>.
