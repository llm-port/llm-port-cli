# llmport CLI

> Command-line installer and management tool for the **llm.port** platform.

## Features

- **One-command install** — `llmport up` starts the full stack
- **System diagnostics** — `llmport doctor` verifies prerequisites
- **Module management** — enable/disable RAG, PII, auth modules
- **Dev mode** — `llmport dev init` bootstraps a full development workspace
- **Cross-platform** — Windows, macOS, Linux

## Quick Start

```bash
# Install with pip or uv
uv tool install llmport-cli

# Check system readiness
llmport doctor

# Start the platform
llmport up

# Check service status
llmport status
```

## Developer Workflow

```bash
# Clone all repos and set up workspace
llmport dev init --workspace ~/projects/llm-port

# Start dev servers (backend + worker + frontend)
llmport dev up

# Check dev environment status
llmport dev status
```

## Command Reference

| Command               | Description                                |
| --------------------- | ------------------------------------------ |
| `llmport version`     | Print version and runtime info             |
| `llmport doctor`      | Run system health checks                   |
| `llmport status`      | Show running service status                |
| `llmport up`          | Start llm.port services                    |
| `llmport down`        | Stop and remove containers                 |
| `llmport logs`        | Stream container logs                      |
| `llmport config show` | Display current configuration              |
| `llmport config set`  | Set a configuration value                  |
| `llmport config init` | Create a default config file               |
| `llmport module list` | List available modules                     |
| `llmport module enable`  | Enable a module (rag, pii, auth)        |
| `llmport module disable` | Disable a module                        |
| `llmport dev init`    | Bootstrap development workspace            |
| `llmport dev up`      | Start dev servers                          |
| `llmport dev status`  | Show dev workspace status                  |

## Configuration

Configuration is stored in `~/.config/llmport/llmport.yaml`:

```yaml
install_dir: /opt/llm-port/shared
profiles:
  - rag
  - pii
admin_email: admin@example.com
dev:
  workspace_dir: ~/projects/llm-port
  clone_method: https
  branch: main
```

Override the config path with `LLMPORT_CONFIG` environment variable.

## Requirements

- Python ≥ 3.12
- Docker with Compose v2
- Git (for dev mode)
- uv, Node.js, npm (for dev mode)

## License

Apache License 2.0 — see [LICENSE](LICENSE).
