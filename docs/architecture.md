# Arquitetura

## Visao geral

O projeto segue um fluxo simples e explicito:

1. O entrypoint recebe os argumentos.
2. O `bootstrap` monta as dependencias.
3. O `PdfToMarkdownConverter` delega para a estrategia adequada.
4. O `PdfDocumentProcessor` valida a origem, aplica triagem de seguranca, extrai o texto e monta o Markdown.
5. O repositório persiste o resultado em disco.

## Camadas

### Entrypoints

- `entrypoints/single.py`
- `entrypoints/batch.py`

Os entrypoints apenas interpretam argumentos, configuram logging e traduzem erros esperados em codigos de saida.

### Composicao

- `entrypoints/bootstrap.py`

Centraliza a montagem das dependencias. Isso evita que um entrypoint dependa do outro e reduz acoplamento acidental.

O `entrypoints/bootstrap.py` e o ponto primario de composicao da aplicacao.

Os pontos primarios de execucao sao:

- `entrypoints/single.py`
- `entrypoints/batch.py`

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
- O modo batch ignora subarvores vazias e falha apenas quando a raiz inteira nao possui PDFs.
- Excecoes genericas nao devem ser engolidas nos entrypoints.
