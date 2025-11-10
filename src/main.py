import sys
import typer
from pathlib import Path
from src.history_functions import history_i
from src.ls import command_ls
from src.cd import command_cd
from src.cat import command_cat
from src.cp import command_cp
from src.mv import command_mv
from src.rm import command_rm
from src.zip import command_zip
from src.unzip import command_unzip
from src.tar import command_tar
from src.untar import command_untar
from src.grep import command_grep
from src.history import command_history
from src.undo import command_undo

app = typer.Typer()

def init_shell():
    history_i()

@app.command()
def ls(
        path: str = typer.Argument(None, help="Path to list"),
        detailed: bool = typer.Option(False, "-l", help="Detailed listing")
):
    if path in ["-l"]:
        path = "."
        detailed = True

    if path is None:
        path = "."
    command_ls(path, detailed)

@app.command()
def cd(a: str):
    command_cd(a)

@app.command()
def cat(c: str):
    command_cat(c)

@app.command()
def cp(object: str, direction: str, f: bool = typer.Option(False, "--r", "-r")):
    command_cp(object, direction, f)

@app.command()
def mv(object: str, direction: str):
    command_mv(object, direction)

@app.command()
def rm(object: str, f: bool = typer.Option(False, "--r", "-r")):
    command_rm(object, f)

@app.command()
def zip(s: str, archive: str):
    command_zip(s, archive)

@app.command()
def unzip(archive: str):
    command_unzip(archive)

@app.command()
def tar(k: str, archive: str):
    command_tar(k, archive)

@app.command()
def untar(archive: str):
    command_untar(archive)

@app.command()
def grep(stroka: str, path: str,
         r: bool = typer.Option(False, "-r"),
         ign: bool = typer.Option(False, "-i")):
    command_grep(stroka, path, r, ign)

@app.command()
def history(limit: int = 15):
    command_history(limit)

@app.command()
def undo():
    command_undo()

@app.command()
def interactive():
    init_shell()
    typer.echo("My Terminal :) Use 'exit' to close the program")

    while True:
        try:
            a = input(f"\n{Path.cwd()}$ ").strip()
            if not a:
                continue

            if a.lower() in ['exit']:
                typer.echo("Good!")
                break
            elif a.lower() == 'ls --help':
                help()
            else:
                shell_command(a)

        except KeyboardInterrupt:
            typer.echo("Good!")
            break
        except Exception as e:
            typer.echo(f"Error: {e}")

def help():
    commands = [
        "ls [path] [-l]                      - List files/directories",
        "cd <a>                              - Change directory",
        "cat <file>                          - Show file content",
        "cp <object> <direction> [-r]        - Copy files/directories",
        "mv <object> <direction>             - Move files",
        "rm <object> [-r]                    - Remove files/directories",
        "zip <s> <archive>                   - Create zip archive",
        "unzip <archive>                     - Extract zip archive",
        "tar <s> <archive>                   - Create tar.gz archive",
        "untar <archive>                     - Extract tar.gz archive",
        "grep <stroka> <path>                - Search in files",
        "history                             - Show command history",
        "undo                                - Undo last command",
        "exit                                - Exit shell"
    ]
    typer.echo("Available сommands:")
    for i in commands:
        typer.echo(f"  {i}")

def shell_command(command: str):
    k = command.split()
    if not k:
        return

    c, ar = k[0], k[1:]

    try:
        if c == "ls":
            path = ar[0] if ar else "." #если есть аргументы, берем первый - путь, иначе - текущая
            key_com = "-l" in ar
            ls(path, key_com)
        elif c == "cd":
            cd(ar[0] if ar else "~") #если есть аргументы, берем первый - путь, инач - домашняя
        elif c == "cat":
            if ar:
                cat(ar[0])
            else:
                typer.echo("cat: missing file")
        elif c == "cp":
            if len(ar) >= 2:
                r = "-r" in ar
                direction = [a for a in ar if not a.startswith('-')] #не флаг
                cp(direction[0], direction[1], r)
            else:
                typer.echo("cp: missing source/destination")
        elif c == "mv":
            if len(ar) >= 2:
                mv(ar[0], ar[1])
            else:
                typer.echo("mv: missing source/destination")
        elif c == "rm":
            if ar:
                r = "-r" in ar
                object = [a for a in ar if not a.startswith('-')][0]
                rm(object, r)
            else:
                typer.echo("rm: missing target")
        elif c == "zip":
            if len(ar) >= 2:
                zip(ar[0], ar[1])
            else:
                typer.echo("zip: missing archive")
        elif c == "unzip":
            if ar:
                unzip(ar[0])
            else:
                typer.echo("unzip: missing archive")
        elif c == "tar":
            if len(ar) >= 2:
                tar(ar[0], ar[1])
            else:
                typer.echo("tar: missing archive")
        elif c == "untar":
            if ar:
                untar(ar[0])
            else:
                typer.echo("untar: missing archive")
        elif c == "grep":
            if len(ar) >= 2:
                r = "-r" in ar
                ign = "-i" in ar
                path = next((a for a in ar if not a.startswith('-')), "") #шаблон
                grep(path[0], path[1], r, ign)
            else:
                typer.echo("grep: missing path")
        elif c == "history":
            lim = int(ar[0]) if ar and ar[0].isdigit() else 15
            history(lim)
        elif c == "undo":
            undo()
        else:
            typer.echo(f"Unknown command: {c}")
    except Exception as e:
        typer.echo(f"Command error: {e}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        interactive()
    else:
        app()
