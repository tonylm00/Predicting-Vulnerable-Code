import os
import pytest
from Dataset2.Union.Union_TM_ASA import Union_TMwithASA
from Dataset2.Union.Total_Combination import TotalCombination


class TestTotalCombinationIntegration:

    def test_case_1(self, base_fixture, fixture_csv_tm_asa, fixture_csv_sm):
        text_mining_dir, asa_dir, software_metrics_dir, union_tm_asa_dir, union_combination_dir = base_fixture

        os.chdir(union_tm_asa_dir)
        Union_TMwithASA.main()

        tm_asa_csv_path = union_tm_asa_dir / "Union_TM_ASA.csv"
        assert tm_asa_csv_path.exists()

        tm_asa_actual = tm_asa_csv_path.read_text()
        tm_asa_expected = 'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,java:asa1,' \
                          'java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,java:asa9,' \
                          'java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,' \
                          'java:asa18,java:asa19,class\ntony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,' \
                          'e2,e3,e4,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos '

        assert tm_asa_actual.strip() == tm_asa_expected.strip()

        os.chdir(union_combination_dir)
        TotalCombination.main()

        total_combination_csv_path = union_combination_dir / "3COMBINATION.csv"
        assert total_combination_csv_path.exists()

        total_combination_actual = total_combination_csv_path.read_text()
        total_combination_expected = 'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,' \
                                     'eeee,java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,' \
                                     'java:asa8,java:asa9,java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,' \
                                     'java:asa15,java:asa16,java:asa17,java:asa18,java:asa19,m1,m2,m3,m4,m5,m6,m7,m8,' \
                                     'm9,class\n' \
                                     'tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,m1,m2,m3,' \
                                     'm4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,1,2,3,4,5,6,' \
                                     '7,8,9,10,11,pos,pos '

        assert total_combination_actual.strip() == total_combination_expected.strip()

    def test_case_2(self, base_fixture, fixture_csv_asa, fixture_csv_sm):
        text_mining_dir, asa_dir, software_metrics_dir, union_tm_asa_dir, union_combination_dir = base_fixture

        os.chdir(union_tm_asa_dir)
        with pytest.raises(FileNotFoundError):
            Union_TMwithASA.main()

        tm_asa_csv_path = union_tm_asa_dir / "Union_TM_ASA.csv"
        assert tm_asa_csv_path.exists()

        # Verifichiamo che il contenuto sia vuoto
        tm_asa_content = tm_asa_csv_path.read_text().strip()
        assert tm_asa_content == ""

        os.chdir(union_combination_dir)
        TotalCombination.main()

        total_combination_csv_path = union_combination_dir / "3COMBINATION.csv"
        assert total_combination_csv_path.exists()

        # Verifichiamo che il contenuto sia vuoto
        total_combination_actual = total_combination_csv_path.read_text()
        total_combination_expected = ""

        assert total_combination_actual.strip() == total_combination_expected.strip()

    def test_case_3(self, base_fixture, fixture_csv_tm_asa_not_valid, fixture_csv_sm):
        text_mining_dir, asa_dir, software_metrics_dir, union_tm_asa_dir, union_combination_dir = base_fixture

        os.chdir(union_tm_asa_dir)
        Union_TMwithASA.main()

        tm_asa_csv_path = union_tm_asa_dir / "Union_TM_ASA.csv"
        assert tm_asa_csv_path.exists()

        tm_asa_actual = tm_asa_csv_path.read_text()
        tm_asa_expected = 'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,class\n' \
                          'tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,0,0,0,0,0,0,0,0,0,0,' \
                          '0,0,0,0,0,0,0,0,0,pos '

        assert tm_asa_actual.strip() == tm_asa_expected.strip()

        os.chdir(union_combination_dir)
        TotalCombination.main()

        total_combination_csv_path = union_combination_dir / "3COMBINATION.csv"
        assert total_combination_csv_path.exists()

        total_combination_actual = total_combination_csv_path.read_text()
        total_combination_expected = 'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,' \
                                     'eeee,m1,m2,m3,m4,m5,m6,m7,m8,m9,class\n' \
                                     'tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,0,0,0,0,' \
                                     '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,pos,pos '

        assert total_combination_actual.strip() == total_combination_expected.strip()

    def test_case_4(self, base_fixture, fixture_csv_tm_empty_asa_empty, fixture_csv_sm):
        text_mining_dir, asa_dir, software_metrics_dir, union_tm_asa_dir, union_combination_dir = base_fixture

        os.chdir(union_tm_asa_dir)
        Union_TMwithASA.main()

        tm_asa_csv_path = union_tm_asa_dir / "Union_TM_ASA.csv"
        assert tm_asa_csv_path.exists()

        # Verifichiamo che il contenuto sia vuoto
        tm_asa_content = tm_asa_csv_path.read_text().strip()
        assert tm_asa_content == ""

        os.chdir(union_combination_dir)
        TotalCombination.main()

        total_combination_csv_path = union_combination_dir / "3COMBINATION.csv"
        assert total_combination_csv_path.exists()

        # Verifichiamo che il contenuto sia vuoto
        total_combination_actual = total_combination_csv_path.read_text()
        total_combination_expected = ""

        assert total_combination_actual.strip() == total_combination_expected.strip()

    def test_case_5(self, base_fixture, fixture_csv_tm_asa):
        text_mining_dir, asa_dir, software_metrics_dir, union_tm_asa_dir, union_combination_dir = base_fixture

        os.chdir(union_tm_asa_dir)
        Union_TMwithASA.main()

        tm_asa_csv_path = union_tm_asa_dir / "Union_TM_ASA.csv"
        assert tm_asa_csv_path.exists()

        tm_asa_actual = tm_asa_csv_path.read_text()
        tm_asa_expected = 'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,java:asa1,' \
                          'java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,java:asa9,' \
                          'java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,' \
                          'java:asa18,java:asa19,class\ntony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,' \
                          'e2,e3,e4,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos '

        assert tm_asa_actual.strip() == tm_asa_expected.strip()

        os.chdir(union_combination_dir)

        with pytest.raises(FileNotFoundError):
            TotalCombination.main()

        total_combination_csv_path = union_combination_dir / "3COMBINATION.csv"
        assert total_combination_csv_path.exists()

        # Verifichiamo che il contenuto sia vuoto
        total_combination_actual = total_combination_csv_path.read_text()
        total_combination_expected = ""

        assert total_combination_actual.strip() == total_combination_expected.strip()

    def test_case_6(self, base_fixture, fixture_csv_tm_not_valid_asa, fixture_csv_sm):
        text_mining_dir, asa_dir, software_metrics_dir, union_tm_asa_dir, union_combination_dir = base_fixture

        os.chdir(union_tm_asa_dir)
        Union_TMwithASA.main()

        tm_asa_csv_path = union_tm_asa_dir / "Union_TM_ASA.csv"
        assert tm_asa_csv_path.exists()

        tm_asa_actual = tm_asa_csv_path.read_text()
        tm_asa_expected = 'NameClass;a;aa;aaa;aaaa;b;bb;bbb;bbbb;c;cc;ccc;cccc,d,dd,ddd,dddd,e,ee,eee,eeee,java:asa1,' \
                          'java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,java:asa9,' \
                          'java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,' \
                          'java:asa18,java:asa19,class\n' \
                          'tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,m1,m2,m3,m4,m5,m6,' \
                          'm7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos '

        assert tm_asa_actual.strip() == tm_asa_expected.strip()

        os.chdir(union_combination_dir)
        TotalCombination.main()

        total_combination_csv_path = union_combination_dir / "3COMBINATION.csv"
        assert total_combination_csv_path.exists()

        total_combination_actual = total_combination_csv_path.read_text()
        total_combination_expected = 'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,' \
                                     'eeee,m1,m2,m3,m4,m5,m6,m7,m8,m9,class\n' \
                                     'tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,0,0,0,0,' \
                                     '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,pos,pos '

        assert total_combination_actual.strip() == total_combination_expected.strip()

    def test_case_7(self, base_fixture, fixture_csv_tm_asa_not_valid, fixture_csv_sm):
        text_mining_dir, asa_dir, software_metrics_dir, union_tm_asa_dir, union_combination_dir = base_fixture

        os.chdir(union_tm_asa_dir)
        Union_TMwithASA.main()

        tm_asa_csv_path = union_tm_asa_dir / "Union_TM_ASA.csv"
        assert tm_asa_csv_path.exists()

        tm_asa_actual = tm_asa_csv_path.read_text()
        tm_asa_expected = 'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,java,asa1,' \
                          'java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,java:asa9,' \
                          'java:asa10;java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,' \
                          'java:asa18,java:asa19,class\n' \
                          'tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,m1,m2,m3,m4,m5,m6,' \
                          'm7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos '

        assert tm_asa_actual.strip() == tm_asa_expected.strip()

        os.chdir(union_combination_dir)
        TotalCombination.main()

        total_combination_csv_path = union_combination_dir / "3COMBINATION.csv"
        assert total_combination_csv_path.exists()

        total_combination_actual = total_combination_csv_path.read_text()
        total_combination_expected = 'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,' \
                                     'eeee,java,asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,' \
                                     'java:asa8,java:asa9,java:asa10;java:asa11,java:asa12,java:asa13,java:asa14,' \
                                     'java:asa15,java:asa16,java:asa17,java:asa18,java:asa19,m1,m2,m3,m4,m5,m6,m7,m8,' \
                                     'm9,class\n' \
                                     'tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,m1,m2,m3,' \
                                     'm4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,1,2,3,4,5,6,' \
                                     '7,8,9,10,11,pos,pos '

        assert total_combination_actual.strip() == total_combination_expected.strip()

    def test_case_8(self, base_fixture, fixture_csv_tm_header_asa_header, fixture_csv_sm_header):
        text_mining_dir, asa_dir, software_metrics_dir, union_tm_asa_dir, union_combination_dir = base_fixture

        os.chdir(union_tm_asa_dir)
        Union_TMwithASA.main()

        tm_asa_csv_path = union_tm_asa_dir / "Union_TM_ASA.csv"
        assert tm_asa_csv_path.exists()

        tm_asa_actual = tm_asa_csv_path.read_text()
        tm_asa_expected = 'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,java:asa1,' \
                          'java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,java:asa9,' \
                          'java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,' \
                          'java:asa18,java:asa19,class'

        assert tm_asa_actual.strip() == tm_asa_expected.strip()

        os.chdir(union_combination_dir)
        TotalCombination.main()

        total_combination_csv_path = union_combination_dir / "3COMBINATION.csv"
        assert total_combination_csv_path.exists()

        total_combination_actual = total_combination_csv_path.read_text()
        total_combination_expected = 'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,' \
                                     'eeee,java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,' \
                                     'java:asa8,java:asa9,java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,' \
                                     'java:asa15,java:asa16,java:asa17,java:asa18,java:asa19,m1,m2,m3,m4,m5,m6,m7,m8,' \
                                     'm9,class'

        assert total_combination_actual.strip() == total_combination_expected.strip()

    def test_case_9(self, base_fixture, fixture_csv_asa, fixture_csv_sm):
        text_mining_dir, asa_dir, software_metrics_dir, union_tm_asa_dir, union_combination_dir = base_fixture

        os.chdir(union_tm_asa_dir)
        with pytest.raises(FileNotFoundError):
            Union_TMwithASA.main()

        tm_asa_csv_path = union_tm_asa_dir / "Union_TM_ASA.csv"
        assert tm_asa_csv_path.exists()

        tm_asa_actual = tm_asa_csv_path.read_text()
        tm_asa_expected = ""

        assert tm_asa_actual.strip() == tm_asa_expected.strip()

        os.chdir(union_combination_dir)
        TotalCombination.main()

        total_combination_csv_path = union_combination_dir / "3COMBINATION.csv"
        assert total_combination_csv_path.exists()

        total_combination_actual = total_combination_csv_path.read_text()
        total_combination_expected = ""

        assert total_combination_actual.strip() == total_combination_expected.strip()

    def test_case_10(self, base_fixture):
        text_mining_dir, asa_dir, software_metrics_dir, union_tm_asa_dir, union_combination_dir = base_fixture

        os.chdir(union_tm_asa_dir)
        with pytest.raises(FileNotFoundError):
            Union_TMwithASA.main()

        tm_asa_csv_path = union_tm_asa_dir / "Union_TM_ASA.csv"
        assert tm_asa_csv_path.exists()

        # Verifichiamo che il contenuto sia vuoto
        tm_asa_content = tm_asa_csv_path.read_text().strip()
        assert tm_asa_content == ""

        os.chdir(union_combination_dir)
        with pytest.raises(FileNotFoundError):
            TotalCombination.main()

        total_combination_csv_path = union_combination_dir / "3COMBINATION.csv"
        assert total_combination_csv_path.exists()

        # Verifichiamo che il contenuto sia vuoto
        total_combination_actual = total_combination_csv_path.read_text()
        total_combination_expected = ""

        assert total_combination_actual.strip() == total_combination_expected.strip()

    def test_case_11(self, base_fixture, fixture_csv_tm_asa, fixture_first_union_not_valid, fixture_csv_sm):
        text_mining_dir, asa_dir, software_metrics_dir, union_tm_asa_dir, union_combination_dir = base_fixture

        os.chdir(union_tm_asa_dir)
        Union_TMwithASA.main()

        tm_asa_csv_path = union_tm_asa_dir / "Union_TM_ASA.csv"
        assert tm_asa_csv_path.exists()

        tm_asa_actual = tm_asa_csv_path.read_text()
        tm_asa_expected = 'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,java:asa1,' \
                          'java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,java:asa9,' \
                          'java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,' \
                          'java:asa18,java:asa19,class\ntony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,' \
                          'e2,e3,e4,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos '

        assert tm_asa_actual.strip() == tm_asa_expected.strip()

        os.chdir(union_combination_dir)
        TotalCombination.main()

        total_combination_csv_path = union_combination_dir / "3COMBINATION.csv"
        assert total_combination_csv_path.exists()

        total_combination_actual = total_combination_csv_path.read_text()
        total_combination_expected = 'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,' \
                                     'eeee,java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,' \
                                     'java:asa8,java:asa9,java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,' \
                                     'java:asa15,java:asa16,java:asa17,java:asa18,java:asa19,m1,m2,m3,m4,m5,m6,m7,m8,' \
                                     'm9,class\n' \
                                     'tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,m1,m2,m3,' \
                                     'm4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,1,2,3,4,5,6,' \
                                     '7,8,9,10,11,pos,pos '

        assert total_combination_actual.strip() == total_combination_expected.strip()

    def test_case_12(self, base_fixture, fixture_csv_tm_asa, fixture_first_union, fixture_csv_sm):
        text_mining_dir, asa_dir, software_metrics_dir, union_tm_asa_dir, union_combination_dir = base_fixture

        os.chdir(union_tm_asa_dir)
        Union_TMwithASA.main()

        tm_asa_csv_path = union_tm_asa_dir / "Union_TM_ASA.csv"
        assert tm_asa_csv_path.exists()

        tm_asa_actual = tm_asa_csv_path.read_text()
        tm_asa_expected = 'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,java:asa1,' \
                          'java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,java:asa9,' \
                          'java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,' \
                          'java:asa18,java:asa19,class\ntony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,' \
                          'e2,e3,e4,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos '

        assert tm_asa_actual.strip() == tm_asa_expected.strip()

        os.chdir(union_combination_dir)
        TotalCombination.main()

        total_combination_csv_path = union_combination_dir / "3COMBINATION.csv"
        assert total_combination_csv_path.exists()

        total_combination_actual = total_combination_csv_path.read_text()
        total_combination_expected = 'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,' \
                                     'eeee,java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,' \
                                     'java:asa8,java:asa9,java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,' \
                                     'java:asa15,java:asa16,java:asa17,java:asa18,java:asa19,m1,m2,m3,m4,m5,m6,m7,m8,' \
                                     'm9,class\n' \
                                     'tony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,e2,e3,e4,m1,m2,m3,' \
                                     'm4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,1,2,3,4,5,6,' \
                                     '7,8,9,10,11,pos,pos '

        assert total_combination_actual.strip() == total_combination_expected.strip()

    def test_case_13(self, base_fixture, fixture_csv_tm_asa, fixture_csv_sm_empty):
        text_mining_dir, asa_dir, software_metrics_dir, union_tm_asa_dir, union_combination_dir = base_fixture

        os.chdir(union_tm_asa_dir)
        Union_TMwithASA.main()

        tm_asa_csv_path = union_tm_asa_dir / "Union_TM_ASA.csv"
        assert tm_asa_csv_path.exists()

        tm_asa_actual = tm_asa_csv_path.read_text()
        tm_asa_expected = 'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,eeee,java:asa1,' \
                          'java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,java:asa8,java:asa9,' \
                          'java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,java:asa15,java:asa16,java:asa17,' \
                          'java:asa18,java:asa19,class\ntony.java,a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,d1,d2,d3,d4,e1,' \
                          'e2,e3,e4,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,pos'

        assert tm_asa_actual.strip() == tm_asa_expected.strip()

        os.chdir(union_combination_dir)
        TotalCombination.main()

        total_combination_csv_path = union_combination_dir / "3COMBINATION.csv"
        assert total_combination_csv_path.exists()

        total_combination_actual = total_combination_csv_path.read_text()
        total_combination_expected = 'NameClass,a,aa,aaa,aaaa,b,bb,bbb,bbbb,c,cc,ccc,cccc,d,dd,ddd,dddd,e,ee,eee,' \
                                     'eeee,java:asa1,java:asa2,java:asa3,java:asa4,java:asa5,java:asa6,java:asa7,' \
                                     'java:asa8,java:asa9,java:asa10,java:asa11,java:asa12,java:asa13,java:asa14,' \
                                     'java:asa15,java:asa16,java:asa17,java:asa18,java:asa19,class'

        assert total_combination_actual.strip() == total_combination_expected.strip()
