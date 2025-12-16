# Setup

- We work with uv. You can install it [here](https://docs.astral.sh/uv/guides/install-python/)
- Docker with docker compose. [Install instructions](https://docs.docker.com/compose/install/).

```bash
make requirements   #  Install dependencies
```

Start the development server and start building!.

```bash
make dev
```

If finished, shutdown the development server.

```bash
make dev-down
```

# Development

```bash
make dev                #  Run a local development server
make prod               #  Run a local production server
make docs               #  Run a local mkdocs server for documentation
make lint               #  Lint the code
make format             #  Format the code
make tests              #  Run unit tests
```

# Project Organization

```bash
├── docs                # A default mkdocs project; see www.mkdocs.org for details
├── docuisine           # Source code for use in this project
├── scripts/dev         # Docker-compose files for development database
├── tests               # Unit tests
├── CONTRIBUTING.md     # Project contribution guidelines and instructions
├── LICENSE             # Open-source license if one is chosen
├── Makefile            # Makefile with convenience commands like `make test` or `make format`
├── pyproject.toml      # Dependencies list and project configuration
└── README.md           # The top-level README for developers using this project
```

---
