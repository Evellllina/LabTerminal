import json
import datetime
from pathlib import Path

def history_i(): #запуск/создание папки для корзины
    trash_dir = Path(".trash")
    trash_dir.mkdir(exist_ok=True)
    history_file = Path(".history")
    if not history_file.exists():
        save_history([])

def add_history(c: str): #добавление истории
    history = load_history()
    history.append({
        "time": datetime.datetime.now().isoformat(),
        "command": c
    })
    save_history(history[-50:])

def output_history(lim: int = 15): #вывод истории
    history = load_history()
    return history[-lim:] if lim else history

def remove_command(): #удаление последней команды
    history = load_history()
    if history:
        save_history(history[:-1])

def get_command(): #получение последней команды
    history = load_history()
    return history[-1] if history else None

def save_history(history): #сохранение истории
    with open(".history", 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2) #сохраняет в питон объект и записыавет в файл

def load_history(): #загрузка истории
    try:
        with open(".history", 'r', encoding='utf-8') as f:
            return json.load(f) #преобразует в список
    except Exception:
        return []
