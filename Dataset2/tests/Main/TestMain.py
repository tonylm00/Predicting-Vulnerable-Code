from unittest import mock
from unittest.mock import call
import pytest
from Dataset2.Main import Main

class TestMain:
    class TestRunTextMining:
        @pytest.fixture(autouse=True)
        def setup(self, mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture):
            self.main = Main("Predicting-Vulnerable-Code/Dataset2")

        @pytest.mark.parametrize(
            'mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture',
            [
                (
                        {
                            'directories': {

                            },
                            'error_path': "Predicting-Vulnerable-Code/Dataset2/Dataset_Divided"
                        },
                        {
                            'isdir_map': {
                            }
                        },
                        {'file_contents': {}, 'file_to_fail': '', 'exception_type': ''},
                        None
                )
            ],
            indirect=['mock_listdir_fixture', 'mock_isdir_fixture', 'mock_open_fixture', 'mock_path_join_fixture']
        )
        def test_case_1(self, mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture):
            with pytest.raises(FileNotFoundError, match=r"The directory 'Predicting-Vulnerable-Code/Dataset2/Dataset_Divided' was not found."):
                self.main.run_text_mining()

        @pytest.mark.parametrize(
            'mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture',
            [
                (
                        {
                            'directories': {
                                "Predicting-Vulnerable-Code/Dataset2/Dataset_Divided":["1.csv", "2.csv", "3.csv"]
                            },
                            'error_path': ""
                        },
                        {
                            'isdir_map': {
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": False,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": False,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": False
                            }
                        },
                        {'file_contents': {}, 'file_to_fail': '', 'exception_type': ''},
                        None
                )
            ],
            indirect=['mock_listdir_fixture', 'mock_isdir_fixture', 'mock_open_fixture', 'mock_path_join_fixture']
        )
        def test_case_2(self, mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture):
            self.main.run_text_mining()
            assert mock_open_fixture.call_count == 4
            assert mock_open_fixture.call_args_list[0] == call("Predicting-Vulnerable-Code/Dataset2/mining_results/text_mining_dict.txt","w+", encoding='utf-8')
            assert mock_open_fixture.call_args_list[1] == call("Predicting-Vulnerable-Code/Dataset2/mining_results/FilteredTextMining.txt","w+", encoding='utf-8')
            mock_open_fixture().write.assert_any_call("{}")

        @pytest.mark.parametrize(
            'mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture',
            [
                (
                        {
                            'directories': {
                                "Predicting-Vulnerable-Code/Dataset2/Dataset_Divided": ["1.csv", "2.csv", "3.csv"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": [],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": [],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": []
                            },
                            'error_path': ""
                        },
                        {
                            'isdir_map': {
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": True
                            }
                        },
                        {'file_contents': {}, 'file_to_fail': '', 'exception_type': ''},
                        None
                )
            ],
            indirect=['mock_listdir_fixture', 'mock_isdir_fixture', 'mock_open_fixture', 'mock_path_join_fixture']
        )
        def test_case_3(self, mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture):
            self.main.run_text_mining()
            assert mock_open_fixture.call_count == 4
            assert mock_open_fixture.call_args_list[0] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/text_mining_dict.txt", "w+", encoding='utf-8')
            assert mock_open_fixture.call_args_list[1] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/FilteredTextMining.txt", "w+", encoding='utf-8')
            mock_open_fixture().write.assert_any_call("{}")

        @pytest.mark.parametrize(
            'mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture',
            [
                (
                        {
                            'directories': {
                                "Predicting-Vulnerable-Code/Dataset2/Dataset_Divided": ["1.csv", "2.csv", "3.csv"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": ["file.txt"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": ["file.txt"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": ["file.txt"]
                            },
                            'error_path': ""
                        },
                        {
                            'isdir_map': {
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/file.txt": False,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/file.txt": False,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/file.txt": False
                            }
                        },
                        {'file_contents': {}, 'file_to_fail': '', 'exception_type': ''},
                        None
                )
            ],
            indirect=['mock_listdir_fixture', 'mock_isdir_fixture', 'mock_open_fixture', 'mock_path_join_fixture']
        )
        def test_case_4(self, mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture):
            self.main.run_text_mining()
            assert mock_open_fixture.call_count == 4
            assert mock_open_fixture.call_args_list[0] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/text_mining_dict.txt", "w+", encoding='utf-8')
            assert mock_open_fixture.call_args_list[1] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/FilteredTextMining.txt", "w+", encoding='utf-8')
            mock_open_fixture().write.assert_any_call("{}")

        @pytest.mark.parametrize(
            'mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture',
            [
                (
                        {
                            'directories': {
                                "Predicting-Vulnerable-Code/Dataset2/Dataset_Divided": ["1.csv", "2.csv", "3.csv"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": ["CHECK.txt"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": ["CHECK.txt"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": ["CHECK.txt"]
                            },
                            'error_path': ""
                        },
                        {
                            'isdir_map': {
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/CHECK.txt": False,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/CHECK.txt": False,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/CHECK.txt": False
                            }
                        },
                        {'file_contents': {}, 'file_to_fail': '', 'exception_type': ''},
                        None
                )
            ],
            indirect=['mock_listdir_fixture', 'mock_isdir_fixture', 'mock_open_fixture', 'mock_path_join_fixture']
        )
        def test_case_5(self, mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture):
            self.main.run_text_mining()
            assert mock_open_fixture.call_count == 4
            assert mock_open_fixture.call_args_list[0] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/text_mining_dict.txt", "w+", encoding='utf-8')
            assert mock_open_fixture.call_args_list[1] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/FilteredTextMining.txt", "w+", encoding='utf-8')
            mock_open_fixture().write.assert_any_call("{}")

        @pytest.mark.parametrize(
            'mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture',
            [
                (
                        {
                            'directories': {
                                "Predicting-Vulnerable-Code/Dataset2/Dataset_Divided": ["1.csv", "2.csv", "3.csv"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": ["cvd_id1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": ["cvd_id2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": ["cvd_id3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": [],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": [],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": []
                            },
                            'error_path': ""
                        },
                        {
                            'isdir_map': {
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": True
                            }
                        },
                        {'file_contents': {}, 'file_to_fail': '', 'exception_type': ''},
                        None
                )
            ],
            indirect=['mock_listdir_fixture', 'mock_isdir_fixture', 'mock_open_fixture', 'mock_path_join_fixture']
        )
        def test_case_6(self, mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture):
            self.main.run_text_mining()
            assert mock_open_fixture.call_count == 4
            assert mock_open_fixture.call_args_list[0] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/text_mining_dict.txt", "w+", encoding='utf-8')
            assert mock_open_fixture.call_args_list[1] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/FilteredTextMining.txt", "w+", encoding='utf-8')
            mock_open_fixture().write.assert_any_call("{}")

        @pytest.mark.parametrize(
            'mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture',
            [
                (
                        {
                            'directories': {
                                "Predicting-Vulnerable-Code/Dataset2/Dataset_Divided": ["1.csv", "2.csv", "3.csv"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": ["cvd_id1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": ["cvd_id2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": ["cvd_id3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": ["file.txt"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": ["file.txt"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": ["file.txt"]
                            },
                            'error_path': ""
                        },
                        {
                            'isdir_map': {
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/file.txt": False,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/file.txt": False,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/file.txt": False
                            }
                        },
                        {'file_contents': {}, 'file_to_fail': '', 'exception_type': ''},
                        None
                )
            ],
            indirect=['mock_listdir_fixture', 'mock_isdir_fixture', 'mock_open_fixture', 'mock_path_join_fixture']
        )
        def test_case_7(self, mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture):
            self.main.run_text_mining()
            assert mock_open_fixture.call_count == 4
            assert mock_open_fixture.call_args_list[0] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/text_mining_dict.txt", "w+", encoding='utf-8')
            assert mock_open_fixture.call_args_list[1] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/FilteredTextMining.txt", "w+", encoding='utf-8')
            mock_open_fixture().write.assert_any_call("{}")

        @pytest.mark.parametrize(
            'mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture',
            [
                (
                        {
                            'directories': {
                                "Predicting-Vulnerable-Code/Dataset2/Dataset_Divided": ["1.csv", "2.csv", "3.csv"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": ["cvd_id1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": ["cvd_id2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": ["cvd_id3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": [".DS_Store"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": [".DS_Store"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": [".DS_Store"]
                            },
                            'error_path': ""
                        },
                        {
                            'isdir_map': {
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/.DS_Store": False,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/.DS_Store": False,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/.DS_Store": False
                            }
                        },
                        {'file_contents': {}, 'file_to_fail': '', 'exception_type': ''},
                        None
                )
            ],
            indirect=['mock_listdir_fixture', 'mock_isdir_fixture', 'mock_open_fixture', 'mock_path_join_fixture']
        )
        def test_case_8(self, mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture):
            self.main.run_text_mining()
            assert mock_open_fixture.call_count == 4
            assert mock_open_fixture.call_args_list[0] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/text_mining_dict.txt", "w+", encoding='utf-8')
            assert mock_open_fixture.call_args_list[1] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/FilteredTextMining.txt", "w+", encoding='utf-8')
            mock_open_fixture().write.assert_any_call("{}")

        @pytest.mark.parametrize(
            'mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture',
            [
                (
                        {
                            'directories': {
                                "Predicting-Vulnerable-Code/Dataset2/Dataset_Divided": ["1.csv", "2.csv", "3.csv"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": ["cvd_id1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": ["cvd_id2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": ["cvd_id3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": ["folder1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": ["folder2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": ["folder3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1": [],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2": [],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3": []
                            },
                            'error_path': ""
                        },
                        {
                            'isdir_map': {
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3": True

                            }
                        },
                        {'file_contents': {}, 'file_to_fail': '', 'exception_type': ''},
                        None
                )
            ],
            indirect=['mock_listdir_fixture', 'mock_isdir_fixture', 'mock_open_fixture', 'mock_path_join_fixture']
        )
        def test_case_9(self, mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture):
            self.main.run_text_mining()
            assert mock_open_fixture.call_count == 4
            assert mock_open_fixture.call_args_list[0] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/text_mining_dict.txt", "w+", encoding='utf-8')
            assert mock_open_fixture.call_args_list[1] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/FilteredTextMining.txt", "w+", encoding='utf-8')
            mock_open_fixture().write.assert_any_call("{}")

        @pytest.mark.parametrize(
            'mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture',
            [
                (
                        {
                            'directories': {
                                "Predicting-Vulnerable-Code/Dataset2/Dataset_Divided": ["1.csv", "2.csv", "3.csv"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": ["cvd_id1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": ["cvd_id2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": ["cvd_id3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": ["folder1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": ["folder2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": ["folder3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1": ["Example.java"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2": ["Example.java"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3": ["Example.java"]
                            },
                            'error_path': ""
                        },
                        {
                            'isdir_map': {
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3": True

                            }
                        },
                        {'file_contents':{'Example.java':'''public class Test {
                                                                /* This is a comment */ 
                                                                public static void main(String[] args) { 
                                                                // Single line comment
                                                                System.out.println("Hello World"); /* Inline comment */
                                                                } 
                                                            }'''},
                        'file_to_fail':'', 'exception_type':''
                        },
                        None
                )
            ],
            indirect=['mock_listdir_fixture', 'mock_isdir_fixture', 'mock_open_fixture', 'mock_path_join_fixture']
        )
        def test_case_10(self, mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture):
            with (mock.patch('Dataset2.Main.JavaTextMining') as MockText, \
                  mock.patch('Dataset2.Main.JavaTextMining.splitDict', return_value={
                      'public': 6, 'class': 3, 'test': 3, 'static': 3, 'void': 3, 'main': 3,
                      'string': 3, 'args': 3, 'system': 3, 'out': 3, 'println': 3
                  }) as mock_splitDict, \
                  mock.patch('Dataset2.Main.JavaTextMining.mergeDict', return_value={
                      'public': 6, 'class': 3, 'Test': 3, 'static': 3, 'void': 3, 'main': 3,
                      'String': 3, 'args': 3, 'System': 3, 'out': 3, 'println': 3
                  }) as mock_mergeDict):
                mock_istanza = MockText.return_value

                # Mock del metodo di istanza takeJavaClass
                mock_istanza.takeJavaClass.return_value = {
                    'public': 2, 'class': 1, 'Test': 1, 'static': 1, 'void': 1, 'main': 1,
                    'String': 1, 'args': 1, 'System': 1, 'out': 1, 'println': 1
                }
                self.main.run_text_mining()
                assert mock_open_fixture.call_count == 7
                assert mock_open_fixture.call_args_list[0] == call(
                    "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1/Example.java_text_mining.txt", "w+",
                    encoding='utf-8')
                assert mock_open_fixture.call_args_list[1] == call(
                    "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2/Example.java_text_mining.txt", "w+",
                    encoding='utf-8')
                assert mock_open_fixture.call_args_list[2] == call(
                    "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3/Example.java_text_mining.txt", "w+",
                    encoding='utf-8')
                assert mock_open_fixture.call_args_list[3] == call(
                    "Predicting-Vulnerable-Code/Dataset2/mining_results/text_mining_dict.txt", "w+", encoding='utf-8')
                assert mock_open_fixture.call_args_list[4] == call(
                    "Predicting-Vulnerable-Code/Dataset2/mining_results/FilteredTextMining.txt", "w+", encoding='utf-8')
                assert mock_open_fixture.call_args_list[5] == call(
                    "Predicting-Vulnerable-Code/Dataset2/mining_results/csv_mining_final.csv", "w+", encoding='utf-8')
                assert mock_open_fixture.call_args_list[6] == call(
                    "Predicting-Vulnerable-Code/Dataset2/mining_results/csv_mining_final.csv", "a", encoding='utf-8')

                expected_writes = [
                    "{'public': 2, 'class': 1, 'Test': 1, 'static': 1, 'void': 1, 'main': 1, 'String': 1, 'args': 1, 'System': 1, 'out': 1, 'println': 1}",
                    "{'public': 2, 'class': 1, 'Test': 1, 'static': 1, 'void': 1, 'main': 1, 'String': 1, 'args': 1, 'System': 1, 'out': 1, 'println': 1}",
                    "{'public': 2, 'class': 1, 'Test': 1, 'static': 1, 'void': 1, 'main': 1, 'String': 1, 'args': 1, 'System': 1, 'out': 1, 'println': 1}",
                    "{'public': 6, 'class': 3, 'Test': 3, 'static': 3, 'void': 3, 'main': 3, 'String': 3, 'args': 3, 'System': 3, 'out': 3, 'println': 3}",
                    "{'public': 6, 'class': 3, 'test': 3, 'static': 3, 'void': 3, 'main': 3, 'string': 3, 'args': 3, 'system': 3, 'out': 3, 'println': 3}",
                    'Name',', args',', class',', main',', out',', println',', public',', static',', string',', system',', test',', void', '\n',
                    'folder1/Example.java',',1',',1',',1',',1',',1',',2',',1',',1',',1',',1',',1','\n',
                    'folder2/Example.java',',1',',1',',1',',1',',1',',2',',1',',1',',1',',1',',1','\n',
                    'folder3/Example.java',',1',',1',',1',',1',',1',',2',',1',',1',',1',',1',',1','\n'
                ]
                scritture = [call.args[0] for call in mock_open_fixture().write.mock_calls]  # Ottieni il contenuto di ogni write
                assert scritture == expected_writes, f"Le scritture non corrispondono! Atteso: {expected_writes}, ma trovato: {scritture}"

        @pytest.mark.parametrize(
            'mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture',
            [
                (
                        {
                            'directories': {
                                "Predicting-Vulnerable-Code/Dataset2/Dataset_Divided": ["1.csv", "2.csv", "3.csv"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": ["cvd_id1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": ["cvd_id2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": ["cvd_id3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": ["folder1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": ["folder2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": ["folder3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1": [
                                    "Example.java", "Example.java_text_mining.txt"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2": [
                                    "Example.java", "Example.java_text_mining.txt"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3": [
                                    "Example.java", "Example.java_text_mining.txt"]
                            },
                            'error_path': ""
                        },
                        {
                            'isdir_map': {
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3": True

                            }
                        },
                        {'file_contents': {'Example.java': '''public class Test {
                                                                                    /* This is a comment */ 
                                                                                    public static void main(String[] args) { 
                                                                                    // Single line comment
                                                                                    System.out.println("Hello World"); /* Inline comment */
                                                                                    } 
                                                                                }'''},
                         'file_to_fail': '', 'exception_type': ''
                         },
                        None
                )
            ],
            indirect=['mock_listdir_fixture', 'mock_isdir_fixture', 'mock_open_fixture', 'mock_path_join_fixture']
        )
        def test_case_11(self, mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture):
            with (mock.patch('Dataset2.Main.JavaTextMining') as MockText, \
                  mock.patch('Dataset2.Main.JavaTextMining.splitDict', return_value={
                      'public': 6, 'class': 3, 'test': 3, 'static': 3, 'void': 3, 'main': 3,
                      'string': 3, 'args': 3, 'system': 3, 'out': 3, 'println': 3
                  }) as mock_splitDict, \
                  mock.patch('Dataset2.Main.JavaTextMining.mergeDict', return_value={
                      'public': 6, 'class': 3, 'Test': 3, 'static': 3, 'void': 3, 'main': 3,
                      'String': 3, 'args': 3, 'System': 3, 'out': 3, 'println': 3
                  }) as mock_mergeDict):
                mock_istanza = MockText.return_value

                # Mock del metodo di istanza takeJavaClass
                mock_istanza.takeJavaClass.return_value = {
                    'public': 2, 'class': 1, 'Test': 1, 'static': 1, 'void': 1, 'main': 1,
                    'String': 1, 'args': 1, 'System': 1, 'out': 1, 'println': 1
                }
                self.main.run_text_mining()
                assert mock_open_fixture.call_count == 7
                assert mock_open_fixture.call_args_list[0] == call(
                    "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1/Example.java_text_mining.txt",
                    "w+",
                    encoding='utf-8')
                assert mock_open_fixture.call_args_list[1] == call(
                    "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2/Example.java_text_mining.txt",
                    "w+",
                    encoding='utf-8')
                assert mock_open_fixture.call_args_list[2] == call(
                    "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3/Example.java_text_mining.txt",
                    "w+",
                    encoding='utf-8')
                assert mock_open_fixture.call_args_list[3] == call(
                    "Predicting-Vulnerable-Code/Dataset2/mining_results/text_mining_dict.txt", "w+", encoding='utf-8')
                assert mock_open_fixture.call_args_list[4] == call(
                    "Predicting-Vulnerable-Code/Dataset2/mining_results/FilteredTextMining.txt", "w+", encoding='utf-8')
                assert mock_open_fixture.call_args_list[5] == call(
                    "Predicting-Vulnerable-Code/Dataset2/mining_results/csv_mining_final.csv", "w+", encoding='utf-8')
                assert mock_open_fixture.call_args_list[6] == call(
                    "Predicting-Vulnerable-Code/Dataset2/mining_results/csv_mining_final.csv", "a", encoding='utf-8')

                expected_writes = [
                    "{'public': 2, 'class': 1, 'Test': 1, 'static': 1, 'void': 1, 'main': 1, 'String': 1, 'args': 1, 'System': 1, 'out': 1, 'println': 1}",
                    "{'public': 2, 'class': 1, 'Test': 1, 'static': 1, 'void': 1, 'main': 1, 'String': 1, 'args': 1, 'System': 1, 'out': 1, 'println': 1}",
                    "{'public': 2, 'class': 1, 'Test': 1, 'static': 1, 'void': 1, 'main': 1, 'String': 1, 'args': 1, 'System': 1, 'out': 1, 'println': 1}",
                    "{'public': 6, 'class': 3, 'Test': 3, 'static': 3, 'void': 3, 'main': 3, 'String': 3, 'args': 3, 'System': 3, 'out': 3, 'println': 3}",
                    "{'public': 6, 'class': 3, 'test': 3, 'static': 3, 'void': 3, 'main': 3, 'string': 3, 'args': 3, 'system': 3, 'out': 3, 'println': 3}",
                    'Name', ', args', ', class', ', main', ', out', ', println', ', public', ', static', ', string', ', system',
                    ', test', ', void', '\n',
                    'folder1/Example.java', ',1', ',1', ',1', ',1', ',1', ',2', ',1', ',1', ',1', ',1', ',1', '\n',
                    'folder2/Example.java', ',1', ',1', ',1', ',1', ',1', ',2', ',1', ',1', ',1', ',1', ',1', '\n',
                    'folder3/Example.java', ',1', ',1', ',1', ',1', ',1', ',2', ',1', ',1', ',1', ',1', ',1', '\n'
                ]
                scritture = [call.args[0] for call in
                             mock_open_fixture().write.mock_calls]  # Ottieni il contenuto di ogni write
                assert scritture == expected_writes, f"Le scritture non corrispondono! Atteso: {expected_writes}, ma trovato: {scritture}"

        @pytest.mark.parametrize(
            'mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture',
            [
                (
                        {
                            'directories': {
                                "Predicting-Vulnerable-Code/Dataset2/Dataset_Divided": ["1.csv", "2.csv", "3.csv"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": ["cvd_id1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": ["cvd_id2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": ["cvd_id3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": ["folder1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": ["folder2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": ["folder3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1": [
                                    "Example.java"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2": [
                                    "Example.java"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3": [
                                    "Example.java"]
                            },
                            'error_path': ""
                        },
                        {
                            'isdir_map': {
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3": True

                            }
                        },
                        {'file_contents': {'Example.java': '''public class Test {
                                                                                        /* This is a comment */ 
                                                                                        public static void main(String[] args) { 
                                                                                        // Single line comment
                                                                                        System.out.println("Hello World"); /* Inline comment */
                                                                                        } 
                                                                                    }'''},
                         'file_to_fail': 'Example.java_text_mining.txt', 'exception_type': 'PermissionError'
                         },
                        None
                )
            ],
            indirect=['mock_listdir_fixture', 'mock_isdir_fixture', 'mock_open_fixture', 'mock_path_join_fixture']
        )
        def test_case_12(self, mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture):
            with pytest.raises(PermissionError):
                self.main.run_text_mining()
            assert mock_open_fixture.call_count == 1
            assert mock_open_fixture.call_args_list[0] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1/Example.java", "r",
                encoding='utf-8')


        @pytest.mark.parametrize(
            'mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture',
            [
                (
                        {
                            'directories': {
                                "Predicting-Vulnerable-Code/Dataset2/Dataset_Divided": ["1.csv", "2.csv", "3.csv"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": ["cvd_id1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": ["cvd_id2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": ["cvd_id3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": ["folder1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": ["folder2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": ["folder3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1": [
                                    "Example.java"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2": [
                                    "Example.java"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3": [
                                    "Example.java"]
                            },
                            'error_path': ""
                        },
                        {
                            'isdir_map': {
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3": True

                            }
                        },
                        {'file_contents': {'Example.java': '''public class Test {
                                                                                            /* This is a comment */ 
                                                                                            public static void main(String[] args) { 
                                                                                            // Single line comment
                                                                                            System.out.println("Hello World"); /* Inline comment */
                                                                                            } 
                                                                                        }'''},
                         'file_to_fail': 'Example.java_text_mining.txt', 'exception_type': 'ValueError'
                         },
                        None
                )
            ],
            indirect=['mock_listdir_fixture', 'mock_isdir_fixture', 'mock_open_fixture', 'mock_path_join_fixture']
        )
        def test_case_13(self, mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture):
            with (mock.patch('Dataset2.Main.JavaTextMining') as MockText, \
                  mock.patch('Dataset2.Main.JavaTextMining.splitDict', return_value={
                      'public': 6, 'class': 3, 'test': 3, 'static': 3, 'void': 3, 'main': 3,
                      'string': 3, 'args': 3, 'system': 3, 'out': 3, 'println': 3
                  }) as mock_splitDict, \
                  mock.patch('Dataset2.Main.JavaTextMining.mergeDict', return_value={
                      'public': 6, 'class': 3, 'Test': 3, 'static': 3, 'void': 3, 'main': 3,
                      'String': 3, 'args': 3, 'System': 3, 'out': 3, 'println': 3
                  }) as mock_mergeDict):
                mock_istanza = MockText.return_value

                # Mock del metodo di istanza takeJavaClass
                mock_istanza.takeJavaClass.return_value = {
                    'public': 2, 'class': 1, 'Test': 1, 'static': 1, 'void': 1, 'main': 1,
                    'String': 1, 'args': 1, 'System': 1, 'out': 1, 'println': 1
                }
                with pytest.raises(ValueError):
                    self.main.run_text_mining()

        @pytest.mark.parametrize(
            'mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture',
            [
                (
                        {
                            'directories': {
                                "Predicting-Vulnerable-Code/Dataset2/Dataset_Divided": ["1.csv", "2.csv", "3.csv"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": ["cvd_id1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": ["cvd_id2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": ["cvd_id3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": ["folder1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": ["folder2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": ["folder3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1": [
                                    "Example.java"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2": [
                                    "Example.java"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3": [
                                    "Example.java"]
                            },
                            'error_path': ""
                        },
                        {
                            'isdir_map': {
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3": True

                            }
                        },
                        {'file_contents': {'Example.java': '''public class Test {
                                                                                                /* This is a comment */ 
                                                                                                public static void main(String[] args) { 
                                                                                                // Single line comment
                                                                                                System.out.println("Hello World"); /* Inline comment */
                                                                                                } 
                                                                                            }'''},
                         'file_to_fail': 'Example.java', 'exception_type': 'AccessError'
                         },
                        None
                )
            ],
            indirect=['mock_listdir_fixture', 'mock_isdir_fixture', 'mock_open_fixture', 'mock_path_join_fixture']
        )
        def test_case_14(self, mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture):
            with pytest.raises(PermissionError):
                self.main.run_text_mining()
            assert mock_open_fixture.call_count == 0


        @pytest.mark.parametrize(
            'mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture',
            [
                (
                        {
                            'directories': {
                                "Predicting-Vulnerable-Code/Dataset2/Dataset_Divided": ["1.csv", "2.csv", "3.csv"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": ["cvd_id1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": ["cvd_id2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": ["cvd_id3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": ["folder1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": ["folder2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": ["folder3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1": [".DS_Store"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2": [".DS_Store"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3": [".DS_Store"]
                            },
                            'error_path': ""
                        },
                        {
                            'isdir_map': {
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1/.DS_Store": False,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2/.DS_Store": False,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3/.DS_Store": False

                            }
                        },
                        {'file_contents': {}, 'file_to_fail': '', 'exception_type': ''},
                        None
                )
            ],
            indirect=['mock_listdir_fixture', 'mock_isdir_fixture', 'mock_open_fixture', 'mock_path_join_fixture']
        )
        def test_case_15(self, mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture):
            self.main.run_text_mining()
            assert mock_open_fixture.call_count == 4
            assert mock_open_fixture.call_args_list[0] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/text_mining_dict.txt", "w+", encoding='utf-8')
            assert mock_open_fixture.call_args_list[1] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/FilteredTextMining.txt", "w+", encoding='utf-8')
            mock_open_fixture().write.assert_any_call("{}")

        @pytest.mark.parametrize(
            'mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture',
            [
                (
                        {
                            'directories': {
                                "Predicting-Vulnerable-Code/Dataset2/Dataset_Divided": ["1.csv", "2.csv", "3.csv"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": ["cvd_id1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": ["cvd_id2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": ["cvd_id3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": ["folder1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": ["folder2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": ["folder3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1": [
                                    "file.txt"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2": [
                                    "file.txt"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3": [
                                    "file.txt"]
                            },
                            'error_path': ""
                        },
                        {
                            'isdir_map': {
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1/file.txt": False,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2/file.txt": False,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3/file.txt": False
                            }
                        },
                        {'file_contents': {}, 'file_to_fail': '', 'exception_type': ''},
                        None
                )
            ],
            indirect=['mock_listdir_fixture', 'mock_isdir_fixture', 'mock_open_fixture', 'mock_path_join_fixture']
        )
        def test_case_16(self, mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture):
            self.main.run_text_mining()
            assert mock_open_fixture.call_count == 4
            assert mock_open_fixture.call_args_list[0] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/text_mining_dict.txt", "w+", encoding='utf-8')
            assert mock_open_fixture.call_args_list[1] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/FilteredTextMining.txt", "w+", encoding='utf-8')
            mock_open_fixture().write.assert_any_call("{}")

        @pytest.mark.parametrize(
            'mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture',
            [
                (
                        {
                            'directories': {
                                "Predicting-Vulnerable-Code/Dataset2/Dataset_Divided": ["1.csv", "2.csv", "3.csv"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": ["cvd_id1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": ["cvd_id2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": ["cvd_id3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": ["folder1"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": ["folder2"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": ["folder3"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1": [
                                    "another_folder"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2": [
                                    "another_folder"],
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3": [
                                    "another_folder"],
                            },
                            'error_path': ""
                        },
                        {
                            'isdir_map': {
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining3/cvd_id3/folder3": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining1/cvd_id1/folder1/another_folder": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepositoryMining2/cvd_id2/folder2/another_folder": True,
                                "Predicting-Vulnerable-Code/Dataset2/mining_results/RepoMining3/cvd_id3/folder3/another_folder": True
                            }
                        },
                        {'file_contents': {}, 'file_to_fail': '', 'exception_type': ''},
                        None
                )
            ],
            indirect=['mock_listdir_fixture', 'mock_isdir_fixture', 'mock_open_fixture', 'mock_path_join_fixture']
        )
        def test_case_17(self, mock_listdir_fixture, mock_isdir_fixture, mock_open_fixture, mock_path_join_fixture):
            self.main.run_text_mining()
            assert mock_open_fixture.call_count == 4
            assert mock_open_fixture.call_args_list[0] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/text_mining_dict.txt", "w+", encoding='utf-8')
            assert mock_open_fixture.call_args_list[1] == call(
                "Predicting-Vulnerable-Code/Dataset2/mining_results/FilteredTextMining.txt", "w+", encoding='utf-8')
            mock_open_fixture().write.assert_any_call("{}")
