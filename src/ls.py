import datetime
import typer
from pathlib import Path
from src.logger import command_log


def command_ls(path: str = ".", met: bool = False):
    try:
        a = Path(path).resolve()
        if not a.exists():
            typer.echo(f"ls: '{path}': No such file or directory")
            command_log(f"ls {path}", False, "No such file or directory")
            return

        spisok = list(a.iterdir()) #список папок и файлов
        if met:
            for i in sorted(spisok):
                k = i.stat() #метаданные
                size = k.st_size
                hour = datetime.datetime.fromtimestamp(k.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                prava = oct(k.st_mode)[-3:] #права доступа
                typer.echo(f"{i.name:20}\t{size:>10}\t{hour:>19}\t{prava:>4}")
        else:
            for j in sorted(spisok):
                typer.echo(j.name)
        command_log(f"ls {path}" + ("-l" if met else ""))

    except Exception as e:
        typer.echo(f"ls: error: {e}")
        command_log(f"ls {path}", False, str(e))
