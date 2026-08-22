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

> **Payload**: todos os endpoints da API aceitam e retornam **camelCase** (ex: `statusLabel`, `docUrl`, `createdAt`).

## Seed automático

Na primeira inicialização do Docker Compose, o script `scripts/init.sql` é executado automaticamente pelo PostgreSQL, populando o banco com dados padrão:

| Tabela | Registros seedados |
|---|---|
| `integrations` | GitHub Actions, GitLab CI, Jenkins, Webhook, CLI, Slack |
| `skills` | Segurança, Arquitetura, Code Smell, Desempenho, Dependências |
| `output_formats` | Markdown, JSON, HTML, PDF |
| `history` | 5 análises de exemplo |
| `config` | Configuração inicial (modo `PARALELO`, markdown, 3 skills habilitadas) |

Para resetar o banco e recomeçar do zero:

```bash
docker compose down -v
docker compose up -d
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
| `GET` | `/api/skills` | Listar skills |
| `GET` | `/api/skills/{id}` | Buscar skill |
| `POST` | `/api/skills` | Criar skill |
| `PUT` | `/api/skills/{id}` | Atualizar skill |
| `DELETE` | `/api/skills/{id}` | Remover skill |
| `GET` | `/api/output-formats` | Listar formatos de saída |
| `GET` | `/api/output-formats/{id}` | Buscar formato |
| `POST` | `/api/output-formats` | Criar formato |
| `PUT` | `/api/output-formats/{id}` | Atualizar formato |
| `DELETE` | `/api/output-formats/{id}` | Remover formato |
| `GET` | `/api/history` | Listar histórico |
| `GET` | `/api/history/{id}` | Buscar item do histórico |
| `POST` | `/api/history` | Criar item no histórico |
| `PUT` | `/api/history/{id}` | Atualizar item |
| `DELETE` | `/api/history/{id}` | Remover item |
| `GET` | `/api/config` | Obter configuração |
| `PUT` | `/api/config` | Atualizar configuração |

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
| `app/api/` | Rotas por entidade (`integration_routes`, `skill_routes`, `output_format_routes`, `history_routes`, `config_routes`) |
| `app/core/` | Configuração via pydantic-settings (`settings.py`) |
| `app/db/` | Engine, sessão SQLAlchemy e dependência `get_db` |
| `app/models/` | Modelos ORM (`Integration`, `Skill`, `OutputFormat`, `History`, `Config`) |
| `app/schemas/` | Schemas Pydantic de request/response |
| `app/services/` | Lógica de negócio (CRUD com DB) |
| `scripts/` | Script de inicialização do banco (`init.sql`) |
| `tests/` | Testes com pytest + httpx ASGITransport |

> Nota: `/api/config` é um singleton (sempre `id=1`). As tabelas são criadas automaticamente na inicialização da aplicação via `Base.metadata.create_all` (fallback quando roda sem Docker).