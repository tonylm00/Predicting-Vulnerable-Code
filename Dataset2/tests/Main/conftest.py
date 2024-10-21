import os

import pytest
from unittest.mock import patch, mock_open, MagicMock


@pytest.fixture
def mock_listdir_fixture(request):
    directories = request.param.get('directories', {})
    error_path = request.param.get('error_path', None)

    # Funzione mock per os.listdir
    def mock_listdir(path):
        if path == error_path:
            raise FileNotFoundError(f"The directory '{path}' was not found.")
        elif path in directories:
            return directories[path]
        else:
            raise FileNotFoundError(f"The directory '{path}' does not exist in the mock.")

    with patch('os.listdir', side_effect=mock_listdir):
        yield


@pytest.fixture
def mock_isdir_fixture(request):
    isdir_map = request.param.get('isdir_map', {})

    # Funzione mock per os.path.isdir
    def mock_isdir(path):
        return isdir_map.get(path, False)

    with patch('os.path.isdir', side_effect=mock_isdir):
        yield


# Fixture che simula open e tiene traccia di file aperti e contenuto scritto
@pytest.fixture
def mock_open_fixture(request):
    # Ottieni il dizionario file -> contenuto fittizio passato dal test
    file_contents = request.param.get('file_contents', {}) if hasattr(request, 'param') else {}
    file_to_fail = request.param.get('file_to_fail', None)
    exception_type = request.param.get('exception_type', None)

    # Crea un'istanza di mock_open generica per tracciare le chiamate
    m_open = mock_open()

    # Funzione personalizzata che restituisce il contenuto corretto in base al file aperto
    def custom_open(file_name, mode='r', *args, **kwargs):
        file_basename = os.path.basename(file_name)
        # Controlla se il file corrisponde al file che deve fallire
        print(file_basename, file_to_fail)
        if file_basename == file_to_fail:
            if 'w' in mode or 'a' in mode:  # Se aperto in modalità scrittura o append
                if exception_type == 'ValueError':
                    raise ValueError(f"Errore di valore durante la scrittura su {file_name}")
            if exception_type == 'PermissionError':
                raise PermissionError(f"Permesso negato per il file {file_name}")
            if exception_type == 'AccessError':
                raise PermissionError(f"Permesso negato per il file {file_name}")

        # Se il file è aperto in lettura e presente nei contenuti fittizi, restituisci il contenuto
        if 'r' in mode and file_basename in file_contents:
            mock_file = m_open(file_name, mode, *args, **kwargs)
            mock_file.read = MagicMock(return_value=file_contents[file_basename])
            return mock_file
        else:
            # Usa il mock_open generico per tutte le altre operazioni
            return m_open(file_name, mode, *args, **kwargs)

    # Patch della funzione 'open' con la nostra funzione personalizzata
    with patch("builtins.open", custom_open):
        yield m_open


@pytest.fixture
def mock_path_join_fixture(request):
    def mock_join(*args):
        # Concatenare gli argomenti con il separatore '/'
        return "/".join(args)

    with patch('os.path.join', side_effect=mock_join):
        yield
