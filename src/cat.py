import typer
from pathlib import Path
from src.logger import command_log
import os

def command_cat(c: str):
    try:
        path = Path(c)
        if path.is_dir():
            typer.echo(f"cat: {c}: Is a directory")
            command_log(f"cat {c}", False, "Is a directory")
            return

        if not path.exists():
            typer.echo(f"cat: {c}:  No such file or directory")
            command_log(f"cat {c}", False, " No such file or directory")
            return

        if not os.access(c, os.R_OK):
            typer.echo(f"cat: {c}, Permission denied")
            command_log(f"cat {c}", False, "Permission denied ")
            return

        with path.open('r', encoding='utf-8') as k:
            typer.echo(k.read())
        command_log(f"cat {c}")

    except Exception as e:
        typer.echo(f"cat: error: {e}")
        command_log(f"cat {c}", False, str(e))
