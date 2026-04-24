from pydantic import ValidationError
import typer
from rich import print
from rich.table import Table
import click

from contextforge.config import load_config, save_config
from contextforge.models import OrgConfig
from contextforge.scanner.github import list_repos
from contextforge.store import save_projects

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
    
@app.command()
def scan(token: str = typer.Option(..., prompt=True, hide_input=True)):
    """Scan your org's repos and discover services."""
    config = load_config()
    if config is None:
        print("[bold red]No config found. Run 'contextforge init' first.[/bold red]")
        raise typer.Exit(1)

    # Call list_repos, then display the results
    # Use Rich's Table for a nice output
    projects = list_repos(config.org_name, token)
    table = Table(title="Discovered Repos")
    table.add_column("Name")
    table.add_column("Language")
    table.add_column("Type")

    for project in projects:
        table.add_row(project.name, project.language or "—", project.type)

    print(table)
    save_projects(projects)