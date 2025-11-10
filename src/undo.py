import shutil
import typer
from pathlib import Path
from src.logger import command_log
from src.history_functions import get_command
from src.history_functions import remove_command

def command_undo():
    try:
        a = get_command()
        if not a:
            typer.echo("undo: no commands")
            return

        last_a = a["command"] #извлекает текстовое представление команды
        argyment = last_a.split() #разбивает команду на отдельные части
        if last_a.startswith("cp") and len(argyment) >= 3:
            direction = argyment[-1] #последний аргумень
            d = Path(direction)
            if d.exists():
                if d.is_file():
                    d.unlink() #удаляет файл
                else:
                    shutil.rmtree(d) #рекурсивно удаляет директорию со всем содержимым
                typer.echo(f"Undo 'cp': removed {direction}")

        elif last_a.startswith("rm") and len(argyment) >= 2:
            last_argyment = argyment[-1]
            argyment_name = Path(last_argyment).name #извлекает имя файла, без пути
            trash_dir = Path(".trash")
            trash_files = list(trash_dir.glob(f"{argyment_name}_*")) #оригинальный формат
            if trash_files:
                last_trash = max(trash_files, key=lambda x: x.stat().st_ctime) #находит самый новый файл по времени
                shutil.move(str(last_trash), last_argyment) #перемещает файл в исходное положение
                typer.echo(f"Undo rm: restored {last_argyment}")
            else:
                typer.echo(f"undo: could not find '{last_argyment}' in trash")

        elif last_a.startswith("mv") and len(argyment) >= 3:
            object, direction = argyment[-2], argyment[-1]
            o, dir = Path(object), Path(direction)
            if dir.exists():
                shutil.move(str(dir), str(o))
                typer.echo(f"Undo 'mv': moved back to {object}")
        remove_command()
        command_log("undo")

    except Exception as e:
        typer.echo(f"undo: error: {e}")
        command_log("undo", False, str(e))
