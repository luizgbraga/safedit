import typer

from .main import start_server

app = typer.Typer()


@app.command()
def main(path: str, port: int = None):
    """Start safedit server"""
    start_server(path, port)


if __name__ == "__main__":
    app()
