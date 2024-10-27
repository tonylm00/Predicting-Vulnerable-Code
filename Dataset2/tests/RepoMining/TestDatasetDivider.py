import pytest
from unittest.mock import patch, mock_open, call
from Dataset2.tests.RepoMining.conftest import generate_csv_string
from Dataset2.RepoMining.DatasetDivider import DatasetDivider


class TestDatasetDivider:
    DATASET_NAME = 'initial_Dataset.csv'
    DATASET_HEADERS = 'cve_id,repo_url,commit_id,cls'

    DIR_NAME = 'Dataset_Divided'

    BASE_DIR = 'test/path'

    @pytest.mark.parametrize('mock_op_fail', [BASE_DIR + '/' + DATASET_NAME], indirect=True)
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    def test_case_1_new(self, mock_join, mock_op_fail):

        data_divider = DatasetDivider(self.BASE_DIR, self.DATASET_NAME)

        with pytest.raises(FileNotFoundError):
            data_divider.divide_dataset()

    @patch('os.path.exists', return_value=True)
    @patch('shutil.rmtree')
    @patch('os.makedirs')
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    @pytest.mark.parametrize('mock_files', [
        {BASE_DIR + '/' + DATASET_NAME: generate_csv_string(0), BASE_DIR + '/' + DIR_NAME + '/' + '1.csv': None}
    ], indirect=True)
    def test_case_2_new(self, mock_join, mock_makedirs, mock_rmtree, mock_exists, mock_files):
        data_divider = DatasetDivider(self.BASE_DIR, self.DATASET_NAME)
        data_divider.divide_dataset()

        dataset_path = self.BASE_DIR + '/' + self.DATASET_NAME
        data_divide_dir = self.BASE_DIR + '/' + self.DIR_NAME
        file_path = data_divide_dir + '/' + '1.csv'

        mock_rmtree.assert_called_with(data_divide_dir)

        mock_makedirs.assert_called_with(data_divide_dir)

        mock_files[dataset_path].assert_called_with(dataset_path, 'r')

        mock_files[file_path].assert_called_with(file_path, 'w+')
        mock_files[file_path]().writelines.assert_called_with([self.DATASET_HEADERS + '\n'])

    @patch('os.path.exists', return_value=True)
    @patch('shutil.rmtree')
    @patch('os.makedirs')
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    @pytest.mark.parametrize('mock_files', [
        {BASE_DIR + '/' + DATASET_NAME: generate_csv_string(50), BASE_DIR + '/' + DIR_NAME + '/' + '1.csv': None}
    ], indirect=True)
    @pytest.mark.parametrize('mock_op_permission_err', [
        BASE_DIR + '/' + DIR_NAME + '/' + '1.csv'
    ], indirect=True)
    def test_case_3_new(self, mock_join, mock_makedirs, mock_rmtree, mock_exists, mock_files, mock_op_permission_err):

        data_divider = DatasetDivider(self.BASE_DIR, self.DATASET_NAME)

        with pytest.raises(PermissionError):

            data_divider.divide_dataset()

    @patch('os.path.exists', return_value=True)
    @patch('shutil.rmtree')
    @patch('os.makedirs')
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    @pytest.mark.parametrize('mock_files', [
        {BASE_DIR + '/' + DATASET_NAME: generate_csv_string(50),
         BASE_DIR + '/' + DIR_NAME + '/' + '1.csv': None,
         BASE_DIR + '/' + DIR_NAME + '/' + '2.csv': None}
    ], indirect=True)
    def test_case_4_new(self, mock_join, mock_makedirs, mock_rmtree, mock_exists, mock_files):
        data_divider = DatasetDivider(self.BASE_DIR, self.DATASET_NAME)
        data_divider.divide_dataset()

        dataset_path = self.BASE_DIR + '/' + self.DATASET_NAME
        data_divide_dir = self.BASE_DIR + '/' + self.DIR_NAME
        file_path = data_divide_dir + '/' + '1.csv'

        lines_per_dataset = 50

        oracle_data = generate_csv_string(50)

        lines = oracle_data.strip().split('\n')  # Use '\r\n' to split lines
        lines = [line + "\n" for line in lines[1:]]

        mock_rmtree.assert_called_with(data_divide_dir)

        mock_makedirs.assert_called_with(data_divide_dir)

        mock_files[dataset_path].assert_called_with(dataset_path, 'r')

        mock_files[file_path].assert_called_with(file_path, 'w+')
        mock_files[file_path]().write.assert_called_with(self.DATASET_HEADERS + '\n')
        mock_files[file_path]().writelines.assert_called_with(lines[0:lines_per_dataset])

    @patch('os.path.exists', return_value=True)
    @patch('shutil.rmtree')
    @patch('os.makedirs')
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    @pytest.mark.parametrize('mock_files', [
        {BASE_DIR + '/' + DATASET_NAME: generate_csv_string(60),
         BASE_DIR + '/' + DIR_NAME + '/' + '1.csv': None,
         BASE_DIR + '/' + DIR_NAME + '/' + '2.csv': None}
    ], indirect=True)
    def test_case_5_new(self, mock_join, mock_makedirs, mock_rmtree, mock_exists, mock_files):
        data_divider = DatasetDivider(self.BASE_DIR, self.DATASET_NAME)
        data_divider.divide_dataset()

        dataset_path = self.BASE_DIR + '/' + self.DATASET_NAME
        data_divide_dir = self.BASE_DIR + '/' + self.DIR_NAME
        file_path_1 = data_divide_dir + '/' + '1.csv'
        file_path_2 = data_divide_dir + '/' + '2.csv'

        lines_per_dataset = 50

        oracle_data = generate_csv_string(60)

        lines = oracle_data.strip().split('\n')  # Use '\r\n' to split lines
        lines = [line + "\n" for line in lines[1:]]

        mock_rmtree.assert_called_with(data_divide_dir)

        mock_makedirs.assert_called_with(data_divide_dir)

        mock_files[dataset_path].assert_called_with(dataset_path, 'r')

        mock_files[file_path_1].assert_called_with(file_path_1, 'w+')
        mock_files[file_path_1]().write.assert_called_with(self.DATASET_HEADERS + '\n')
        mock_files[file_path_1]().writelines.assert_called_with(lines[0:lines_per_dataset])

        mock_files[file_path_2].assert_called_with(file_path_2, 'w+')
        mock_files[file_path_2]().write.assert_called_with(self.DATASET_HEADERS + '\n')
        mock_files[file_path_2]().writelines.assert_called_with(lines[lines_per_dataset:])

    @patch('os.path.exists', return_value=False)
    @patch('shutil.rmtree')
    @patch('os.makedirs')
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    @pytest.mark.parametrize('mock_files', [
        {BASE_DIR + '/' + DATASET_NAME: generate_csv_string(60),
         BASE_DIR + '/' + DIR_NAME + '/' + '1.csv': None,
         BASE_DIR + '/' + DIR_NAME + '/' + '2.csv': None}
    ], indirect=True)
    def test_case_6_new(self, mock_join, mock_makedirs, mock_rmtree, mock_exists, mock_files):
        data_divider = DatasetDivider(self.BASE_DIR, self.DATASET_NAME)
        data_divider.divide_dataset()

        dataset_path = self.BASE_DIR + '/' + self.DATASET_NAME
        data_divide_dir = self.BASE_DIR + '/' + self.DIR_NAME
        file_path_1 = data_divide_dir + '/' + '1.csv'
        file_path_2 = data_divide_dir + '/' + '2.csv'

        lines_per_dataset = 50

        oracle_data = generate_csv_string(60)

        lines = oracle_data.strip().split('\n')  # Use '\r\n' to split lines
        lines = [line + "\n" for line in lines[1:]]

        mock_makedirs.assert_called_with(data_divide_dir)

        mock_rmtree.assert_not_called()

        mock_files[dataset_path].assert_called_with(dataset_path, 'r')

        mock_files[file_path_1].assert_called_with(file_path_1, 'w+')
        mock_files[file_path_1]().write.assert_called_with(self.DATASET_HEADERS + '\n')
        mock_files[file_path_1]().writelines.assert_called_with(lines[0:lines_per_dataset])

        mock_files[file_path_2].assert_called_with(file_path_2, 'w+')
        mock_files[file_path_2]().write.assert_called_with(self.DATASET_HEADERS + '\n')
        mock_files[file_path_2]().writelines.assert_called_with(lines[lines_per_dataset:])

    @pytest.mark.parametrize('mock_op_fail', [None], indirect=True)
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    def test_case_7_new(self, mock_join, mock_op_fail):
        data_divider = DatasetDivider(3, self.DATASET_NAME)

        with pytest.raises(TypeError):
            data_divider.divide_dataset()

    @pytest.mark.parametrize('mock_op_fail', [None], indirect=True)
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    def test_case_8_new(self, mock_join, mock_op_fail):

        data_divider = DatasetDivider("test.<</path", self.DATASET_NAME)

        with pytest.raises(OSError):
            data_divider.divide_dataset()

    @pytest.mark.parametrize('mock_op_fail', [BASE_DIR + '/' + DATASET_NAME], indirect=True)
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    def test_case_9_new(self, mock_join, mock_op_fail):

        data_divider = DatasetDivider(self.BASE_DIR, self.DATASET_NAME)

        with pytest.raises(FileNotFoundError):
            data_divider.divide_dataset()