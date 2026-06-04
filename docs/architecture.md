# Arquitetura

## Visao geral

O projeto segue um fluxo simples e explicito:

1. A CLI recebe os argumentos.
2. O `bootstrap` monta as dependencias.
3. O `PdfToMarkdownConverter` delega para a estrategia adequada.
4. O `PdfDocumentProcessor` valida a origem, aplica triagem de seguranca, extrai o texto e monta o Markdown.
5. O repositório persiste o resultado em disco.

## Camadas

### Entrada

- `cli.py`
- `hierarchical_batch_cli.py`

As CLIs apenas interpretam argumentos, configuram logging e traduzem erros esperados em codigos de saida.

### Composicao

- `bootstrap.py`

Centraliza a montagem das dependencias. Isso evita que uma CLI dependa da outra e reduz acoplamento acidental.

### Aplicacao

- `converter/facade.py`
- `converter/processor.py`
- `converter/strategies/`

A camada de aplicacao orquestra o caso de uso sem conhecer detalhes de interface de linha de comando.

### Dominio e transformacao

- `models.py`
- `markdown_builder.py`
- `converter/hierarchical_document_builder.py`
- `sanitizer.py`
- `validation.py`
- `security/`

Aqui ficam as regras de negocio e transformacoes de conteudo.

### Infraestrutura

- `pdf_extractor.py`
- `file_repository.py`

Esses componentes lidam com bibliotecas externas e filesystem.

## Diretrizes

- Validacoes de entrada ficam fora do repositório.
- O builder de Markdown individual gera um `body` reutilizavel para consolidacoes.
- O modo hierarquico ignora subarvores vazias e falha apenas quando a raiz inteira nao possui PDFs.
- Excecoes genericas nao devem ser engolidas nas CLIs.
