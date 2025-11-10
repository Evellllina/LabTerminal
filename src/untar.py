import tarfile
import typer
from pathlib import Path
from src.logger import command_log

def command_untar(archive: str):
    try:
        a_path = Path(archive)
        if not a_path.exists():
            typer.echo(f"untar: '{archive}': No such file or directory")
            command_log(f"untar {archive}", False, "No such file or directory")
            return

        if not a_path.is_file():
            typer.echo(f"untar: '{archive}': Is a directory")
            command_log(f"untar {archive}", False, "Is a directory")
            return

        with tarfile.open(a_path, "r:gz") as f:
            f.extractall()

        typer.echo(f"Extracted archive: {archive}")
        command_log(f"untar {archive}")

    except Exception as e:
        typer.echo(f"untar: error: {e}")
        command_log(f"untar {archive}", False, str(e))
