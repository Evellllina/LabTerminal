from pyfakefs.fake_filesystem import FakeFilesystem
from src.unzip import command_unzip
from unittest.mock import patch, MagicMock

def test_unzip_nonexisted_file(fs: FakeFilesystem):
    """Несуществующий архив"""
    fs.create_dir("existing_dir")
    with patch('src.unzip.typer.echo') as mock_echo:
        with patch('src.unzip.command_log') as mock_log:
            command_unzip("nonexisting_archive.zip")
            mock_echo.assert_called_with("unzip: 'nonexisting_archive.zip': No such file or directory")
            mock_log.assert_called_with("unzip nonexisting_archive.zip", False, "No such file or directory")

def test_unzip_dir_instead_of_file(fs: FakeFilesystem):
    """Директория вместо файла"""
    fs.create_dir("some_directory")
    with patch('src.unzip.typer.echo') as mock_echo:
        with patch('src.unzip.command_log') as mock_log:
            command_unzip("some_directory") #пытаемся распоковать директорию
            mock_echo.assert_called_with("unzip: 'some_directory': Is a directory")
            mock_log.assert_called_with("unzip some_directory", False, "Is a directory")

def test_unzip_suc(fs: FakeFilesystem):
    """Распаковка архива"""
    fs.create_file("archive.zip", contents="fake zip content")
    with patch('src.unzip.typer.echo') as mock_echo:
        with patch('src.unzip.command_log') as mock_log:
            with patch('src.unzip.zipfile.is_zipfile') as mock_is_zipfile:
                mock_is_zipfile.return_value = True #файл является валидным zip архивом
                mock_zipfile = MagicMock()
                mock_zipfile.return_value.__enter__.return_value = MagicMock()
                mock_zipfile.return_value.__exit__.return_value = None
                with patch('src.unzip.zipfile.ZipFile', mock_zipfile):
                    command_unzip("archive.zip")
                    mock_zipfile.assert_called_once()
                    mock_echo.assert_called_with("Extracted archive: archive.zip")
                    mock_log.assert_called_with("unzip archive.zip")
