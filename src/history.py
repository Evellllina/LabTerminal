import datetime
import typer
from src.logger import command_log
from src.history_functions import output_history

def command_history(limit: int = 15):
    try:
        hist = output_history(limit)
        if not hist:
            typer.echo("No history")
            return
        for i, el in enumerate(hist, 1):
            time_per = datetime.datetime.fromisoformat(el["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            typer.echo(f"{i:3d}. [{time_per}] {el['command']}")
        command_log(f"history {limit}")

    except Exception as e:
        typer.echo(f"history: error: {e}")
        command_log(f"history {limit}", False, str(e))
