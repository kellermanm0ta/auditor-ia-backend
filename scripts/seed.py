"""Seed database with frontend integration data via the API."""
import asyncio
import time

import httpx

INTEGRATIONS = [
    {
        "name": "GitHub Actions",
        "icon": "bi-github",
        "desc": "Execute a análise automaticamente em cada push ou pull request.",
        "status": "connected",
        "status_label": "Conectado",
        "doc_url": "#",
        "steps": [
            "Adicione o token AUDITORIA_TOKEN como secret do repositório.",
            "Crie o arquivo .github/workflows/auditoria.yml:",
        ],
        "yaml": """name: AuditorIA Analysis
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run AuditorIA
        run: |
          curl -s -X POST https://api.auditoria.dev/analyze \
            -H "Authorization: Bearer \${{ secrets.AUDITORIA_TOKEN }}" \
            -H "Content-Type: application/json" \
            -d '{"repo":"\${{ github.repository }}","ref":"\${{ github.ref }}"}'
""",
    },
    {
        "name": "GitLab CI",
        "icon": "bi-gitlab",
        "desc": "Integre a análise nos pipelines do GitLab com um job customizado.",
        "status": "disconnected",
        "status_label": "Desconectado",
        "doc_url": "#",
        "steps": [
            "Configure a variável AUDITORIA_TOKEN no CI/CD Settings do projeto.",
            "Adicione ao seu .gitlab-ci.yml:",
        ],
        "yaml": """auditoria-analysis:
  stage: test
  image: curlimages/curl:latest
  script:
    - curl -s -X POST https://api.auditoria.dev/analyze
        -H "Authorization: Bearer \$AUDITORIA_TOKEN"
        -H "Content-Type: application/json"
        -d '{"repo":"\$CI_PROJECT_PATH","ref":"\$CI_COMMIT_REF_NAME"}'
  only:
    - main
""",
    },
    {
        "name": "Jenkins",
        "icon": "bi-gear-wide-connected",
        "desc": "Adicione um stage no seu Jenkinsfile para auditar o código.",
        "status": "disconnected",
        "status_label": "Desconectado",
        "doc_url": "#",
        "steps": [
            "Instale o plugin de credenciais e adicione AUDITORIA_TOKEN.",
            "Adicione o stage ao seu Jenkinsfile:",
        ],
        "yaml": """stage('AuditorIA') {
  steps {
    script {
      sh \"\"\"
        curl -s -X POST https://api.auditoria.dev/analyze \\
          -H "Authorization: Bearer \${AUDITORIA_TOKEN}" \\
          -H "Content-Type: application/json" \\
          -d '{"repo":"\${env.GIT_URL}","ref":"\${env.BRANCH_NAME}"}'
      \"\"\"
    }
  }
}
""",
    },
    {
        "name": "Webhook Genérico",
        "icon": "bi-webhook",
        "desc": "Dispere análises de qualquer ferramenta via HTTP POST.",
        "status": "connected",
        "status_label": "Ativo",
        "doc_url": "#",
        "steps": [
            "Utilize o endpoint abaixo para disparar análises programaticamente:",
            "Exemplo com curl:",
        ],
        "yaml": """curl -X POST https://api.auditoria.dev/webhook \\
  -H "Authorization: Bearer SEU_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "repo": "https://github.com/usuario/repositorio",
    "ref": "refs/heads/main",
    "skills": ["seguranca","arquitetura","codesmell"]
  }'
""",
    },
    {
        "name": "CLI (Linha de Comando)",
        "icon": "bi-terminal",
        "desc": "Execute análises diretamente do terminal em qualquer ambiente.",
        "status": "connected",
        "status_label": "Instalado",
        "doc_url": "#",
        "steps": [
            "Instale a CLI com npm:",
            "Execute a análise:",
        ],
        "yaml": """# Instalação
npm install -g auditoria-cli

# Uso
auditoria analyze --repo . --token SEU_TOKEN
""",
    },
    {
        "name": "Slack",
        "icon": "bi-slack",
        "desc": "Receba notificações no Slack quando uma análise for concluída.",
        "status": "disconnected",
        "status_label": "Desconectado",
        "doc_url": "#",
        "steps": [
            "Crie um webhook no Slack (Incoming Webhook).",
            "Configure o webhook nas configurações da plataforma.",
        ],
        "yaml": """# Webhook URL (adicione nas configurações)
https://hooks.slack.com/services/T00/B00/xxxxxxxxx
""",
    },
]

BASE_URL = "http://localhost:8000"


async def seed():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        for integration in INTEGRATIONS:
            response = await client.post("/api/integrations", json=integration)
            if response.status_code == 201:
                print(f"  ✓ {integration['name']}")
            else:
                print(f"  ✗ {integration['name']} — {response.status_code}: {response.text}")
            time.sleep(0.05)


if __name__ == "__main__":
    print("Seeding integrations...")
    asyncio.run(seed())
    print("Done.")