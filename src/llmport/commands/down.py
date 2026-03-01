"""``llmport down`` — stop llm.port services."""

from __future__ import annotations

import sys

import click

from llmport.core.compose import build_context_from_config, down as compose_down
from llmport.core.console import console, success, error
from llmport.core.settings import load_config


@click.command("down")
@click.option("--volumes/--no-volumes", default=False, help="Remove named volumes declared in the compose file.")
@click.option("--remove-orphans/--no-remove-orphans", default=True, help="Remove containers for services not defined in the compose file.")
def down_cmd(*, volumes: bool, remove_orphans: bool) -> None:
    """Stop and remove llm.port containers and networks."""
    cfg = load_config()
    ctx = build_context_from_config(cfg)

    console.print("[bold cyan]Stopping llm.port services…[/bold cyan]")

    with console.status("[bold cyan]docker compose down[/bold cyan]"):
        returncode = compose_down(ctx, volumes=volumes, remove_orphans=remove_orphans)

    if returncode == 0:
        success("Services stopped.")
    else:
        error(f"docker compose down exited with code {returncode}.")
        sys.exit(returncode)
