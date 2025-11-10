import shutil
import typer
from pathlib import Path
from src.logger import command_log
from src.history_functions import add_history
import os

def command_mv(object: str, direction: str):
    try:
        o = Path(object)
        d = Path(direction)

        if not os.access(o, os.R_OK):
            typer.echo(f"mv: cannot move '{object}' to '{d}': Permission denied")
            command_log(f"mv {object} {d}", False, "Permission denied")

        if not o.exists():
            typer.echo(f"mv: '{object}': No such file or directory")
            command_log(f"mv {object} {direction}", False, "No such file or directory")
            return

        shutil.move(str(o), str(d))
        typer.echo(f"Moved '{object}' to '{direction}'")
        c_mv = f"mv {object} {direction}"
        add_history(c_mv)
        command_log(c_mv)

    except Exception as e:
        typer.echo(f"mv: error: {e}")
        command_log(f"mv {object} {direction}", False, str(e))
