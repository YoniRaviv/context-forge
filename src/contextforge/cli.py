import typer
import click
from pydantic import ValidationError
from rich import print
from rich.table import Table
from rich.panel import Panel

from contextforge.config import load_config, save_config
from contextforge.models import OrgConfig
from contextforge.scanner.github import list_repos
from contextforge.store import load_projects, save_projects
from contextforge.utils import create_table

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
    table = create_table(
        title="Discoverd Projects", 
        columns=["Name", "Language", "Type"], 
        rows=[[p.name, p.language or "—", p.type] for p in projects]
    )

    print(table)
    save_projects(projects, config.org_name)

@app.command()
def show(project_name: str = typer.Argument(None)):
    """Show discovered projects. Optionally pass a project name for details."""
    config = load_config()
    projects = load_projects(config.org_name)

    if not projects:
        print("[bold yellow]No projects found. Run 'contextforge scan' first.[/bold yellow]")
        raise typer.Exit(1)

    if project_name:
        matches = [p for p in projects if p.name == project_name]
        if not matches:
            print(f"[bold red]Project '{project_name}' not found[/bold red]")
            raise typer.Exit(1)
        project = matches[0]
        print(Panel(
            f"Language: {project.language or '—'}\n"
            f"Type: {project.type}\n"
            f"URL: {project.repo_url}",
            title=project.name
        ))
    else:
        table = create_table(
            title="Projects",
            columns=["Name", "Language", "Type"],
            rows=[[p.name, p.language or "—", p.type] for p in projects]
        )
        print(table)