import os
import typer
from pathlib import Path
from src.logger import command_log

def command_cd(a: str):
    try:
        if not a or a == "~":
            new = Path.home()
        elif a == "..":
            new = Path.cwd().parent
        else:
            new = Path(a).resolve()

        if not os.access(new, os.X_OK):
            typer.echo(f"cd: {a}: Permission denied")

        if not new.exists():
            typer.echo(f"cd: {a}: No such directory")
            command_log(f"cd {a}", False, "No such directory")
            return

        if not new.is_dir():
            typer.echo(f"cd: {a}: Is not a directory")
            command_log(f"cd {a}", False, "Is not a directory")
            return

        os.chdir(new)
        command_log(f"cd {a}")

    except Exception as e:
        typer.echo(f"cd: error: {e}")
        command_log(f"cd {a}", False, str(e))
