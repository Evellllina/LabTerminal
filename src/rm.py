import datetime
import shutil
import typer
from pathlib import Path
from src.logger import command_log
from src.history_functions import add_history

def command_rm(object: str, f: bool = False):
    try:
        a = Path(object)
        if not a.exists():
            typer.echo(f"rm: cannot remove '{object}': No such file or directory")
            command_log(f"rm {object}", False, "No such file or directory")
            return

        dir_c = Path.cwd() #возвращает текущую рабочую директорию
        if ((a.resolve() == Path("/")) or (a.resolve() == dir_c.parent) or (str(a.resolve()) == str(dir_c.root))):
            typer.echo("rm: cannot remove directory")
            command_log(f"rm {object}", False, "Cannot remove directory")
            return

        if a.is_dir():
            if not f:
                typer.echo(f"rm: cannot remove '{object}': Is a directory")
                command_log(f"rm {object}", False, "Is a directory")
                return

            confirm = typer.confirm(f"Are you sure you want to recursively delete '{a}'?")
            if not confirm:
                typer.echo("Deletion cancelled")
                return

        trash_dir = Path(".trash") #представляет путь к папке
        trash_dir.mkdir(exist_ok=True) #создает директорию
        time_per = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') #временная метка
        trash_name = f"{a.name}_{time_per}" #создание имени корзины
        trash_ob = trash_dir / trash_name #создание полного пути
        shutil.move(str(a.resolve()), str(trash_ob.resolve())) #перемещает папку/файл в корзину
        typer.echo(f"Moved '{object}' to trash")
        v = f"rm {object}"
        if f:
            v += "-r"
        add_history(v)
        command_log(v)

    except Exception as e:
        typer.echo(f"rm: error: {e}")
        command_log(f"rm {object}", False, str(e))
