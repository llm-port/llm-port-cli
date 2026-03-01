"""Configuration file (llmport.yaml) read/write utilities.

The CLI persists its state in a YAML file located at:
  - ``$LLMPORT_CONFIG`` env var (if set)
  - ``<install_dir>/llmport.yaml``
  - ``~/.config/llmport/llmport.yaml`` (default)

The schema is intentionally flat:  top-level scalars for the common
case, with a ``dev:`` section for dev-mode specifics.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


# ── Default paths ─────────────────────────────────────────────────

_DEFAULT_CONFIG_DIR = Path.home() / ".config" / "llmport"
_DEFAULT_CONFIG_FILE = _DEFAULT_CONFIG_DIR / "llmport.yaml"

_GITHUB_ORG = "llm-port"
_REPOS = [
    "llm-port-backend",
    "llm-port-frontend",
    "llm-port-api",
    "llm-port-rag",
    "llm-port-pii",
    "llm-port-shared",
    "llm-port-dev",
    "llm-port-cli",
    ".github",
]

# Map GitHub repo name → local directory name (underscore convention)
REPO_DIR_MAP: dict[str, str] = {
    "llm-port-backend": "llm_port_backend",
    "llm-port-frontend": "llm_port_frontend",
    "llm-port-api": "llm_port_api",
    "llm-port-rag": "llm_port_rag",
    "llm-port-pii": "llm_port_pii",
    "llm-port-shared": "llm_port_shared",
    "llm-port-dev": "llm_port_dev",
    "llm-port-cli": "llm_port_cli",
    ".github": ".github",
}


@dataclass
class DevConfig:
    """Dev-mode specific configuration."""

    workspace_dir: str = ""
    clone_method: str = "https"  # "https" or "ssh"
    branch: str = "master"
    repos: list[str] = field(default_factory=lambda: list(_REPOS))


@dataclass
class LlmportConfig:
    """Top-level CLI configuration."""

    version: int = 1
    install_dir: str = ""
    compose_file: str = "docker-compose.yaml"
    compose_dev_file: str = "docker-compose.dev.yaml"
    profiles: list[str] = field(default_factory=list)
    admin_email: str = ""
    api_url: str = "http://localhost:8000"
    api_token: str = ""
    dev: DevConfig = field(default_factory=DevConfig)

    # ── Derived paths ─────────────────────────────────────────

    @property
    def install_path(self) -> Path:
        """Resolved install directory."""
        return Path(self.install_dir).expanduser().resolve() if self.install_dir else Path.cwd()

    @property
    def compose_path(self) -> Path:
        """Path to the main docker-compose file."""
        return self.install_path / self.compose_file

    @property
    def compose_dev_path(self) -> Path:
        """Path to the dev overlay docker-compose file."""
        return self.install_path / self.compose_dev_file

    @property
    def env_path(self) -> Path:
        """Path to the .env file."""
        return self.install_path / ".env"

    @property
    def dev_workspace_path(self) -> Path:
        """Resolved dev workspace directory."""
        if self.dev.workspace_dir:
            return Path(self.dev.workspace_dir).expanduser().resolve()
        return Path.cwd()


# ── Read/write ────────────────────────────────────────────────────


def config_path() -> Path:
    """Return the active config file path."""
    env = os.environ.get("LLMPORT_CONFIG")
    if env:
        return Path(env).expanduser().resolve()
    return _DEFAULT_CONFIG_FILE


def load_config() -> LlmportConfig:
    """Load the config from disk, or return defaults if missing."""
    path = config_path()
    if not path.exists():
        return LlmportConfig()
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return _from_dict(data)


def save_config(cfg: LlmportConfig) -> Path:
    """Write the config to disk.  Creates parent dirs as needed."""
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(_to_dict(cfg), default_flow_style=False, sort_keys=False), encoding="utf-8")
    return path


# ── Serialisation helpers ─────────────────────────────────────────


def _from_dict(data: dict[str, Any]) -> LlmportConfig:
    """Build a ``LlmportConfig`` from a raw dict."""
    dev_data = data.pop("dev", {}) or {}
    dev = DevConfig(**{k: v for k, v in dev_data.items() if k in DevConfig.__dataclass_fields__})
    cfg = LlmportConfig(
        **{k: v for k, v in data.items() if k in LlmportConfig.__dataclass_fields__ and k != "dev"},
        dev=dev,
    )
    return cfg


def _to_dict(cfg: LlmportConfig) -> dict[str, Any]:
    """Serialise a ``LlmportConfig`` to a plain dict for YAML."""
    from dataclasses import asdict

    return asdict(cfg)


def repo_clone_url(repo: str, *, method: str = "https") -> str:
    """Return the git clone URL for a repo in the llm-port org."""
    if method == "ssh":
        return f"git@github.com:{_GITHUB_ORG}/{repo}.git"
    return f"https://github.com/{_GITHUB_ORG}/{repo}"
