import os
import pytest

@pytest.fixture
def create_temp_file():
    file_path = None

    def _create_temp_file(path, content):
        nonlocal file_path
        file_path = path
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return path

    yield _create_temp_file

    if file_path and os.path.exists(file_path):
        os.remove(file_path)
