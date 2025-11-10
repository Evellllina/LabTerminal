from pyfakefs.fake_filesystem import FakeFilesystem
from src.mv import command_mv
from unittest.mock import patch

def test_mv_nonexisted_file(fs: FakeFilesystem):
    """Несуществующий файл или директория"""
    fs.create_dir("existing_dir")
    with patch('src.mv.typer.echo') as mock_echo:
        with patch('src.mv.command_log') as mock_log:
            with patch('src.mv.add_history') as mock_history:
                command_mv("nonexisting_file", "destination")
                mock_echo.assert_called_with("mv: 'nonexisting_file': No such file or directory")
                mock_log.assert_called_with("mv nonexisting_file destination", False, "No such file or directory")
                mock_history.assert_not_called()

def test_mv_file(fs: FakeFilesystem):
    """Успешное перемещение файла"""
    fs.create_file("source.txt", contents="test content")
    with patch('src.mv.typer.echo') as mock_echo:
        with patch('src.mv.command_log') as mock_log:
            with patch('src.mv.add_history') as mock_history:
                with patch('src.mv.shutil.move') as mock_move:
                    command_mv("source.txt", "destination.txt")
                    mock_move.assert_called_once() #вызвана только 1 раз
                    mock_echo.assert_called_with("Moved 'source.txt' to 'destination.txt'")
                    mock_log.assert_called_with("mv source.txt destination.txt")
                    mock_history.assert_called_with("mv source.txt destination.txt")

def test_mv_dir(fs: FakeFilesystem):
    """Успешное перемещение директории"""
    fs.create_dir("source_dir")
    fs.create_file("source_dir/file.txt", contents="test")
    with patch('src.mv.typer.echo') as mock_echo:
        with patch('src.mv.command_log') as mock_log:
            with patch('src.mv.add_history') as mock_history:
                with patch('src.mv.shutil.move') as mock_move:
                    command_mv("source_dir", "destination_dir")
                    mock_move.assert_called_once()#вызвана только 1 раз
                    mock_echo.assert_called_with("Moved 'source_dir' to 'destination_dir'")
                    mock_log.assert_called_with("mv source_dir destination_dir")
                    mock_history.assert_called_with("mv source_dir destination_dir")
