from unittest.mock import patch
import pytest
from Dataset2.mining_results_asa.DictGenerator import DictGenerator
from unittest import mock


class TestGenerateRulesDict:

    def test_case_1(self):
        dg = DictGenerator("file.csv")
        with pytest.raises(FileNotFoundError):
            dg.generate_rules_dict()

    @patch("builtins.open", mock.mock_open(read_data=""))
    def test_case_2(self):
        dg = DictGenerator("mocked_file.csv")
        result = dg.generate_rules_dict()
        assert result == {}

    @patch("builtins.open", mock.mock_open(read_data="severity;rule,project,type\n"))
    def test_case_3(self):
        dg = DictGenerator("mocked_file.csv")
        result = dg.generate_rules_dict()
        assert result == {}

    @patch("builtins.open", mock.mock_open(read_data="severity;updateDate;line;rule;project;effort;message"
                                                     ";creationDate;type"))
    def test_case_4(self):
        dg = DictGenerator("mocked_file.csv")
        result = dg.generate_rules_dict()
        assert result == {}

    @patch("builtins.open", mock.mock_open(read_data="severity;updateDate;line;rule;project;effort;message"
                                                     ";creationDate;type;component;textRange;debt;key;hash;status"))
    def test_case_5(self):
        dg = DictGenerator("mocked_file.csv")
        result = dg.generate_rules_dict()
        assert result == {}

    @patch("builtins.open", mock.mock_open(read_data="severity;line;rule;type\nBLOCKER;319;java:S6437;VULNERABILITY"
                                                     "\nBLOCKER;359;java:S6437;VULNERABILITY"))
    def test_case_6(self):
        dg = DictGenerator("mocked_file.csv")
        with pytest.raises(IndexError):
            dg.generate_rules_dict()

    @patch("builtins.open", mock.mock_open(read_data="line;rule;type\n;;NO_ISSUES_FOUND\n;;NO_ISSUES_FOUND"))
    def test_case_7(self):
        dg = DictGenerator("mocked_file.csv")
        with pytest.raises(IndexError):
            dg.generate_rules_dict()

    @patch("builtins.open", mock.mock_open(read_data="severity;updateDate;line;rule;project;effort;message"
                                                     ";creationDate;type\nBLOCKER;2024-10-09T15:40:56+0200;319;java"
                                                     ":S6437;RepositoryMining1:1"
                                                     ":9137e6cc45922b529fb776c6857647a3935471bb;1h;Revoke and change "
                                                     "this password, as it is "
                                                     "compromised;2024-10-09T15:40:56+0200;VULNERABILITY"))
    def test_case_8(self):
        dg = DictGenerator("mocked_file.csv")
        result = dg.generate_rules_dict()
        assert result != {}

    @patch("builtins.open", mock.mock_open(read_data="severity;updateDate;line;rule;project;effort;message"
                                                     ";creationDate;type\nBLOCKER;2024-10-09T15:40:56+0200;319"
                                                     ";;RepositoryMining1:1:9137e6cc45922b529fb776c6857647a3935471bb"
                                                     ";1h;Revoke and change this password, "
                                                     "as it is compromised;2024-10-09T15:40:56+0200;NO_ISSUES_FOUND"))
    def test_case_9(self):
        dg = DictGenerator("mocked_file.csv")
        result = dg.generate_rules_dict()
        assert result == {}

    @patch("builtins.open", mock.mock_open(read_data="severity;updateDate;line;rule;project;effort;message;"
                                                     "creationDate;type;col\nBLOCKER;2024-10-09T15:40:56+0200;319;"
                                                     "java:S6437;RepositoryMining1:1"
                                                     ":9137e6cc45922b529fb776c6857647a3935471bb;1h;Revoke and change "
                                                     "this password, as it is "
                                                     "compromised;2024-10-09T15:40:56+0200;VULNERABILITY;data"))
    def test_case_10(self):
        dg = DictGenerator("mocked_file.csv")
        result = dg.generate_rules_dict()
        assert result != {}

    @patch("builtins.open", mock.mock_open(read_data="severity;updateDate;line;rule;project;effort;message"
                                                     ";creationDate;type;col\nBLOCKER;2024-10-09T15:40:56+0200;319"
                                                     ";;RepositoryMining1:1:9137e6cc45922b529fb776c6857647a3935471bb"
                                                     ";1h;message;compromised;2024-10-09T15:40:56+0200;"
                                                     "NO_ISSUES_FOUND;data"))
    def test_case_11(self):
        dg = DictGenerator("mocked_file.csv")
        result = dg.generate_rules_dict()
        assert result == {}


