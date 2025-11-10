import datetime

def command_log(command: str, k: bool = True, mes: str = ""):
    time_per = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("shell.log", "a", encoding="utf-8") as f: #автоматически закрывает файл после работы
        f.write(f"[{time_per}] {command}\n")
        if not k:
            f.write(f"[{time_per}] error: {mes}\n")
