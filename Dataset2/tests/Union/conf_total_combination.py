import os
import pytest


@pytest.fixture
def base_fixture(tmp_path):
    # Creazione della struttura di directory temporanea
    text_mining_dir = tmp_path / "Union" / "Union_TM_ASA"
    software_metrics_dir = tmp_path / "Software_Metrics"
    union_dir = tmp_path / "Union" / "Total_Combination"

    text_mining_dir.mkdir(parents=True)
    software_metrics_dir.mkdir(parents=True)
    union_dir.mkdir(parents=True)

    # Cambia la directory corrente nella cartella Total_Combination
    original_cwd = os.getcwd()
    os.chdir(union_dir)

    yield text_mining_dir, software_metrics_dir, union_dir

    # Ripristina la directory originale dopo il test
    os.chdir(original_cwd)


@pytest.fixture
def fixture_only_sm(base_fixture):
    _, software_metrics_dir, _ = base_fixture

    # Creazione solo del file di metriche software
    soft_m_csv_content = (
        'kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n'
        'txt,tony.java,1,2,3,4,5,6,7,8,9,10,11,pos\n'
    )

    soft_m_csv_path = software_metrics_dir / "mining_results_sm_final.csv"
    soft_m_csv_path.write_text(soft_m_csv_content)

    yield


@pytest.fixture
def fixture_only_tm(base_fixture):
    text_mining_dir, _, _ = base_fixture

    # Creazione solo del file di text mining
    mining_csv_content = (
        'NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,class\n'
        'tony.java,1,2,3,4,5,6,7,8,9,pos\n'
    )

    mining_csv_path = text_mining_dir / "Union_TM_ASA.csv"
    mining_csv_path.write_text(mining_csv_content)

    yield


@pytest.fixture
def fixture_empty_tm(base_fixture):
    text_mining_dir, software_metrics_dir, _ = base_fixture

    mining_csv_content = ""
    soft_m_csv_content = (
        'kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n'
        'txt,nicola,1,2,3,4,5,6,7,8,9,10,11,pos\n'
        'txt,tony.java,1,2,3,4,5,6,7,8,9,10,11,pos\n'
    )

    # Scrivi i file nella struttura di directory
    mining_csv_path = text_mining_dir / "Union_TM_ASA.csv"
    soft_m_csv_path = software_metrics_dir / "mining_results_sm_final.csv"

    mining_csv_path.write_text(mining_csv_content)
    soft_m_csv_path.write_text(soft_m_csv_content)

    yield


@pytest.fixture
def fixture_tm_header(base_fixture):
    text_mining_dir, software_metrics_dir, _ = base_fixture

    # Creazione dei file temporanei nelle directory appropriate
    mining_csv_content = (
        'NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,class\n'
    )
    soft_m_csv_content = (
        'kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n'
        'txt,nicola,1,2,3,4,5,6,7,8,9,10,11,pos\n'
        'txt,tony.java,1,2,3,4,5,6,7,8,9,10,11,pos\n'
    )

    # Scrivi i file nella struttura di directory
    mining_csv_path = text_mining_dir / "Union_TM_ASA.csv"
    soft_m_csv_path = software_metrics_dir / "mining_results_sm_final.csv"

    mining_csv_path.write_text(mining_csv_content)
    soft_m_csv_path.write_text(soft_m_csv_content)

    yield


@pytest.fixture
def fixture_empty_sm(base_fixture):
    text_mining_dir, software_metrics_dir, _ = base_fixture

    # Creazione dei file temporanei nelle directory appropriate
    mining_csv_content = (
        'NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,class\n'
        'tony.java,1,2,3,4,5,6,7,8,9,pos\n'
        'paky,1,2,3,4,5,6,7,8,9,pos\n'
        'dani,1,2,3,4,5,6,7,8,9,pos\n'
    )
    soft_m_csv_content = ""

    # Scrivi i file nella struttura di directory
    mining_csv_path = text_mining_dir / "Union_TM_ASA.csv"
    soft_m_csv_path = software_metrics_dir / "mining_results_sm_final.csv"

    mining_csv_path.write_text(mining_csv_content)
    soft_m_csv_path.write_text(soft_m_csv_content)

    yield


@pytest.fixture
def fixture_sm_header(base_fixture):
    text_mining_dir, software_metrics_dir, _ = base_fixture

    # Creazione dei file temporanei nelle directory appropriate
    mining_csv_content = (
        'NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,class\n'
        'tony.java,1,2,3,4,5,6,7,8,9,pos\n'
        'paky,1,2,3,4,5,6,7,8,9,pos\n'
        'dani,1,2,3,4,5,6,7,8,9,pos\n'
    )
    soft_m_csv_content = (
        'kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n'
    )

    # Scrivi i file nella struttura di directory
    mining_csv_path = text_mining_dir / "Union_TM_ASA.csv"
    soft_m_csv_path = software_metrics_dir / "mining_results_sm_final.csv"

    mining_csv_path.write_text(mining_csv_content)
    soft_m_csv_path.write_text(soft_m_csv_content)

    yield


@pytest.fixture
def fixture_both_csv(base_fixture):
    text_mining_dir, software_metrics_dir, _ = base_fixture

    # Creazione dei file temporanei nelle directory appropriate
    mining_csv_content = (
        'NameClass,a1,a2,a3,a4,a5,a6,a7,a8,a9,class\n'
        'tony.java,1,2,3,4,5,6,7,8,9,pos\n'
        'paky,1,2,3,4,5,6,7,8,9,pos\n'
        'dani,1,2,3,4,5,6,7,8,9,pos\n'
    )
    soft_m_csv_content = (
        'kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n'
        'txt,nicola,1,2,3,4,5,6,7,8,9,10,11,pos\n'
        'txt,tony.java,1,2,3,4,5,6,7,8,9,10,11,pos\n'
    )

    # Scrivi i file nella struttura di directory
    mining_csv_path = text_mining_dir / "Union_TM_ASA.csv"
    soft_m_csv_path = software_metrics_dir / "mining_results_sm_final.csv"

    mining_csv_path.write_text(mining_csv_content)
    soft_m_csv_path.write_text(soft_m_csv_content)

    yield
