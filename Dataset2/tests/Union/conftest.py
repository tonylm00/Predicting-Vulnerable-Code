import pytest


@pytest.fixture
def base_fixture(tmp_path):
    # Creazione della struttura di directory temporanea
    text_mining_dir = tmp_path / "Text_Mining"
    asa_dir = tmp_path / "mining_results_asa"
    software_metrics_dir = tmp_path / "Software_Metrics"

    union_tm_asa_dir = tmp_path / "Union" / "Union_TM_ASA"
    union_combination_dir = tmp_path / "Union" / "Total_Combination"

    text_mining_dir.mkdir(parents=True)
    asa_dir.mkdir(parents=True)
    software_metrics_dir.mkdir(parents=True)

    union_tm_asa_dir.mkdir(parents=True)
    union_combination_dir.mkdir(parents=True)

    yield text_mining_dir, asa_dir, software_metrics_dir, union_tm_asa_dir, union_combination_dir


@pytest.fixture
def fixture_csv_tm_asa(base_fixture):
    tm_dir, asa_dir, _, _, _ = base_fixture

    csv_tm_content = (
        'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,class\n'
        'tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,pos\n'
    )

    csv_asa_content = (
        'Name,java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,'
        'java:asa9,java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,'
        'java:asa17,java:asa18,java:asa19,java:asa20,java:asa21,class\n'
        'paky.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,'
        'm11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n'
        'tony.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,'
        'm11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n'
    )

    tm_csv_path = tm_dir / "csv_mining_final.csv"
    asa_csv_path = asa_dir / "csv_ASA_final.csv"

    tm_csv_path.write_text(csv_tm_content)
    asa_csv_path.write_text(csv_asa_content)

    yield


@pytest.fixture
def fixture_csv_asa(base_fixture):
    tm_dir, asa_dir, _, _, _ = base_fixture

    csv_tm_content = (
        'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,class\n'
        'tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,pos\n'
    )
    tm_csv_path = tm_dir / "csv_mining_final.csv"
    tm_csv_path.write_text(csv_tm_content)

    yield


@pytest.fixture
def fixture_csv_tm_header_asa_header(base_fixture):
    tm_dir, asa_dir, _, _, _ = base_fixture

    csv_tm_content = 'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,class\n'

    csv_asa_content = (
        'Name,java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,'
        'java:asa9,java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,'
        'java:asa17,java:asa18,java:asa19,java:asa20,java:asa21,class\n'
    )

    tm_csv_path = tm_dir / "csv_mining_final.csv"
    asa_csv_path = asa_dir / "csv_ASA_final.csv"

    tm_csv_path.write_text(csv_tm_content)
    asa_csv_path.write_text(csv_asa_content)

    yield


@pytest.fixture
def fixture_csv_asa(base_fixture):
    _, asa_dir, _, _, _ = base_fixture

    csv_asa_content = (
        'Name,java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,'
        'java:asa9,java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,'
        'java:asa17,java:asa18,java:asa19,java:asa20,java:asa21,class\n'
        'paky.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,'
        'm11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n'
        'tony.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,'
        'm11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n'
    )

    asa_csv_path = asa_dir / "csv_ASA_final.csv"
    asa_csv_path.write_text(csv_asa_content)

    yield


@pytest.fixture
def fixture_csv_tm_empty_asa_empty(base_fixture):
    tm_dir, asa_dir, _, _, _ = base_fixture

    csv_tm_content = ""
    csv_asa_content = ""

    tm_csv_path = tm_dir / "csv_mining_final.csv"
    asa_csv_path = asa_dir / "csv_ASA_final.csv"

    tm_csv_path.write_text(csv_tm_content)
    asa_csv_path.write_text(csv_asa_content)

    yield


@pytest.fixture
def fixture_csv_tm_asa_not_valid(base_fixture):
    tm_dir, asa_dir, _, _, _ = base_fixture

    csv_tm_content = (
        'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,class\n'
        'tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,pos\n'
    )

    csv_asa_content = (
        'Name,java,asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,'
        'java:asa9,java:asa10;java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,'
        'java:asa17,java:asa18,java:asa19,java:asa20,java:asa21,class\n'
        'paky.java;m1,m2,m3;m4;m5,m6,m7,m8,m9,m10,'
        'm11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n'
        'tony.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,'
        'm11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n'
    )

    tm_csv_path = tm_dir / "csv_mining_final.csv"
    asa_csv_path = asa_dir / "csv_ASA_final.csv"

    tm_csv_path.write_text(csv_tm_content)
    asa_csv_path.write_text(csv_asa_content)

    yield


@pytest.fixture
def fixture_csv_tm_not_valid_asa(base_fixture):
    tm_dir, asa_dir, _, _, _ = base_fixture

    csv_tm_content = (
        'NameClass;a;aa;aaa;aaaa;b;bb;bbb;bbbb;c;cc;ccc;cccc,d,dd,ddd,dddd,e,ee,eee,eeee,class\n'
        'tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,pos\n'
    )

    csv_asa_content = (
        'Name,java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,'
        'java:asa9,java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,'
        'java:asa17,java:asa18,java:asa19,java:asa20,java:asa21,class\n'
        'paky.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,'
        'm11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n'
        'tony.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,'
        'm11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n'
    )

    tm_csv_path = tm_dir / "csv_mining_final.csv"
    asa_csv_path = asa_dir / "csv_ASA_final.csv"

    tm_csv_path.write_text(csv_tm_content)
    asa_csv_path.write_text(csv_asa_content)

    yield


@pytest.fixture
def fixture_csv_sm(base_fixture):
    _, _, software_metrics_dir, _, _ = base_fixture

    soft_m_csv_content = (
        'kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n'
        'txt,nicola,1,2,3,4,5,6,7,8,9,10,11,pos\n'
        'txt,tony.java,1,2,3,4,5,6,7,8,9,10,11,pos\n'
    )

    software_metrics_csv_path = software_metrics_dir / "mining_results_sm_final.csv"
    software_metrics_csv_path.write_text(soft_m_csv_content)

    yield


@pytest.fixture
def fixture_csv_sm_empty(base_fixture):
    _, _, software_metrics_dir, _, _ = base_fixture

    soft_m_csv_content = ""

    software_metrics_csv_path = software_metrics_dir / "mining_results_sm_final.csv"
    software_metrics_csv_path.write_text(soft_m_csv_content)

    yield


@pytest.fixture
def fixture_csv_sm_header(base_fixture):
    _, _, software_metrics_dir, _, _ = base_fixture

    soft_m_csv_content = 'kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n'

    software_metrics_csv_path = software_metrics_dir / "mining_results_sm_final.csv"
    software_metrics_csv_path.write_text(soft_m_csv_content)

    yield


@pytest.fixture
def fixture_first_union_not_valid(base_fixture):
    _, _, _, union_combination_dir, _ = base_fixture

    soft_m_csv_content = 'kind;Name;m1,..m2,m3,m4\n'

    software_metrics_csv_path = union_combination_dir / "Union_TM_ASA.csv"
    software_metrics_csv_path.write_text(soft_m_csv_content)

    yield


@pytest.fixture
def fixture_first_union(base_fixture):
    _, _, _, union_combination_dir, _ = base_fixture

    soft_m_csv_content = 'kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n'

    software_metrics_csv_path = union_combination_dir / "Union_TM_ASA.csv"
    software_metrics_csv_path.write_text(soft_m_csv_content)

    yield
