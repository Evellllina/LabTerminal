import shutil
import typer
from pathlib import Path
from src.logger import command_log
from src.history_functions import add_history

def command_cp(object: str, direction: str, f: bool = False):
    try:
        o = Path(object)
        d = Path(direction)
        if not o.exists():
            typer.echo(f"cp: '{object}': No such file or directory")
            command_log(f"cp {object} {direction}", False, "No such file or directory")
            return

        if o.is_dir():
            if not f:
                typer.echo(f"cp: -r not specified; omitting directory '{object}'")
                command_log(f"cp {object} {direction}", False, "Is a directory; -r not specified")
                return

        if o.is_file():
            shutil.copy2(o, d)
            mes = f"Copied '{object}' to '{direction}'"
        else:
            shutil.copytree(o, d)
            mes = f"Copied '{object}' to '{direction}'"
        typer.echo(mes)

        v = f"cp {object} {direction}"
        if f:
            v += "-r"
        add_history(v)
        command_log(v)

    except Exception as e:
        typer.echo(f"cp: error: {e}")
        command_log(f"cp {object} {direction}", False, str(e))
