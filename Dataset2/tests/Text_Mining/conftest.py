import os
from unittest.mock import mock_open, patch, Mock, MagicMock
import pytest
from collections import defaultdict
import shutil
import itertools


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

    def mock_open_side_effect(file, mode='r', encoding=None):
        if file == file_to_fail:
            if error_type == 'FileNotFoundError':
                raise FileNotFoundError
            elif error_type == 'PermissionError':
                raise PermissionError
            elif error_type == 'IsADirectoryError':
                raise IsADirectoryError
        file_mock = mock(file, mode)

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

            # Sovrascrivi il metodo write con una versione mockata del controllo del tipo
            file_mock.write = MagicMock(side_effect=write_with_type_check)

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
    fs = defaultdict(set)

    # 1 cartella vuota
    # 2 cartella con file
    # 3 file
    repo_empty = request.param.get('repo_empty', 3)
    cvd_id_empty = request.param.get('cvd_id_empty', 3)
    folder_empty = request.param.get('folder_empty', 3)

    cvd_id = request.param.get('cvd_id', None)
    folder = request.param.get('folder', None)
    file = request.param.get('file', None)

    # Esempio di struttura di base
    # '/fake/cwd' contiene 'mining_results'
    fs['/Predicting-Vulnerable-Code/Dataset2/Text_Mining'] = set()
    fs['/Predicting-Vulnerable-Code/Dataset2'] = {'mining_results'}

    for i in range(1, 36):
        if i == 18:
            continue  # RepositoryMining18 non esiste nel file system originale
        repo = f'RepositoryMining{i}'
        fs['/Predicting-Vulnerable-Code/Dataset2/mining_results'].add(repo)

        if repo_empty == 1:
            fs[f'/Predicting-Vulnerable-Code/Dataset2/mining_results/{repo}'] = set()
        elif repo_empty == 2:
            fs[f'/Predicting-Vulnerable-Code/Dataset2/mining_results/{repo}'] = {cvd_id}

        if cvd_id_empty == 1:
            fs[f'/Predicting-Vulnerable-Code/Dataset2/mining_results/{repo}/{cvd_id}'] = set()
        elif cvd_id_empty == 2:
            fs[f'/Predicting-Vulnerable-Code/Dataset2/mining_results/{repo}/{cvd_id}'] = {folder}

        if folder_empty == 1:
            fs[f'/Predicting-Vulnerable-Code/Dataset2/mining_results/{repo}/{cvd_id}/{folder}'] = set()
        elif folder_empty == 2:
            fs[f'/Predicting-Vulnerable-Code/Dataset2/mining_results/{repo}/{cvd_id}/{folder}'] = {file}
    return fs


@pytest.fixture
def mock_os_functions(mock_file_system, request):
    """
    Fixture che mocka le funzioni os.chdir, os.getcwd, os.listdir e open
    basandosi sulla struttura del file system mockata.
    """
    type_error = request.param.get('type_error', '')
    file_contents = request.param.get('file_contents', {})
    file_to_fail = request.param.get('file_to_fail', None)
    current_dir = ['/Predicting-Vulnerable-Code/Dataset2/Text_Mining']

    def mock_getcwd():
        return current_dir[0]

    chdir_mock = MagicMock()

    def mock_chdir(path):
        nonlocal current_dir
        chdir_mock(path)
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
        # Restituiamo una lista, anche se l'origine è un set, poiché os.listdir restituisce una lista
        return list(mock_file_system[path])[:]

    mock = mock_open()

    def mocked_open(file, mode='r', encoding=None):
        path = f"{current_dir[0].rstrip('/')}"
        # Simuliamo l'apertura dei file basandoci sul percorso corrente
        if 'r' in mode:
            if file == file_to_fail:
                if type_error == "access_error":
                    raise PermissionError
                if type_error == "directory_error":
                    raise IsADirectoryError
            if file not in mock_file_system[path]:
                raise FileNotFoundError(f"No such file: '{file}'")

        file_mock = mock(file, mode)
        file_mock.read = MagicMock(return_value=file_contents.get(file, ''))

        if 'w' in mode or 'a' in mode:
            if file == file_to_fail:
                if type_error == "perm_error":
                    raise PermissionError
                elif type_error == "value_error":
                    raise TypeError

            def write(data):
                if path in mock_file_system:
                    mock_file_system[path].add(file)
                else:
                    mock_file_system[path] = {file}

            file_mock.write = MagicMock(side_effect=write)

        return file_mock

    with patch('os.getcwd', mock_getcwd), \
            patch('os.chdir', mock_chdir), \
            patch('os.listdir', mock_listdir), \
            patch('builtins.open', new=mocked_open):
        yield chdir_mock, mock


