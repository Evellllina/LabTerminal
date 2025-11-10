from pyfakefs.fake_filesystem import FakeFilesystem
from src.tar import command_tar
from unittest.mock import patch, MagicMock

def test_tar_nonexisted_dir(fs: FakeFilesystem):
    """Несуществующая директория"""
    fs.create_dir("existing_dir")
    with patch('src.tar.typer.echo') as mock_echo:
        with patch('src.tar.command_log') as mock_log:
            command_tar("nonexisting_dir", "archive.tar.gz") #dspjd c премещением
            mock_echo.assert_called_with("tar: 'nonexisting_dir': No such file or directory")
            mock_log.assert_called_with("tar nonexisting_dir archive.tar.gz", False, "No such file or directory")

def test_tar_for_file_instead_of_dir(fs: FakeFilesystem):
    """Файл вместо директории"""
    fs.create_file("some_file.txt", contents="test")
    with patch('src.tar.typer.echo') as mock_echo:
        with patch('src.tar.command_log') as mock_log:
            command_tar("some_file.txt", "archive.tar.gz")
            mock_echo.assert_called_with("tar: 'some_file.txt': Not a directory")
            mock_log.assert_called_with("tar some_file.txt archive.tar.gz", False, "Not a directory")

def test_tar_succ(fs: FakeFilesystem):
    """Успешное создание архива"""
    fs.create_dir("source_dir")
    fs.create_file("source_dir/file1.txt", contents="test content") #файл внури директории
    fs.create_file("archive.tar.gz")  #файл архива
    with patch('src.tar.typer.echo') as mock_echo:
        with patch('src.tar.command_log') as mock_log:
            mock_tar = MagicMock() #mock объекта архива
            mock_tarfile = MagicMock() #mock функции tarfile.open
            mock_tarfile.return_value.__enter__.return_value = mock_tar #при входе
            mock_tarfile.return_value.__exit__.return_value = None #при выходе
            with patch('src.tar.tarfile.open', mock_tarfile):
                with patch('src.tar.Path.stat') as mock_stat:
                    mock_stat.return_value.st_size = 1024 #размер файла
                    command_tar("source_dir", "archive.tar.gz")
                    mock_tarfile.assert_called_once_with("archive.tar.gz", "w:gz")
                    mock_tar.add.assert_called_once_with("source_dir", arcname="source_dir")
                    mock_echo.assert_called_with("Created tag.gz archive: archive.tar.gz")
                    mock_log.assert_called_with("tar source_dir archive.tar.gz")
