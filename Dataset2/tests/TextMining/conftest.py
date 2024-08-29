from unittest.mock import mock_open, patch, Mock, MagicMock
import pytest
from collections import defaultdict
@pytest.fixture
def mock_file_read_permission_error():
    # Crea un oggetto MagicMock per il file
    mock_file = MagicMock()

    # Definisci un'eccezione da lanciare quando viene chiamato `read`
    mock_file.read.side_effect = PermissionError("Cannot read the file due to permission error.")

    # Restituisci il mock file
    return mock_file

@pytest.fixture
def mock_file_with_content(request):
    # Crea un oggetto MagicMock per il file
    mock_file = MagicMock()

    # Configura `read` per restituire la stringa passata come parametro
    mock_file.read.return_value = request.param

    # Restituisci il mock file
    return mock_file

@pytest.fixture
def mock_open_file(request):
    # Parametri passati alla fixture
    file_content = request.param.get('file_content', '')
    file_to_fail = request.param.get('file_to_fail', None)
    error_type = request.param.get('error_type', None)
    error_on_write = request.param.get('error_on_write', None)

    # Mock di 'open'
    mock = mock_open(read_data=file_content)

    def mock_open_side_effect(file, mode='r'):
        if file == file_to_fail:
            if error_type == 'FileNotFoundError':
                raise FileNotFoundError
            elif error_type == 'PermissionError':
                raise PermissionError
            elif error_type == 'IsADirectoryError':
                raise IsADirectoryError
        file_mock = mock(file, mode)
        if 'w' in mode and error_on_write:
            # Simula un errore durante la scrittura
            file_mock.write.side_effect = error_on_write
        """
        if 'w' in mode:
            # Simula un errore durante la scrittura se richiesto
            if error_on_write:
                file_mock.write.side_effect = error_on_write
            # Verifica il tipo del parametro passato a write
            original_write = file_mock.write

            def write_with_type_check(content):
                if not isinstance(content, str):
                    raise TypeError("Il parametro deve essere una stringa")
                return original_write(content)

            file_mock.write = write_with_type_check
        """
        return file_mock

    with patch('builtins.open', mock_open_side_effect):
        yield mock

@pytest.fixture
def mock_getcwd(request):
    # Parametri passati alla fixture
    path_to_return = request.param.get('path_to_return', '')

    def mock_getcwd_side_effect():
        return path_to_return

    with patch('os.getcwd', side_effect=mock_getcwd_side_effect):
        yield

@pytest.fixture
def mock_chdir(request):
    path_to_fail = request.param.get('path_to_fail', "")
    error_type = request.param.get('error_type', "")

    def mock_chdir_side_effect(path):
        if path.endswith(path_to_fail):
            if error_type == 'FileNotFoundError':
                raise FileNotFoundError(f"No such directory: '{path}'")

        return None

    with patch('os.chdir', side_effect=mock_chdir_side_effect):
        yield


@pytest.fixture
def mock_listdir(request):
    # Parametri passati alla fixture
    path_to_return_mixed = request.param.get('path_to_return_mixed', False)
    path_to_return_with_file = request.param.get('path_to_return_with_file', False)

    def mock_listdir_side_effect():
        if path_to_return_mixed:
            return ['file1.txt', 'file2.txt', 'directory1', 'directory2']
        elif path_to_return_with_file:
            return ['file1.txt', 'directory1', 'text_mining_dict.txt']
        return []

    # Mock di 'os.listdir'
    with patch('os.listdir', side_effect=mock_listdir_side_effect):
        yield