@pytest.fixture
def setup_environment(request):
    levels = request.param.get('levels', 1)
    base_dir = request.param.get('base_dir', os.getcwd())
    files = request.param.get('files', {})

    mining_results_dir = os.path.join(base_dir, "mining_results")
    old_cwd = os.getcwd()
    if files:
        cyclic_iterator = itertools.cycle(files.items())

    try:
        # Crea la directory principale
        os.makedirs(mining_results_dir, mode=0o777, exist_ok=True)

        # Crea la struttura di directory in base ai livelli richiesti
        for i in range(1, 36):
            if i == 18:
                continue  # Salta RepositoryMining18

            if levels > 1:
                repo_name = f"RepositoryMining{i}"
                repo_dir = os.path.join(mining_results_dir, repo_name)
                os.makedirs(repo_dir, mode=0o777, exist_ok=True)

                if levels > 2:
                    level1_dir = os.path.join(repo_dir, str(i))
                    os.makedirs(level1_dir, mode=0o777, exist_ok=True)

                    if levels > 3:
                        level2_dir = os.path.join(level1_dir, f"commit{i}")
                        os.makedirs(level2_dir, mode=0o777, exist_ok=True)

                        if levels > 4 and len(files) == 0:
                            os.makedirs(os.path.join(level2_dir, "directory"), mode=0o777, exist_ok=True)
                        elif files:
                            file_name, content = next(cyclic_iterator)
                            file_path = os.path.join(level2_dir, file_name)
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(content)  # Contenuto di esempio, puoi personalizzarlo

        # Cambia la directory di lavoro corrente
        os.chdir(mining_results_dir)

        yield mining_results_dir

    finally:
        os.chdir(old_cwd)
        if os.path.exists(mining_results_dir):
            shutil.rmtree(mining_results_dir, ignore_errors=True)


@pytest.fixture
def create_temp_file():
    # Questa variabile manterrà il percorso del file creato
    file_path = None

    def _create_temp_file(path, content):
        nonlocal file_path
        file_path = path  # Salva il percorso del file per il teardown
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return path

    yield _create_temp_file

    # Teardown: elimina il file creato, se esiste
    if file_path and os.path.exists(file_path):
        os.remove(file_path)


"""@pytest.fixture(scope="function")
def modify_file():

    original_content = {}

    def _modify_file(file_path, new_content):
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                original_content[file_path] = f.read()

            # Modifica del contenuto del file
            with open(file_path, "w") as f:
                f.write(new_content)

    yield _modify_file

    # Teardown: ripristina il contenuto originale del file
    for file_path, content in original_content.items():
        with open(file_path, "w") as f:
            f.write(content)"""

"""@pytest.fixture(scope="function")
def delete_file():

    deleted_files = []

    def _delete_file(file_path):
        if os.path.exists(file_path):
            deleted_files.append(file_path)
            os.remove(file_path)

    yield _delete_file

    # Teardown: ricrea i file eliminati
    for file_path in deleted_files:
        with open(file_path, "w") as f:
            f.write('''
            public class SampleClass {
                // This is a sample comment
                String sampleString = "Sample";
                /* Multi-line comment
                   continues here */
                public void sampleMethod() {
                    // Another comment
                    int sampleNumber = 42;
                }
            }
            ''')


@pytest.fixture(scope="function")
def move_directory():
    moved_directories = []

    def _move_directory(src, dst):
        if os.path.exists(src):
            shutil.move(src, dst)
            moved_directories.append((src, dst))

    try:
        yield _move_directory
    finally:
        for src, dst in reversed(moved_directories):
            if os.path.exists(dst):
                shutil.move(dst, src)

"""