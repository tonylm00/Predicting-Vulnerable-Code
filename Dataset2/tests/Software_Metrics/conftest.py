import os
from unittest.mock import mock_open, patch, Mock, MagicMock
import pytest
from collections import defaultdict
import shutil
import itertools

@pytest.fixture
def setup_environment(request):
    levels = request.param.get('levels', 1)
    base_dir = request.param.get('base_dir', os.getcwd())
    files = request.param.get('files', {})

    dataset_divided_dir = os.path.join(base_dir, "Dataset_Divided")
    mining_results_dir = os.path.join(base_dir, "mining_results")
    software_metrics_dir = os.path.join(base_dir, "Software_Metrics")

    if os.path.exists(mining_results_dir):
        shutil.rmtree(mining_results_dir, ignore_errors=True)
    if os.path.exists(dataset_divided_dir):
        shutil.rmtree(dataset_divided_dir, ignore_errors=True)
    if os.path.exists(software_metrics_dir):
        shutil.rmtree(software_metrics_dir, ignore_errors=False)

    if files:
        cyclic_iterator = itertools.cycle(files.items())

    try:
        if levels != 0:
            os.makedirs(software_metrics_dir, mode=0o777, exist_ok=True)
        os.makedirs(mining_results_dir, mode=0o777, exist_ok=True)
        os.makedirs(dataset_divided_dir, mode=0o777, exist_ok=True)

        # Crea la struttura di directory in base ai livelli richiesti
        for i in range(1, 36):
            csv = str(i) + ".csv"
            csv_path = os.path.join(dataset_divided_dir, csv)
            with open(csv_path, 'w', encoding='utf-8') as f:
                f.write("")
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
                                f.write(content)

        yield mining_results_dir

    finally:
        if os.path.exists(mining_results_dir):
            shutil.rmtree(mining_results_dir, ignore_errors=True)
        if os.path.exists(dataset_divided_dir):
            shutil.rmtree(dataset_divided_dir, ignore_errors=True)
        if os.path.exists(software_metrics_dir):
            shutil.rmtree(software_metrics_dir, ignore_errors=True)


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

    if file_path and os.path.exists(file_path) and not file_path.endswith(".log"):
        os.remove(file_path)
