import zipfile
import typer
from pathlib import Path
from src.logger import command_log

def command_unzip(archive: str):
    try:
        a_path = Path(archive)

        if not a_path.exists():
            typer.echo(f"unzip: '{archive}': No such file or directory")
            command_log(f"unzip {archive}", False, "No such file or directory")
            return

        if not a_path.is_file():
            typer.echo(f"unzip: '{archive}': Is a directory")
            command_log(f"unzip {archive}", False, "Is a directory")
            return

        if not zipfile.is_zipfile(a_path):
            typer.echo(f"unzip: '{archive}': cannot find or open")
            command_log(f"unzip {archive}", False, "cannot find or open")
            return

        with zipfile.ZipFile(a_path, 'r') as f:
            f.extractall()

        typer.echo(f"Extracted archive: {archive}")
        command_log(f"unzip {archive}")

    except Exception as e:
        typer.echo(f"unzip: error: {e}")
        command_log(f"unzip {archive}", False, str(e))
