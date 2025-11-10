from pyfakefs.fake_filesystem import FakeFilesystem
from src.rm import command_rm
from unittest.mock import patch

def test_rm_nonexisted_file(fs: FakeFilesystem):
    """Несуществующий файл/директория"""
    fs.create_dir("existing_dir")
    with patch('src.rm.typer.echo') as mock_echo:
        with patch('src.rm.command_log') as mock_log:
            with patch('src.rm.add_history') as mock_history:
                command_rm("nonexisting_file")
                mock_echo.assert_called_with("rm: cannot remove 'nonexisting_file': No such file or directory")
                mock_log.assert_called_with("rm nonexisting_file", False, "No such file or directory")
                mock_history.assert_not_called()

def test_rm_directory_without_flag(fs: FakeFilesystem):
    """Директория без флага -r"""
    fs.create_dir("source_dir")
    with patch('src.rm.typer.echo') as mock_echo:
        with patch('src.rm.command_log') as mock_log:
            with patch('src.rm.add_history') as mock_history:
                command_rm("source_dir")
                mock_echo.assert_called_with("rm: cannot remove 'source_dir': Is a directory")
                mock_log.assert_called_with("rm source_dir", False, "Is a directory")
                mock_history.assert_not_called()

def test_rm_file(fs: FakeFilesystem):
    """Успешное удаление файла"""
    fs.create_file("source.txt", contents="test content")
    with patch('src.rm.typer.echo') as mock_echo:
        with patch('src.rm.command_log') as mock_log:
            with patch('src.rm.add_history') as mock_history:
                with patch('src.rm.shutil.move') as mock_move:
                    command_rm("source.txt")
                    mock_move.assert_called_once() #проверяем вызов перемещения
                    mock_echo.assert_called_with("Moved 'source.txt' to trash")
                    mock_log.assert_called_with("rm source.txt")
                    mock_history.assert_called_with("rm source.txt")

def test_rm_directory_with_flag(fs: FakeFilesystem):
    """Успешное удаление директории с флагом -r"""
    fs.create_dir("source_dir")
    fs.create_file("source_dir/file.txt", contents="test")
    with patch('src.rm.typer.echo') as mock_echo:
        with patch('src.rm.command_log') as mock_log:
            with patch('src.rm.add_history') as mock_history:
                with patch('src.rm.shutil.move') as mock_move:
                    with patch('src.rm.typer.confirm') as mock_confirm: #подтверждение
                        mock_confirm.return_value = True #соглашение пользователя
                        command_rm("source_dir", f=True)
                        mock_move.assert_called_once()
                        mock_echo.assert_called_with("Moved 'source_dir' to trash")
                        mock_log.assert_called_with("rm source_dir-r")
                        mock_history.assert_called_with("rm source_dir-r")

def test_rm_directory_with_flag_del(fs: FakeFilesystem):
    """Отмена удаления директории с флагом -r"""
    fs.create_dir("source_dir")
    with patch('src.rm.typer.echo') as mock_echo:
        with patch('src.rm.command_log') as mock_log:
            with patch('src.rm.add_history') as mock_history:
                with patch('src.rm.shutil.move') as mock_move:
                    with patch('src.rm.typer.confirm') as mock_confirm:
                        mock_confirm.return_value = False
                        command_rm("source_dir", f=True) #отказ пользователя
                        mock_echo.assert_called_with("Deletion cancelled")
                        mock_move.assert_not_called()
                        mock_log.assert_not_called()
                        mock_history.assert_not_called()
