# 🎬 API REST de Filmes com FastAPI

Este projeto é uma API RESTful construída com FastAPI para gerenciar uma lista de filmes. Ele inclui funcionalidades de CRUD (Create, Read, Update, Delete) com integração a um banco de dados SQLite, e pode ser testado facilmente com Swagger ou Postman.

## 🚀 Tecnologias utilizadas

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Swagger UI (gerado automaticamente)
- Testes com Postman ou Insomnia

## 📁 Funcionalidades da API

| Método | Endpoint         | Descrição                 |
|--------|------------------|---------------------------|
| POST   | `/filmes/`       | Cadastrar novo filme      |
| GET    | `/filmes/`       | Listar todos os filmes    |
| GET    | `/filmes/{id}`   | Buscar filme por ID       |
| PUT    | `/filmes/{id}`   | Atualizar dados do filme  |
| DELETE | `/filmes/{id}`   | Remover filme do sistema  |

## ▶️ Como executar o projeto

```bash
# Clone o repositório
git clone https://github.com/seuusuario/api-filmes-fastapi.git
cd api-filmes-fastapi

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Rode a aplicação
uvicorn main:app --reload
