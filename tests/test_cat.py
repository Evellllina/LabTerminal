import os
from pyfakefs.fake_filesystem import FakeFilesystem
from src.cat import command_cat
from unittest.mock import patch

def test_cat_for_nonexisted_file(fs: FakeFilesystem):
    """Несуществующий файл"""
    fs.create_dir("data")
    fs.create_file(os.path.join("data", "existing.txt"), contents="test")
    with patch('src.cat.typer.echo') as mock_echo: #заменяет typer.echo
        with patch('src.cat.command_log') as mock_log: #заменяет log_command
            filepath = os.path.join("data", "nonexisting.txt") #создает путь к несуществующему файлу
            command_cat(filepath)
            expected_path = f"cat: {filepath}:  No such file or directory" #ожидаемое сообщение об ошибке
            mock_echo.assert_called_with(expected_path) #проверяет, что typer.echo был вызван с правильным сообщением
            mock_log.assert_called_with(f"cat {filepath}", False, " No such file or directory")

def test_cat_for_dir(fs: FakeFilesystem):
    """Дириктория вместо файла"""
    fs.create_dir("data")
    fs.create_file(os.path.join("data", "existing.txt"), contents="test")
    with patch('src.cat.typer.echo') as mock_echo: #заменяет typer.echo
        with patch('src.cat.command_log') as mock_log: #заменяет log_command
            command_cat("data")
            mock_echo.assert_called_with("cat: data: Is a directory")
            mock_log.assert_called_with("cat data", False, "Is a directory")
