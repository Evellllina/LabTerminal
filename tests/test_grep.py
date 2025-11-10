from pyfakefs.fake_filesystem import FakeFilesystem
from src.grep import command_grep
from unittest.mock import patch

def test_grep_nonexisted_file(fs: FakeFilesystem):
    """Поиск в несуществующем файле или директории"""
    fs.create_dir("existing_dir") #создаем директорию
    with patch('src.grep.typer.echo') as mock_echo:
        with patch('src.grep.command_log') as mock_log:
            command_grep("text", "nonexisting_file") #ищем в несуществующем файле
            mock_echo.assert_called_with("grep: 'nonexisting_file': No such file or directory")
            mock_log.assert_called_with("grep text nonexisting_file", False, "No such file or directory")

def test_grep_suc(fs: FakeFilesystem):
    """Успешный поиск в файле"""
    fs.create_file("test.txt", contents="hello world\ntext here\ngoodbye")
    with patch('src.grep.typer.echo') as mock_echo:
        with patch('src.grep.command_log') as mock_log:
            command_grep("text", "test.txt")
            mock_echo.assert_called_with("test.txt:2: text here") #ищет текст во 2 строке
            mock_log.assert_called_with("grep text test.txt")

def test_grep_no_text(fs: FakeFilesystem):
    """Ищем текст, которого нет в файле"""
    fs.create_file("test.txt", contents="hello world\ngoodbye")
    with patch('src.grep.typer.echo') as mock_echo:
        with patch('src.grep.command_log') as mock_log:
            command_grep("text", "test.txt") #ищем текст, которого нет
            mock_echo.assert_not_called() #нет вывода в консоль
            mock_log.assert_called_with("grep text test.txt")
