import pytest
from Dataset2.Union.Union_TM_ASA import Union_TMwithASA


class TestUnionTMwithASAIntegration:

    def test_case_1(self, fixture_both_csv, base_fixture):
        _, _, union_dir_path = base_fixture

        Union_TMwithASA.main()

        output_file = union_dir_path / "Union_TM_ASA.csv"
        assert output_file.exists()

        written_data = output_file.read_text()
        expected_output = "NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee," \
                          "java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,java:asa9," \
                          "java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,java:asa17," \
                          "java:asa18,java:asa19,class\n" \
                          "tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,m1,m2,m3,m4,m5,m6,m7," \
                          "m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos\n"

        assert written_data.strip() == expected_output.strip()

    def test_case_2(self, fixture_empty_tm, base_fixture):
        _, _, union_dir_path = base_fixture

        Union_TMwithASA.main()

        output_file = union_dir_path / "Union_TM_ASA.csv"
        assert output_file.exists()

        written_data = output_file.read_text()
        expected_output = ''

        assert written_data.strip() == expected_output.strip()

    def test_case_3(self, fixture_empty_asa, base_fixture):
        _, _, union_dir_path = base_fixture

        Union_TMwithASA.main()

        output_file = union_dir_path / "Union_TM_ASA.csv"
        assert output_file.exists()

        written_data = output_file.read_text()
        expected_output = 'Kind,NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,' \
                          'd,dd,ddd,dddd,e,ee,eee,eeee,class\n' \
                          'File,tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,0,0,0,0,0,0,0,' \
                          '0,0,0,0,0,0,0,0,0,0,0,0,pos\n' \
                          'File,dani.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,0,0,0,0,0,0,0,' \
                          '0,0,0,0,0,0,0,0,0,0,0,0,pos '

        assert written_data.strip() == expected_output.strip()

    def test_case_4(self, fixture_only_asa, base_fixture):
        _, _, union_dir_path = base_fixture

        with pytest.raises(FileNotFoundError):
            Union_TMwithASA.main()

        output_file = union_dir_path / "Union_TM_ASA.csv"
        assert output_file.exists()

        written_data = output_file.read_text()
        assert written_data.strip() == ''

    def test_case_5(self, fixture_only_tm, base_fixture):
        _, _, union_dir_path = base_fixture

        with pytest.raises(FileNotFoundError):
            Union_TMwithASA.main()

        output_file = union_dir_path / "Union_TM_ASA.csv"
        assert output_file.exists()

        written_data = output_file.read_text()
        assert written_data.strip() == ''
