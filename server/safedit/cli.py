import typer

from .main import start_server

app = typer.Typer()


@app.command()
def main(path: str, tabs: int = 1, port: int = None):
    """Start safedit server and open N clients."""
    start_server(path, tabs, port)


if __name__ == "__main__":
    app()
