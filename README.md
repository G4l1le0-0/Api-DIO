# Criando Uma API com FastAPI Utilizando TDD - Resolução do Desafio Final DIO

Este projeto é um fork da `Store API`, desenvolvido como parte da resolução de um desafio prático da plataforma **DIO (Digital Innovation One)**. O foco principal deste repositório é a implementação das funcionalidades solicitadas no desafio, aprimorando uma API construída com FastAPI e TDD.

## O Desafio Final Resolvido

O objetivo foi implementar uma série de melhorias e novas funcionalidades na API existente. Abaixo estão os detalhes de cada requisito do desafio e como foram solucionados:

### 1. Create: Tratamento de Exceções na Criação
- **Requisito:** Mapear uma exceção para erros durante a inserção de dados e capturá-la na controller para retornar uma mensagem amigável.
- **Solução Implementada:**
    - Foi criada uma exceção customizada `InsertionError`.
    - O `ProductUsecase` agora utiliza um bloco `try...except` que lança essa exceção caso ocorra um erro do MongoDB.
    - Na aplicação principal (`main.py`), foi adicionado um `@app.exception_handler` que captura a `InsertionError` e retorna uma resposta `HTTP 422 Unprocessable Entity` com uma mensagem de erro clara, evitando que a aplicação quebre com um erro 500 genérico.

### 2. Update: Lógica de Atualização Aprimorada
- **Requisito:** Modificar o método de atualização para retornar `Not Found` se o produto não existir e garantir que o campo `updated_at` seja preenchido com a data e hora atuais.
- **Solução Implementada:**
    - **Verificação de Existência:** Antes de tentar atualizar, o método `update` agora verifica se o produto existe no banco de dados. Se não existir, a API retorna um erro `HTTP 404 Not Found`.
    - **Timestamp Automático:** No schema `ProductUpdate`, foi adicionado o campo `updated_at` com um `default_factory` do Pydantic. Isso garante que, a cada modificação, o campo seja preenchido automaticamente com o timestamp UTC atual.

### 3. Filtros: Filtragem de Produtos por Preço
- **Requisito:** Implementar um filtro na rota de listagem para buscar produtos dentro de uma faixa de preço (ex: `price > 5000 and price < 8000`).
- **Solução Implementada:**
    - O método `query` do `ProductUsecase` foi modificado para aceitar os parâmetros opcionais `price_min` e `price_max`.
    - A lógica constrói uma consulta dinâmica para o MongoDB utilizando os operadores `$gt` (maior que) e `$lt` (menor que), permitindo uma filtragem eficiente por faixa de preço diretamente na URL, como por exemplo: `/products/?price_min=5000&price_max=8000`.

## Tecnologias Utilizadas
- **Framework:** FastAPI
- **Banco de Dados:** MongoDB (com `Motor` para operações assíncronas)
- **Validação de Dados:** Pydantic
- **Testes:** Pytest
- **Gerenciamento de Dependências:** Poetry
- **Ambiente:** Pyenv

## Como Preparar o Ambiente

O projeto utiliza `Pyenv` para gerenciamento da versão do Python e `Poetry` para gerenciamento de dependências e do ambiente virtual.

1.  **Clone o repositório:**
    ```bash
    git clone [URL-DO-SEU-FORK]
    cd [NOME-DO-SEU-REPOSITORIO]
    ```

2.  **Instale a versão correta do Python (se necessário):**
    ```bash
    pyenv install 3.11.8 
    pyenv local 3.11.8
    ```

3.  **Instale as dependências com o Poetry:**
    ```bash
    poetry install
    ```

4.  **Execute a aplicação (usando o servidor Uvicorn):**
    ```bash
    poetry run uvicorn store.main:app --reload
    ```

## Projeto Original
Este fork foi baseado no projeto `TDD Project / Store API`, cujo foco principal era o aprendizado de Desenvolvimento Orientado a Testes (TDD). A estrutura inicial e os conceitos de TDD foram mantidos.
