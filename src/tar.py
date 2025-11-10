import tarfile
import typer
from pathlib import Path
from src.logger import command_log

def command_tar(k: str, archive: str):
    try:
        a_path = Path(k)
        if not a_path.exists():
            typer.echo(f"tar: '{k}': No such file or directory")
            command_log(f"tar {k} {archive}", False, "No such file or directory")
            return

        if not a_path.is_dir():
            typer.echo(f"tar: '{k}': Not a directory")
            command_log(f"tar {k} {archive}", False, "Not a directory")
            return

        with tarfile.open(archive, "w:gz") as f:
            f.add(k, arcname=a_path.name)

        archive_size = Path(archive).stat().st_size
        typer.echo(f"Create zip archive:'{archive}', size: {archive_size} bytes")
        command_log(f"zip {k} {archive}")

        typer.echo(f"Created tag.gz archive: {archive}")
        command_log(f"tar {k} {archive}")

    except Exception as e:
        typer.echo(f"tar: error: {e}")
        command_log(f"tar {k} {archive}", False, str(e))
