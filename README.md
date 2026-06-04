# ExtractContentFromPdf

Projeto em Python para extrair texto de PDFs nativos e gerar arquivos Markdown simples, leves e prontos para consumo por fluxos de busca, RAG e LLMs.

## 🛠️ Tecnologias Utilizadas

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![pdfplumber](https://img.shields.io/badge/pdfplumber-extração%20de%20texto-4B5563?style=for-the-badge)
![PyPDF](https://img.shields.io/badge/PyPDF-triagem%20e%20leitura-B31B1B?style=for-the-badge)
![Poetry](https://img.shields.io/badge/Poetry-gerenciamento-1E3A8A?style=for-the-badge&logo=poetry)
![Pytest](https://img.shields.io/badge/Pytest-testes-0A9EDC?style=for-the-badge&logo=pytest)

## 🎯 Objetivo de negócio

O projeto existe para transformar documentos PDF em conteúdo textual mais fácil de armazenar, indexar e reutilizar em processos automatizados.

Na prática, ele ajuda a:

- reduzir ruído no conteúdo extraído
- preservar o texto relevante para consulta e recuperação
- facilitar a preparação de base documental para RAG
- diminuir custo de processamento em pipelines com LLM

## ⚙️ Instalação

Requisitos:

- Python 3.13+
- Poetry

Instalação:

```bash
poetry install
```

## 🚀 Uso

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

## 📚 Documentação

[Arquitetura do projeto](docs/architecture.md)