@pytest.fixture
def mock_file_system(request):
    """
    Fixture che rappresenta un file system mockato.
    La struttura è un dizionario dove le chiavi sono percorsi assoluti
    e i valori sono liste di contenuti presenti in quella directory.
    """
    fs = defaultdict(list)

    #1 cartella vuota
    #2 cartella con file
    #3 file
    repo_empty = request.param.get('repo_empty', 3)
    cvd_id_empty = request.param.get('cvd_id_empty', 3)
    folder_empty = request.param.get('folder_empty', 3)

    cvd_id = request.param.get('cvd_id', None)
    folder = request.param.get('folder', None)
    file = request.param.get('file', None)

    # Esempio di struttura di base
    # '/fake/cwd' contiene 'mining_results'
    fs['/Predicting-Vulnerable-Code/Dataset2/Text_Mining'] = []
    fs['/Predicting-Vulnerable-Code/Dataset2'] = ['mining_results']

    for i in range(1, 36):
        repo = f'RepositoryMining{i}'
        fs['/Predicting-Vulnerable-Code/Dataset2/mining_results'].append(repo)

        if repo_empty == 1:
            fs[f'/Predicting-Vulnerable-Code/Dataset2/mining_results/{repo}'] = []
        elif repo_empty == 2:
            fs[f'/Predicting-Vulnerable-Code/Dataset2/mining_results/{repo}'] = [cvd_id]

        if cvd_id_empty == 1:
            fs[f'/Predicting-Vulnerable-Code/Dataset2/mining_results/{repo}/{cvd_id}'] = []
        elif cvd_id_empty == 2:
            fs[f'/Predicting-Vulnerable-Code/Dataset2/mining_results/{repo}/{cvd_id}'] = [folder]

        if folder_empty == 1:
            fs[f'/Predicting-Vulnerable-Code/Dataset2/mining_results/{repo}/{cvd_id}/{folder}'] = []
        elif folder_empty == 2:
            fs[f'/Predicting-Vulnerable-Code/Dataset2/mining_results/{repo}/{cvd_id}/{folder}'] = [file]
    return fs


@pytest.fixture
def mock_os_functions(mock_file_system, request):
    """
    Fixture che mocka le funzioni os.chdir, os.getcwd, os.listdir e open
    basandosi sulla struttura del file system mockata.
    """
    type_error = request.param.get('type_error', '')
    file_content = request.param.get('file_content', '')
    current_dir = ['/Predicting-Vulnerable-Code/Dataset2/Text_Mining']

    def mock_getcwd():
        return current_dir[0]

    def mock_chdir(path):
        nonlocal current_dir
        # Supportiamo solo percorsi assoluti per semplicità
        if path.startswith('/'):
            new_path = path
        else:
            # Gestiamo i percorsi relativi
            if path == '..':
                if current_dir[0] == '/':
                    raise FileNotFoundError("No parent directory for root")
                new_path = '/'.join(current_dir[0].rstrip('/').split('/')[:-1])
                if not new_path:
                    new_path = '/'
            else:
                new_path = f"{current_dir[0].rstrip('/')}/{path}"
        if new_path not in mock_file_system:
            if new_path.split('/')[-1] in mock_file_system['/'.join(new_path.split('/')[:-1])]:
                raise NotADirectoryError(f"Not a directory: '{path}'")
            raise FileNotFoundError(f"No such directory: '{new_path}'")
        current_dir[0] = new_path

    def mock_listdir(path=None):
        if path is None:
            path = current_dir[0]
        else:
            if not path.startswith('/'):
                path = f"{current_dir[0].rstrip('/')}/{path}"
        if path not in mock_file_system:
            raise FileNotFoundError(f"No such directory: '{path}'")
        return mock_file_system[path][:]

    def mocked_open(file, mode='r', *args, **kwargs):
        # Simuliamo l'apertura dei file basandoci sul percorso corrente
        if type_error == "access_error":
            raise PermissionError
        if type_error == "directory_error":
            raise IsADirectoryError

        path = f"{current_dir[0].rstrip('/')}"
        #file_path = f"{path}/{file}"

        if 'r' in mode:
            if file not in mock_file_system[path]:
                raise FileNotFoundError(f"No such file: '{file}'")
            file_data = file_content
            m = mock_open(read_data=file_data).return_value
            m.read.return_value = file_data
            return m
        elif 'w' in mode or 'a' in mode:
            m = mock_open().return_value

            def write(data):
                if type_error == "perm_error":
                    raise PermissionError
                elif type_error == "value_error":
                    raise TypeError
                if path in mock_file_system:
                    mock_file_system[path].append(file)
                else:
                    mock_file_system[path] = [file]
                m.write.called_with = data  # per verificare successivamente

            m.write.side_effect = write
            return m
        else:
            return mock_open()(file, mode, *args, **kwargs)

    with patch('os.getcwd', mock_getcwd), \
            patch('os.chdir', mock_chdir), \
            patch('os.listdir', mock_listdir), \
            patch('builtins.open', mocked_open) as mocked_open_func:
        yield mocked_open_func

