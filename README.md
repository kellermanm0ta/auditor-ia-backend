# AuditorIA Backend

API backend do AuditorIA, um sistema de auditoria inteligente.

## Pré-requisitos

- **Docker** 24+ e **Docker Compose** v2.23+
- **Python** 3.11+ (apenas para desenvolvimento fora do container)

## Setup com Docker (recomendado)

```bash
# 1. Configure as variáveis de ambiente
cp .env.example .env

# 2. Suba o PostgreSQL
docker compose up -d

# 3. Instale as dependências Python
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows (cmd)
.venv\Scripts\activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install -e ".[dev]"

# 4. Rode o servidor
uvicorn app.main:app --reload
```

> O Docker Compose lê automaticamente as variáveis do arquivo `.env`.  
> As credenciais do banco (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`) vêm deste arquivo e não ficam hardcoded no `docker-compose.yml`.

### Docker Compose — versões compatíveis

| Plataforma | Docker Engine | Docker Compose |
|-----------|---------------|----------------|
| Linux     | 24+           | v2.23+ (plugin) |
| Windows   | 24+ (Docker Desktop) | v2.23+ (embutido) |
| macOS     | 24+ (Docker Desktop) | v2.23+ (embutido) |

Verifique a versão instalada:

```bash
docker --version       # Docker version 24.x.x
docker compose version # Docker Compose version v2.23.x
```

> **Nota**: use `docker compose` (sem hífen, plugin) — não `docker-compose`.

## Setup manual (sem Docker)

```bash
cp .env.example .env

# Certifique-se de ter um PostgreSQL rodando em localhost:5432
# As credenciais devem bater com as do .env

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## Uso

```bash
# Com o PostgreSQL rodando (via Docker ou manualmente)
uvicorn app.main:app --reload
```

Acesse `http://localhost:8000/docs` para a documentação interativa (Swagger).

### Seed de dados

Para popular o banco com as integrações do frontend (GitHub Actions, GitLab CI, Jenkins, etc.):

```bash
python scripts/seed.py
```

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/health` | Health check |
| `GET` | `/api/integrations` | Listar integrações |
| `GET` | `/api/integrations/{id}` | Buscar integração |
| `POST` | `/api/integrations` | Criar integração |
| `PUT` | `/api/integrations/{id}` | Atualizar integração |
| `DELETE` | `/api/integrations/{id}` | Remover integração |

## Testes

```bash
pytest
```

## Lint e formatação

```bash
ruff check .
ruff format --check .
```

## Projeto

| Diretório | Finalidade |
|-----------|------------|
| `app/main.py` | Criação da aplicação FastAPI + criação automática das tabelas |
| `app/api/` | Rotas (prefixo `/api`) |
| `app/core/` | Configuração via pydantic-settings |
| `app/db/` | Engine, sessão SQLAlchemy e dependência `get_db` |
| `app/models/` | Modelos ORM (`Integration`) |
| `app/schemas/` | Schemas Pydantic de request/response |
| `app/services/` | Lógica de negócio (integrações com DB, items em memória) |
| `scripts/` | Scripts utilitários (`seed.py`) |
| `tests/` | Testes com pytest + httpx ASGITransport |

> Nota: Migrations do Alembic ainda não foram inicializadas. As tabelas são criadas automaticamente na inicialização da aplicação via `Base.metadata.create_all`.