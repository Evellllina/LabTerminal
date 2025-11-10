from pyfakefs.fake_filesystem import FakeFilesystem
from src.undo import command_undo
from unittest.mock import patch

def test_undo_no_com(fs: FakeFilesystem):
    """Нет команд для отмены"""
    with patch('src.undo.typer.echo') as mock_echo:
        with patch('src.undo.command_log') as mock_log:
            with patch('src.undo.get_command') as mock_get_command:
                mock_get_command.return_value = None  #нет команд в истории
                command_undo()
                mock_echo.assert_called_with("undo: no commands")
                mock_log.assert_not_called()

def test_undo_rm(fs: FakeFilesystem):
    """Отмена команды rm"""
    fs.create_dir(".trash")
    fs.create_file(".trash/deleted_file.txt_20241201_120000", contents="original content") #файл в корзине с временной меткой
    with patch('src.undo.typer.echo') as mock_echo:
        with patch('src.undo.command_log') as mock_log:
            with patch('src.undo.get_command') as mock_get_command:
                with patch('src.undo.remove_command') as mock_remove_command:
                    with patch('src.undo.shutil.move') as mock_move: #восстановление
                        mock_get_command.return_value = {"command": "rm deleted_file.txt"}
                        command_undo()
                        mock_echo.assert_called_with("Undo rm: restored deleted_file.txt")
                        mock_move.assert_called_once()
                        mock_remove_command.assert_called_once()
                        mock_log.assert_called_with("undo")

def test_undo_cp(fs: FakeFilesystem):
    """Отмена команды cp"""
    fs.create_file("copied_file.txt", contents="test content")
    with patch('src.undo.typer.echo') as mock_echo:
        with patch('src.undo.command_log') as mock_log:
            with patch('src.undo.get_command') as mock_get_command:
                with patch('src.undo.remove_command') as mock_remove_command:
                    mock_get_command.return_value = {"command": "cp source.txt copied_file.txt"}
                    command_undo()
                    mock_echo.assert_called_with("Undo 'cp': removed copied_file.txt")
                    mock_remove_command.assert_called_once()
                    mock_log.assert_called_with("undo")
