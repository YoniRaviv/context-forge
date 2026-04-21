from pydantic import ValidationError
import typer
from rich import print
import click

from contextforge.config import save_config
from contextforge.models import OrgConfig

app = typer.Typer()

@app.callback()
def main():
    """ContextForge — Auto-discover your org's repos and generate AI coding context."""
    pass

@app.command()
def init():
    """Initialize ContextForge to get data"""
    print('[bold green]Initializing ContextForge...[/bold green]')

    name = typer.prompt("What is your org name?", type=str)
    provider = typer.prompt("What is your provider (github/gitlab)?", type=click.Choice(["github", "gitlab"]))
    agent = typer.prompt("What do you use as coding agent? (CC, Cursor, Codex etc)", type=click.Choice(["claude-code", "cursor", "generic"]), default="claude-code")
    default_branch = typer.prompt("What is your default branch?", type=str, default="main")

    try:
        config = OrgConfig(provider=provider, org_name=name, target_agent=agent, default_branch=default_branch)
        save_config(config)
        print(f'[bold green]✓ Configuration saved for {name}[/bold green]')
        print('Run [bold]contextforge scan[/bold] to discover your repos.')
    except ValidationError as e:
        typer.echo(f"Invalid configuration: {e}")
        raise typer.Exit(1)