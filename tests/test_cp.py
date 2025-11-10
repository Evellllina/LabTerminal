from pyfakefs.fake_filesystem import FakeFilesystem
from src.cp import command_cp
from unittest.mock import patch

def test_cp_nonexisted_file(fs: FakeFilesystem):
    """Несуществующий файл или директория"""
    fs.create_dir("existing_dir") #создаем директорию
    with patch('src.cp.typer.echo') as mock_echo:
        with patch('src.cp.command_log') as mock_log:
            with patch('src.cp.add_history') as mock_history: #стоп добавления в историю
                command_cp("nonexisting_file", "destination") #копируем
                mock_echo.assert_called_with("cp: 'nonexisting_file': No such file or directory")
                mock_log.assert_called_with("cp nonexisting_file destination", False, "No such file or directory")
                mock_history.assert_not_called()

def test_cp_directory_without_flag(fs: FakeFilesystem):
    """Перемещение директория без -r"""
    fs.create_dir("source_dir")
    with patch('src.cp.typer.echo') as mock_echo:
        with patch('src.cp.command_log') as mock_log:
            with patch('src.cp.add_history') as mock_history:
                command_cp("source_dir", "destination")
                mock_echo.assert_called_with("cp: -r not specified; omitting directory 'source_dir'")
                mock_log.assert_called_with("cp source_dir destination", False, "Is a directory; -r not specified")
                mock_history.assert_not_called()

def test_cp_file_suc(fs: FakeFilesystem):
    """Успешное копирование файла"""
    fs.create_file("source.txt", contents="test content")
    with patch('src.cp.typer.echo') as mock_echo:
        with patch('src.cp.command_log') as mock_log:
            with patch('src.cp.add_history') as mock_history:
                with patch('src.cp.shutil.copy2') as mock_copy:
                    command_cp("source.txt", "destination.txt")
                    mock_copy.assert_called_once() #копирование вызвано
                    mock_echo.assert_called_with("Copied 'source.txt' to 'destination.txt'")
                    mock_log.assert_called_with("cp source.txt destination.txt")
                    mock_history.assert_called_with("cp source.txt destination.txt")

def test_cp_directory(fs: FakeFilesystem):
    """Успешное копирование директории с флагом -r"""
    fs.create_dir("source_dir")
    fs.create_file("source_dir/file.txt", contents="test")
    with patch('src.cp.typer.echo') as mock_echo:
        with patch('src.cp.command_log') as mock_log:
            with patch('src.cp.add_history') as mock_history:
                with patch('src.cp.shutil.copytree') as mock_copytree:
                    command_cp("source_dir", "destination_dir", f=True)
                    mock_copytree.assert_called_once()
                    mock_echo.assert_called_with("Copied 'source_dir' to 'destination_dir'")
                    mock_log.assert_called_with("cp source_dir destination_dir-r")
                    mock_history.assert_called_with("cp source_dir destination_dir-r")
