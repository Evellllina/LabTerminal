import zipfile
import typer
from pathlib import Path
from src.logger import command_log

def command_zip(s: str, archive: str):
    try:
        a_path = Path(s)
        if not a_path.exists():
            typer.echo(f"zip: '{s}': No such file or directory")
            command_log(f"zip {s} {archive}", False, "No such file or directory")
            return

        if not a_path.is_dir():
            typer.echo(f"zip: '{s}': Not a directory")
            command_log(f"zip {s} {archive}", False, "Not a directory")
            return

        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as f:
            for i in a_path.rglob('*'):
                if i.is_file():
                    name = i.relative_to(a_path)
                    f.write(i, name)

        archive_size = Path(archive).stat().st_size
        typer.echo(f"Create zip archive:'{archive}', size: {archive_size} bytes")
        typer.echo(f"Create zip archive: {archive}")
        command_log(f"zip {s} {archive}")

    except Exception as e:
        typer.echo(f"zip: error: {e}")
        command_log(f"zip {s} {archive}", False, str(e))
