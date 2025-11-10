from pyfakefs.fake_filesystem import FakeFilesystem
from src.zip import command_zip
from unittest.mock import patch, MagicMock

def test_zip_nonexisted_dir(fs: FakeFilesystem):
    """Несуществующая директория"""
    fs.create_dir("existing_dir")
    with patch('src.zip.typer.echo') as mock_echo:
        with patch('src.zip.command_log') as mock_log:
            command_zip("nonexisting_dir", "archive.zip")
            mock_echo.assert_called_with("zip: 'nonexisting_dir': No such file or directory")
            mock_log.assert_called_with("zip nonexisting_dir archive.zip", False, "No such file or directory")

def test_zip_file_instead_of_dir(fs: FakeFilesystem):
    """Файл вместо директории"""
    fs.create_file("some_file.txt", contents="test")
    with patch('src.zip.typer.echo') as mock_echo:
        with patch('src.zip.command_log') as mock_log:
            command_zip("some_file.txt", "archive.zip")
            mock_echo.assert_called_with("zip: 'some_file.txt': Not a directory")
            mock_log.assert_called_with("zip some_file.txt archive.zip", False, "Not a directory")

def test_zip_suc(fs: FakeFilesystem):
    """Создание архива"""
    fs.create_dir("source_dir")
    fs.create_file("source_dir/file1.txt", contents="test content") #файл внутри директории
    fs.create_file("archive.zip")
    with patch('src.zip.typer.echo') as mock_echo:
        with patch('src.zip.command_log') as mock_log:
            mock_zipfile = MagicMock()
            mock_zip_instance = MagicMock()
            mock_zipfile.return_value.__enter__.return_value = mock_zip_instance #при входе
            mock_zipfile.return_value.__exit__.return_value = None #при выходе
            with patch('src.zip.zipfile.ZipFile', mock_zipfile):
                with patch('src.zip.Path.stat') as mock_stat:
                    mock_stat.return_value.st_size = 1024
                    command_zip("source_dir", "archive.zip")
                    mock_zipfile.assert_called_once()
                    mock_echo.assert_called_with("Create zip archive: archive.zip")
                    mock_log.assert_called_with("zip source_dir archive.zip")
