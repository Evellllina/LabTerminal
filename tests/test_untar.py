from pyfakefs.fake_filesystem import FakeFilesystem
from src.untar import command_untar
from unittest.mock import patch, MagicMock

def test_untar_nonexisted_file(fs: FakeFilesystem):
    """Несуществующий архив"""
    fs.create_dir("existing_dir")
    with patch('src.untar.typer.echo') as mock_echo:
        with patch('src.untar.command_log') as mock_log:
            command_untar("nonexisting_archive.tar.gz") #вызов функции с несущестующим архивом
            mock_echo.assert_called_with("untar: 'nonexisting_archive.tar.gz': No such file or directory")
            mock_log.assert_called_with("untar nonexisting_archive.tar.gz", False, "No such file or directory")

def test_untar_dir_instead_of_file(fs: FakeFilesystem):
    """Директория вместо файла"""
    fs.create_dir("some_directory")
    with patch('src.untar.typer.echo') as mock_echo:
        with patch('src.untar.command_log') as mock_log:
            command_untar("some_directory") #пытаемся распокавать директорию
            mock_echo.assert_called_with("untar: 'some_directory': Is a directory")
            mock_log.assert_called_with("untar some_directory", False, "Is a directory")

def test_untar_suc(fs: FakeFilesystem):
    """Распаковка архива"""
    fs.create_file("archive.tar.gz", contents="fake tar content") #создаем архив для распаковки
    with patch('src.untar.typer.echo') as mock_echo:
        with patch('src.untar.command_log') as mock_log:
            mock_tarfile = MagicMock()
            mock_tarfile.return_value.__enter__.return_value = MagicMock() #при входе
            mock_tarfile.return_value.__exit__.return_value = None #при выходе
            with patch('src.untar.tarfile.open', mock_tarfile): #подменяем функцию на mock
                command_untar("archive.tar.gz")
                mock_tarfile.assert_called_once()
                mock_echo.assert_called_with("Extracted archive: archive.tar.gz")
                mock_log.assert_called_with("untar archive.tar.gz")
