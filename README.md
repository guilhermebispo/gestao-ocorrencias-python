# Gestão de Ocorrências

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Angular](https://img.shields.io/badge/Angular-19-DD0031?logo=angular)](https://angular.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://www.docker.com/)

Sistema fullstack para gestão de ocorrências, com **FastAPI + Angular + PostgreSQL**, rodando em containers via **Docker Compose** ou diretamente no ambiente local.

---

## 🚀 Tecnologias
- **Backend:** Python 3.12, FastAPI, SQLAlchemy, JWT, Passlib, Swagger/OpenAPI  
- **Frontend:** Angular 19, Angular Material, ngx-toastr, ngx-charts  
- **Banco:** PostgreSQL 16  
- **Infra:** Docker, Docker Compose, Nginx  

---

## ⚙️ Como Rodar

### 🔹 Opção 1: Com Docker (recomendado)

#### Pré-requisitos
- [Docker](https://docs.docker.com/get-docker/)  
- [Docker Compose](https://docs.docker.com/compose/)  

#### Passos
```bash
# clonar repositório
git clone https://github.com/seu-usuario/gestao-ocorrencias.git
cd gestao-ocorrencias

# subir os containers
docker compose up -d --build
```

---

### 🔹 Opção 2: Localmente (sem Docker)

#### Pré-requisitos
- [Python 3.12](https://www.python.org/downloads/)  
- [Node.js](https://nodejs.org/)  
- Banco de dados PostgreSQL rodando localmente

#### Backend (FastAPI)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# exporte as variáveis de ambiente se necessário
export DATABASE_URL="postgresql+psycopg://incidents_user:incidents_pass@localhost:5434/incidents_db"
python scripts/run_migrations.py

uvicorn app.main:app --reload --port 8080
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

---

## 🌐 Endpoints

- **Frontend:** http://localhost:4200  
- **Backend:** http://localhost:8080  
- **Swagger UI:** http://localhost:8080/swagger-ui  
- **Banco de Dados:** postgres://localhost:5434/incidents_db  

---

## 👤 Usuário Padrão

O sistema já vem com um usuário administrador para acesso inicial:

- **Usuário:** matheus@incidents.com  
- **Senha:** 123456