class TestGenerateVulnerabilityDict:
    def test_case_1(self):
        dg = DictGenerator("file.csv")
        with pytest.raises(FileNotFoundError):
            dg.generate_vulnerability_dict()

    @patch("builtins.open", mock.mock_open(read_data=""))
    def test_case_2(self):
        dg = DictGenerator("mocked_file.csv")
        result = dg.generate_vulnerability_dict()
        assert result.__len__() == 0

    @patch("builtins.open", mock.mock_open(read_data="severity;updateDate;line;rule;project;effort;message"
                                                     ";creationDate;type;component;textRange;debt;key;hash;status"))
    def test_case_3(self):
        dg = DictGenerator("mocked_file.csv")
        result = dg.generate_vulnerability_dict()
        assert result.__len__() == 0

    @patch("builtins.open", mock.mock_open(read_data="severity;line;rule;type\nBLOCKER;319;java:S6437;VULNERABILITY"
                                                     "\nBLOCKER;359;java:S6437;VULNERABILITY\n;;;NO_ISSUES_FOUND\n"))
    def test_case_4(self):
        dg = DictGenerator("mocked_file.csv")
        with pytest.raises(IndexError):
            dg.generate_vulnerability_dict()

    @patch("builtins.open", mock.mock_open(read_data="severity;line;rule;type\nBLOCKER;319;java:S6437;VULNERABILITY"
                                                     "\nBLOCKER;359;java:S6437"))
    def test_case_5(self):
        dg = DictGenerator("mocked_file.csv")
        with pytest.raises(IndexError):
            dg.generate_vulnerability_dict()

    @patch("builtins.open", mock.mock_open(read_data="severity;line;rule;type\n;;;NO_ISSUES_FOUND\n"))
    def test_case_6(self):
        dg = DictGenerator("mocked_file.csv")
        with pytest.raises(IndexError):
            dg.generate_vulnerability_dict()

    @patch("builtins.open", mock.mock_open(read_data="severity;updateDate;line,"
                                                     "rule;project;effort;message;creationDate;"
                                                     "type;component\nBLOCKER;data;319;java:S6437;RepositoryMining1:1"
                                                     ":9137e6cc45922b529fb776c6857647a3935471bb;1h;message;data"
                                                     ";VULNERABILITY;"
                                                     "RepositoryMining1:1:9137e6cc45922b529fb776c6857647a3935471bb"
                                                     ":JndiLdapContextFactoryTest.java\nx;x;x;NoRule;x;x;message;data;"
                                                     "NO_ISSUES_FOUND;"
                                                     "RepositoryMining1:1:9137e6cc45922b529fb776c6857647a3935471bb"
                                                     ":Perseverance.java"))
    def test_case_7(self):
        dg = DictGenerator("mocked_file.csv")
        dg.generate_vulnerability_dict()
        assert dg.vulnerabilities.__len__() == 2

    @patch("builtins.open", mock.mock_open(read_data="severity;updateDate;line,"
                                                     "rule;project;effort;message;creationDate;"
                                                     "type;component\nBLOCKER;data;319;java:S6437;RepositoryMining1:1"
                                                     ":9137e6cc45922b529fb776c6857647a3935471bb;1h;message;data"
                                                     ";VULNERABILITY;"
                                                     "RepositoryMining1:1:9137e6cc45922b529fb776c6857647a3935471bb"
                                                     ":JndiLdapContextFactoryTest.java"))
    def test_case_8(self):
        dg = DictGenerator("mocked_file.csv")
        dg.generate_vulnerability_dict()
        assert dg.vulnerabilities.__len__() == 1

    @patch("builtins.open", mock.mock_open(read_data="severity;updateDate;line,"
                                                     "rule;project;effort;message;creationDate;"
                                                     "type;component\nx;x;x;NoRule;x;x;message;data;"
                                                     "NO_ISSUES_FOUND;"
                                                     "RepositoryMining1:1:9137e6cc45922b529fb776c6857647a3935471bb"
                                                     ":Perseverance.java"))
    def test_case_9(self):
        dg = DictGenerator("mocked_file.csv")
        dg.generate_vulnerability_dict()
        assert dg.vulnerabilities.__len__() == 1
