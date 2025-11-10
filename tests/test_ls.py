from pyfakefs.fake_filesystem import FakeFilesystem
from src.ls import command_ls
from unittest.mock import patch

def test_ls_nonexisted_directory(fs: FakeFilesystem):
    """Несуществующая директория"""
    fs.create_dir("existing_dir")
    with patch('src.ls.typer.echo') as mock_echo:
        with patch('src.ls.command_log') as mock_log:
            command_ls("nonexisting_dir")
            mock_echo.assert_called_with("ls: 'nonexisting_dir': No such file or directory")
            mock_log.assert_called_with("ls nonexisting_dir", False, "No such file or directory")

def test_ls_list(fs: FakeFilesystem):
    """Dывод списка файлов"""
    fs.create_dir("test_dir")
    fs.create_file("test_dir/file_1.txt")
    fs.create_file("test_dir/file_2.txt")
    fs.create_dir("test_dir/subdir") #поддиректория
    with patch('src.ls.typer.echo') as mock_echo:
        with patch('src.ls.command_log') as mock_log:
            command_ls("test_dir")
            assert mock_echo.call_count >= 3 #ожидаем минимум 3 вызова
            mock_log.assert_called_with("ls test_dir") #успешное логирование

def test_ls_with_l(fs: FakeFilesystem):
    """Вывод с -l"""
    fs.create_dir("test_dir")
    fs.create_file("test_dir/file1.txt", contents="test content")
    with patch('src.ls.typer.echo') as mock_echo:
        with patch('src.ls.command_log') as mock_log:
            command_ls("test_dir", met=True)
            assert mock_echo.call_count >= 1
            mock_log.assert_called_with("ls test_dir-l")

def test_ls_current_dir(fs: FakeFilesystem):
    """Вывод текущей директории"""
    fs.create_file("file_1.txt")
    fs.create_file("file_2.txt")#два файла в коревой директории
    with patch('src.ls.typer.echo') as mock_echo:
        with patch('src.ls.command_log') as mock_log:
            command_ls()
            assert mock_echo.call_count >= 2
            mock_log.assert_called_with("ls .")
