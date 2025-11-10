import re
import typer
from pathlib import Path
from src.logger import command_log

def command_grep(stroka: str, path: str, r: bool = False, ign: bool = False):
    try:
        s = Path(path)
        fl = re.IGNORECASE if ign else 0 #устанавливает флаг игнорирования регистра, если ign=True
        regular_expression = re.compile(stroka, fl) #компилирует строку поиска в объект регулярного выражения

        if not s.exists():
            typer.echo(f"grep: '{path}': No such file or directory")
            command_log(f"grep {stroka} {path}", False, "No such file or directory")
            return

        def search(p): #функция для поиска в одном файле
            try:
                with p.open('r', encoding='utf-8', errors='ignore') as f:
                    for num, line in enumerate(f, 1):
                        if regular_expression.search(line):
                            typer.echo(f"{p}:{num}: {line.strip()}")
            except Exception:
                pass #игнорирует ошибки
        if s.is_file():
            search(s) #если файл, то ищем только в нем
        elif r:
            for p in s.rglob('*'): #рекурсивно обходит все папки и файлы
                if p.is_file(): #является ли текущих элемент фалом
                    search(p) #поиск в каждом файле
        else:
            for i in s.iterdir(): #если путь - директория
                if i.is_file():
                    search(i)


        log_grep = f"grep {stroka} {path}"
        if r:
            log_grep += " -r"
        if ign:
            log_grep += " -i"
        command_log(log_grep)

    except Exception as e:
        typer.echo(f"grep: error: {e}")
        command_log(f"grep {stroka} {path}", False, str(e))
