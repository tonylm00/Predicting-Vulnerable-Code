import os
import pytest


@pytest.fixture
def base_fixture(tmp_path):
    # Creazione della struttura di directory temporanea
    tm_dir = tmp_path / "Text_Mining"
    asa_dir = tmp_path / "mining_results_asa"
    union_dir = tmp_path / "Union" / "Union_TM_ASA"

    tm_dir.mkdir(parents=True)
    asa_dir.mkdir(parents=True)
    union_dir.mkdir(parents=True)

    # Cambia la directory corrente nella cartella Union_TM_ASA
    original_cwd = os.getcwd()
    os.chdir(union_dir)

    yield tm_dir, asa_dir, union_dir

    # Ripristina la directory originale dopo il test
    os.chdir(original_cwd)


@pytest.fixture
def fixture_only_asa(base_fixture):
    _, asa_dir, _ = base_fixture

    csv_asa_content = (
        'Name,java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,'
        'java:asa7,java:asa8,java:asa9,java:asa10,java:asa11,java:asa12,'
        'java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,java:asa18,'
        'java:asa19,java:asa20,java:asa21,class\n'
        'paky.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,'
        'm12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n'
        'tony.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,'
        'm12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n'
    )

    asa_csv_path = asa_dir / "csv_ASA_final.csv"
    asa_csv_path.write_text(csv_asa_content)

    yield


@pytest.fixture
def fixture_only_tm(base_fixture):
    tm_dir, _, _ = base_fixture

    csv_tm_content = (
        'kind,Name,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,class\n'
        'txt,tony.java,1,2,3,4,5,6,7,8,9,10,11,pos\n'
    )

    tm_csv_path = tm_dir / "csv_mining_final.csv"
    tm_csv_path.write_text(csv_tm_content)

    yield


@pytest.fixture
def fixture_empty_tm(base_fixture):
    tm_dir, asa_dir, _ = base_fixture

    csv_tm_content = ''

    csv_asa_content = (
        'Name,java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,'
        'java:asa7,java:asa8,java:asa9,java:asa10,java:asa11,java:asa12,'
        'java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,java:asa18,'
        'java:asa19,java:asa20,java:asa21,class\n'
        'paky.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,'
        'm12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n'
        'tony.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,'
        'm12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n'
    )

    tm_csv_path = tm_dir / "csv_mining_final.csv"
    asa_csv_path = asa_dir / "csv_ASA_final.csv"

    tm_csv_path.write_text(csv_tm_content)
    asa_csv_path.write_text(csv_asa_content)

    yield


@pytest.fixture
def fixture_header_tm(base_fixture):
    tm_dir, asa_dir, _ = base_fixture

    csv_tm_content = (
        'Kind,NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,'
        'dddd,e,ee,eee,eeee,class\n'
    )

    csv_asa_content = (
        'Name,java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,'
        'java:asa7,java:asa8,java:asa9,java:asa10,java:asa11,java:asa12,'
        'java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,java:asa18,'
        'java:asa19,java:asa20,java:asa21,class\n'
        'paky.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,'
        'm12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n'
        'tony.java,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,'
        'm12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n'
    )

    tm_csv_path = tm_dir / "csv_mining_final.csv"
    asa_csv_path = asa_dir / "csv_ASA_final.csv"

    tm_csv_path.write_text(csv_tm_content)
    asa_csv_path.write_text(csv_asa_content)

    yield


@pytest.fixture
def fixture_empty_asa(base_fixture):
    tm_dir, asa_dir, _ = base_fixture

    csv_tm_content = (
        'Kind,NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,'
        'dddd,e,ee,eee,eeee,class\n'
        'File,tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,'
        'd1,d2,d3,d4,e1,e2,e3,e4,pos\n'
        'File,dani.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,'
        'd1,d2,d3,d4,e1,e2,e3,e4,pos\n'
    )

    csv_asa_content = ''

    tm_csv_path = tm_dir / "csv_mining_final.csv"
    asa_csv_path = asa_dir / "csv_ASA_final.csv"

    tm_csv_path.write_text(csv_tm_content)
    asa_csv_path.write_text(csv_asa_content)

    yield


@pytest.fixture
def fixture_header_asa(base_fixture):
    tm_dir, asa_dir, _ = base_fixture

    csv_tm_content = (
        'Kind,NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,'
        'dddd,e,ee,eee,eeee,class\n'
        'File,tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,'
        'd1,d2,d3,d4,e1,e2,e3,e4,pos\n'
        'File,dani.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,'
        'd1,d2,d3,d4,e1,e2,e3,e4,pos\n'
    )

    csv_asa_content = (
        'Name,java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,'
        'java:asa7,java:asa8,java:asa9,java:asa10,java:asa11,java:asa12,'
        'java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,java:asa18,'
        'java:asa19,java:asa20,java:asa21,class\n'
    )

    tm_csv_path = tm_dir / "csv_mining_final.csv"
    asa_csv_path = asa_dir / "csv_ASA_final.csv"

    tm_csv_path.write_text(csv_tm_content)
    asa_csv_path.write_text(csv_asa_content)

    yield


@pytest.fixture
def fixture_both_csv_empty(base_fixture):
    tm_dir, asa_dir, _ = base_fixture

    csv_tm_content = ""

    csv_asa_content = ""

    tm_csv_path = tm_dir / "csv_mining_final.csv"
    asa_csv_path = asa_dir / "csv_ASA_final.csv"

    tm_csv_path.write_text(csv_tm_content)
    asa_csv_path.write_text(csv_asa_content)

    yield


@pytest.fixture
def fixture_header_csv(base_fixture):
    tm_dir, asa_dir, _ = base_fixture

    csv_tm_content = (
        'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,class\n'
    )

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
def fixture_both_csv(base_fixture):
    tm_dir, asa_dir, _ = base_fixture

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
