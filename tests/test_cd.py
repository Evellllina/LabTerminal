from pyfakefs.fake_filesystem import FakeFilesystem
from src.cd import command_cd
from unittest.mock import patch

def test_cd_nonexisted_directory(fs: FakeFilesystem):
    """Несуществующая директория"""
    fs.create_dir("existing_dir") #создаем директорию
    with patch('src.cd.typer.echo') as mock_echo:  #заменяет typer.echo
        with patch('src.cd.command_log') as mock_log:  #заменяет log_command
            with patch('src.cd.os.chdir') as mock_chdir: #перехват смены директории
                command_cd("nonexisting_dir") #вызываем команду из несуществующей директории
                mock_echo.assert_called_with("cd: nonexisting_dir: No such directory") #сообщение об ощибке
                mock_log.assert_called_with("cd nonexisting_dir", False, "No such directory") #ошибка залогировнаия с флагом
                mock_chdir.assert_not_called() #смена директории не произошла

def test_cd_file_instead_of_directory(fs: FakeFilesystem):
    """Файл вместо директории"""
    fs.create_file("some_file.txt", contents="test")
    with patch('src.cd.typer.echo') as mock_echo: #заменяет typer.echo
        with patch('src.cd.command_log') as mock_log:  #заменяет log_command
            with patch('src.cd.os.chdir') as mock_chdir: #стоп смены директории
                command_cd("some_file.txt")
                mock_echo.assert_called_with("cd: some_file.txt: Is not a directory")
                mock_log.assert_called_with("cd some_file.txt", False, "Is not a directory")
                mock_chdir.assert_not_called()

def test_cd_suc(fs: FakeFilesystem):
    """Успешная смена директории"""
    fs.create_dir("test_dir")
    with patch('src.cd.typer.echo') as mock_echo: #заменяет typer.echo
        with patch('src.cd.command_log') as mock_log: #заменяет log_command
            with patch('src.cd.os.chdir') as mock_chdir: #перехват смены директории
                command_cd("test_dir") #переходим в существующую директорию
                mock_echo.assert_not_called()
                mock_log.assert_called_with("cd test_dir")
                mock_chdir.assert_called_once()
                #проверяет, что не было ошибок
