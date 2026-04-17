import typer
from rich import print

app = typer.Typer()

@app.callback()
def main():
    """ContextForge — Auto-discover your org's repos and generate AI coding context."""
    pass

@app.command()
def init():
    """Initialize ContextForge for your organization."""
    print('[bold green]Initializing ContextForge...[/bold green]')