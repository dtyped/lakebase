# Lakebase
This repository is a cookiecutter-style template repository for getting started with Lakebase Autoscaling. This repo provides a minimal structure for setting up Lakebase (Neon-powered, serverless Postgres) with modern Python tooling.

This repository is designed to help you to:
- spin up a Lakebase-ready project quickly
- start with a clean, structured Python project layout
- deploy using GitHub Actions
- Use uv for fast dependency and environment management

Think of it as a starting point — not a framework.
Clone it, adapt it, ship from it.

# Project Structure
```
lakebase/
├── .github/workflows/  # CI/CD (Lakebase deployment)
├── lakebase/           # Core application package
│   ├── cli.py
│   ├── project.py
│   └── __init__.py
├── metadata/           # Environment configs (dev / prod)
├── pyproject.toml      # Project configuration
└── README.md
```

# Getting Started

```
uv venv
uv sync
uv run lakebase-deploy --metadata metadata/dev.yml    
```