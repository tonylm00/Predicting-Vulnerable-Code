import configparser
import os
import zipfile
from time import sleep
import pytest
from pywinauto import Application
from pywinauto.keyboard import send_keys
from pywinauto.timings import wait_until
from Dataset2.tests.RepoMining.conftest import generate_csv_string

class TestSystem:
    START_BUTTON = 2
    PROGRESS_BAR_LABEL = 3
    PROGRESS_BAR = 4
    ANALYSIS_DOWNLOAD_BUTTON = 5
    PREDICTIONS_DOWNLOAD_BUTTON = 6
    SONAR_TOKEN_1 = 9
    SONAR_HOST = 10
    SONAR_TOKEN_2 = 12
    SONAR_PATH = 14
    SOFTWARE_METRICS_CHECK_BOX_1 = 16
    ASA_CHECK_BOX = 17
    SOFTWARE_METRICS_CHECK_BOX_2 = 18
    TEXT_MINING_CHECK_BOX = 19
    COMMIT_TXT_1 = 20
    REPO_TXT = 21
    COMMIT_TXT_2 = 23
    UPLOAD_BUTTON = 25
    CSV_SWITCH = 27

    TEST_DATASET_NAME = 'test_dataset.csv'
    TEST_ANALYSIS_NAME = 'analysis.zip'
    TEST_PREDICTIONS_NAME = 'predictions.zip'

    config = configparser.ConfigParser()
    config.read('config.ini')

    SONAR_TOKEN_TXT = config.get('SonarConfig', 'SONAR_TOKEN')
    SONAR_HOST_TXT = config.get('SonarConfig', 'SONAR_HOST')
    SONAR_PATH_TXT = config.get('SonarConfig', 'SONAR_PATH')

    @pytest.fixture
    def manage_environment(self, request):
        is_uploaded, is_empty, num_rows, is_well_formatted = request.param

        test_path = os.getcwd()

        print("CWD:", test_path)

        if is_uploaded:
            self.manage_test_dataset(is_empty, num_rows, is_well_formatted)

        print("set_up")
        os.chdir('..\..')
        print(os.getcwd())
        os.chdir('Runner')

        Application().start('Perseverance.exe', wait_for_idle=False)

        sleep(6)

        app = Application().connect(title='Perseverance', timeout=30)

        print("APP:", dir(app))

        # Wait for CPU usage to lower, indicating the app is ready
        app.wait_cpu_usage_lower(threshold=5, timeout=20)

        yield app, test_path

        app.kill()

        file_path = os.path.join(test_path, self.TEST_DATASET_NAME)

        if (os.path.exists(file_path)):
            os.remove(file_path)

        analyis_path = os.path.join(test_path, self.TEST_ANALYSIS_NAME)

        if(os.path.exists(analyis_path)):
            os.remove(analyis_path)

        prediction_path = os.path.join(test_path, self.TEST_PREDICTIONS_NAME)

        if(os.path.exists(prediction_path)):
            os.remove(prediction_path)

        os.chdir(test_path)

    def manage_test_dataset(self, is_empty, num_rows, is_well_formatted):
        print("manage_test")

        with open(self.TEST_DATASET_NAME, 'w+') as file:
            if not is_empty:
                if is_well_formatted:
                    data = generate_csv_string(num_rows, is_scb_absent=False)
                else:
                    data = generate_csv_string(num_rows, is_format_valid=False)

            else:
                data = ""
            file.write(data)

    def get_gui_elements(self, window, list_index=None):

        if list_index is None:
            list_index = [2, 3, 4, 5, 6, 10, 12, 14, 16, 17, 19, 20, 21, 25, 25]

        children = window.children()
        gui_elem = {}
        for idx, child in enumerate(children):
            if idx in list_index:
                gui_elem[idx] = child

        return gui_elem

    def load_csv_routine(self, path):
        load_csv_app = Application().connect(title='Load CSV')

        load_csv_window = load_csv_app.window(title="Load CSV")
        # load_csv_window.print_control_identifiers()

        send_keys('test_dataset.csv')

        sleep(2)

        send_keys('^l')

        sleep(2)

        send_keys(path)

        sleep(2)

        send_keys('{ENTER}')

        sleep(2)

        apri_button = load_csv_window.child_window(title="&Apri")
        apri_button.click_input()

    def save_zip_routine(self, app, file_name, path):
        send_keys(file_name)

        sleep(2)

        send_keys('^l')

        sleep(2)

        send_keys(path)

        sleep(2)

        send_keys('{ENTER}')

        save_zip_app = Application().connect(title='Save ZIP file as')

        save_zip_window = save_zip_app.window(title="Save ZIP file as")
        save_zip_window.print_control_identifiers()

        salva_button = save_zip_window.child_window(title="&Salva", class_name="Button")
        salva_button.click_input()

        sleep(5)

        success_dialog = app.Dialog

        exist_dialog = app.Dialog.exist

        success_text = app.Dialog.Static2.window_text()

        success_dialog.OK.click_input()

        sleep(2)

        file_path = os.path.join(path, file_name)

        # zip file handler
        zip = zipfile.ZipFile(file_path)

        return exist_dialog, success_text, zip

    @pytest.mark.parametrize('manage_environment', [(False, False, 0, False)], indirect=True)
    def test_case_1(self, manage_environment):

        app, test_path = manage_environment

        # Connect to the main window, modifying with title or best_match as needed
        window = app.window(title="Perseverance")

        list_index = [
            self.START_BUTTON
        ]

        elem_dict = self.get_gui_elements(window, list_index)
        start_button = elem_dict[self.START_BUTTON]

        start_button.click_input()

        error_dialog = app.Dialog.Static2

        assert error_dialog.exist
        assert error_dialog.window_text() == 'You must upload a CSV to continue'


    @pytest.mark.parametrize('manage_environment', [(True, True, 0, False)], indirect=True)
    def test_case_2(self, manage_environment):

        app, test_path = manage_environment

        # Connect to the main window, modifying with title or best_match as needed
        window = app.window(title="Perseverance")

        list_index = [
            self.UPLOAD_BUTTON,
            self.SOFTWARE_METRICS_CHECK_BOX_1,
            self.START_BUTTON,
            self.PREDICTIONS_DOWNLOAD_BUTTON
        ]

        elem_dict = self.get_gui_elements(window, list_index)
        upload_button = elem_dict[self.UPLOAD_BUTTON]
        start_button = elem_dict[self.START_BUTTON]

        upload_button.click_input()

        sleep(4)

        self.load_csv_routine(test_path)

        sleep(2)

        start_button.click_input()

        sleep(4)

        error_dialog = app.Dialog.Static2

        assert error_dialog.exist
        assert error_dialog.window_text() == 'You must select at least one option'

    @pytest.mark.parametrize('manage_environment', [(True, False, 5, False)], indirect=True)
    def test_case_3(self, manage_environment):

        app, test_path = manage_environment

        # Connect to the main window, modifying with title or best_match as needed
        window = app.window(title="Perseverance")

        list_index = [
            self.UPLOAD_BUTTON,
            self.TEXT_MINING_CHECK_BOX,
            self.ASA_CHECK_BOX,
            self.START_BUTTON,
            self.PREDICTIONS_DOWNLOAD_BUTTON,
            self.ANALYSIS_DOWNLOAD_BUTTON,
            self.SONAR_PATH,
            self.SONAR_HOST,
            self.SONAR_TOKEN_1
        ]

        elem_dict = self.get_gui_elements(window, list_index)
        upload_button = elem_dict[self.UPLOAD_BUTTON]
        asa_box = elem_dict[self.ASA_CHECK_BOX]
        text_mining_box = elem_dict[self.TEXT_MINING_CHECK_BOX]
        start_button = elem_dict[self.START_BUTTON]
        sonar_path = elem_dict[self.SONAR_PATH]
        sonar_host = elem_dict[self.SONAR_HOST]
        sonar_token = elem_dict[self.SONAR_TOKEN_1]
        analysis_download_button = elem_dict[self.ANALYSIS_DOWNLOAD_BUTTON]
        predict_res_button = elem_dict[self.PREDICTIONS_DOWNLOAD_BUTTON]

        upload_button.click_input()

        sleep(4)

        self.load_csv_routine(test_path)

        sleep(2)

        """asa_box.click_input()
        sleep(1)"""
        text_mining_box.click_input()
        sleep(1)

        """sonar_path.click_input(double=True)
        send_keys("^a")
        sonar_path.type_keys(self.SONAR_PATH_TXT)

        sonar_host.click_input(double=True)
        sonar_host.type_keys(self.SONAR_HOST_TXT)

        sonar_token.click_input(double=True)
        sleep(1)
        sonar_token.type_keys(self.SONAR_TOKEN_TXT)"""

        start_button.click_input()

        sleep(4)

        error_dialog = app.Dialog.Static2

        assert error_dialog.exist
        assert error_dialog.window_text() == 'Invalid header dataset'

    @pytest.mark.parametrize('manage_environment', [(True, False, 0, True)], indirect=True)
    def test_case_5(self, manage_environment):

        app, test_path = manage_environment

        # Connect to the main window, modifying with title or best_match as needed
        window = app.window(title="Perseverance")

        list_index = [
            self.UPLOAD_BUTTON,
            self.SOFTWARE_METRICS_CHECK_BOX_1,
            self.START_BUTTON,
            self.TEXT_MINING_CHECK_BOX,
            self.PREDICTIONS_DOWNLOAD_BUTTON,
            self.ANALYSIS_DOWNLOAD_BUTTON
        ]

        elem_dict = self.get_gui_elements(window, list_index)
        upload_button = elem_dict[self.UPLOAD_BUTTON]
        software_metrics_box = elem_dict[self.SOFTWARE_METRICS_CHECK_BOX_1]
        text_mining_box = elem_dict[self.TEXT_MINING_CHECK_BOX]
        start_button = elem_dict[self.START_BUTTON]
        analysis_download_button = elem_dict[self.ANALYSIS_DOWNLOAD_BUTTON]
        predict_res_button = elem_dict[self.PREDICTIONS_DOWNLOAD_BUTTON]

        upload_button.click_input()

        sleep(3)

        self.load_csv_routine(test_path)

        sleep(2)


        software_metrics_box.click_input()
        text_mining_box.click_input()

        sleep(2)

        start_button.click_input()

        wait_until(240, 5, predict_res_button.is_visible, True)

        analysis_download_button.click_input()

        sleep(2)

        exist_analysis_success_dialog, analysis_success_text, analysis_zip = self.save_zip_routine(app, self.TEST_ANALYSIS_NAME,
                                                                                                   test_path)
        predict_res_button.click_input()

        sleep(2)

        exist_prediction_success_dialog, prediction_success_text, prediction_zip = self.save_zip_routine(app, self.TEST_PREDICTIONS_NAME, test_path)

        assert exist_analysis_success_dialog
        assert 'File saved successfully' in analysis_success_text
        assert os.path.exists(os.path.join(test_path, self.TEST_ANALYSIS_NAME))
        assert analysis_zip.namelist() == ['repo_mining.log', 'csv_mining_final.csv', 'mining_results_sm_final.csv',
                                           'Union_TM_SM.csv']

        assert exist_prediction_success_dialog
        assert 'File saved successfully' in prediction_success_text
        assert os.path.exists(os.path.join(test_path, self.TEST_PREDICTIONS_NAME))
        assert len(prediction_zip.namelist())==0

    @pytest.mark.parametrize('manage_environment', [(True, False, 0, True)], indirect=True)
    def test_case_7(self, manage_environment):

        app, test_path = manage_environment

        # Connect to the main window, modifying with title or best_match as needed
        window = app.window(title="Perseverance")

        list_index = [
            self.UPLOAD_BUTTON,
            self.SOFTWARE_METRICS_CHECK_BOX_1,
            self.START_BUTTON,
            self.TEXT_MINING_CHECK_BOX,
            self.PREDICTIONS_DOWNLOAD_BUTTON,
            self.ANALYSIS_DOWNLOAD_BUTTON
        ]

        elem_dict = self.get_gui_elements(window, list_index)
        upload_button = elem_dict[self.UPLOAD_BUTTON]
        software_metrics_box = elem_dict[self.SOFTWARE_METRICS_CHECK_BOX_1]
        text_mining_box = elem_dict[self.TEXT_MINING_CHECK_BOX]
        start_button = elem_dict[self.START_BUTTON]
        analysis_download_button = elem_dict[self.ANALYSIS_DOWNLOAD_BUTTON]
        predict_res_button = elem_dict[self.PREDICTIONS_DOWNLOAD_BUTTON]

        upload_button.click_input()

        sleep(3)

        self.load_csv_routine(test_path)

        sleep(2)

        text_mining_box.click_input()

        sleep(2)

        start_button.click_input()

        wait_until(240, 5, predict_res_button.is_visible, True)

        analysis_download_button.click_input()

        sleep(2)

        exist_analysis_success_dialog, analysis_success_text, analysis_zip = self.save_zip_routine(app, self.TEST_ANALYSIS_NAME,
                                                                                                   test_path)
        predict_res_button.click_input()

        sleep(2)

        exist_prediction_success_dialog, prediction_success_text, prediction_zip = self.save_zip_routine(app, self.TEST_PREDICTIONS_NAME, test_path)

        assert exist_analysis_success_dialog
        assert 'File saved successfully' in analysis_success_text
        assert os.path.exists(os.path.join(test_path, self.TEST_ANALYSIS_NAME))
        assert analysis_zip.namelist() == ['repo_mining.log', 'csv_mining_final.csv']

        assert exist_prediction_success_dialog
        assert 'File saved successfully' in prediction_success_text
        assert os.path.exists(os.path.join(test_path, self.TEST_PREDICTIONS_NAME))
        assert len(prediction_zip.namelist())==0

    @pytest.mark.parametrize('manage_environment', [(False, False, 5, False)], indirect=True)
    def test_case_36(self, manage_environment):

        app, test_path = manage_environment

        # Connect to the main window, modifying with title or best_match as needed
        window = app.window(title="Perseverance")

        list_index = [
            self.CSV_SWITCH,
            self.TEXT_MINING_CHECK_BOX,
            self.ASA_CHECK_BOX,
            self.START_BUTTON,
            self.PREDICTIONS_DOWNLOAD_BUTTON,
            self.ANALYSIS_DOWNLOAD_BUTTON,
            self.SONAR_PATH,
            self.SONAR_HOST,
            self.SONAR_TOKEN_1
        ]

        elem_dict = self.get_gui_elements(window, list_index)
        csv_button = elem_dict[self.CSV_SWITCH]
        asa_box = elem_dict[self.ASA_CHECK_BOX]
        text_mining_box = elem_dict[self.TEXT_MINING_CHECK_BOX]
        start_button = elem_dict[self.START_BUTTON]
        sonar_path = elem_dict[self.SONAR_PATH]
        sonar_host = elem_dict[self.SONAR_HOST]
        sonar_token = elem_dict[self.SONAR_TOKEN_1]
        analysis_download_button = elem_dict[self.ANALYSIS_DOWNLOAD_BUTTON]
        predict_res_button = elem_dict[self.PREDICTIONS_DOWNLOAD_BUTTON]

        csv_button.click_input()

        sleep(2)

        asa_box.click_input()
        sleep(1)
        text_mining_box.click_input()
        sleep(1)

        sonar_path.click_input(double=True)
        send_keys("^a")
        sonar_path.type_keys("C:\\errorpath\sonar-scanner.bat")
        
        sonar_token.click_input(double=True)
        sleep(1)
        sonar_token.type_keys(self.SONAR_TOKEN_TXT)

        sonar_host.click_input(double=True)
        sonar_host.type_keys(self.SONAR_HOST_TXT)

        start_button.click_input()

        wait_until(240, 5, predict_res_button.is_visible, True)

        error_dialog = app.Dialog.Static2

        assert error_dialog.exist
        assert error_dialog.window_text() == 'Error in static analysis, check the logs!'

        app.Dialog.OK.click_input()

        sleep(2)

        analysis_download_button.click_input()

        sleep(2)

        exist_analysis_success_dialog, analysis_success_text, analysis_zip = self.save_zip_routine(app,
                                                                                                   self.TEST_ANALYSIS_NAME,
                                                                                                   test_path)
        predict_res_button.click_input()

        sleep(2)

        exist_prediction_success_dialog, prediction_success_text, prediction_zip = self.save_zip_routine(app,
                                                                                                         self.TEST_PREDICTIONS_NAME,
                                                                                                         test_path)

        assert exist_analysis_success_dialog
        assert 'File saved successfully' in analysis_success_text
        assert os.path.exists(os.path.join(test_path, self.TEST_ANALYSIS_NAME))
        assert analysis_zip.namelist() == ['asa.log', 'repo_mining.log', 'csv_mining_final.csv']

        assert exist_prediction_success_dialog
        assert 'File saved successfully' in prediction_success_text
        assert os.path.exists(os.path.join(test_path, self.TEST_PREDICTIONS_NAME))
        assert prediction_zip.namelist() == ['Predict_TM.csv']

    @pytest.mark.parametrize('manage_environment', [(False, False, 5, False)], indirect=True)
    def test_case_37(self, manage_environment):

        app, test_path = manage_environment

        # Connect to the main window, modifying with title or best_match as needed
        window = app.window(title="Perseverance")

        list_index = [
            self.CSV_SWITCH,
            self.TEXT_MINING_CHECK_BOX,
            self.ASA_CHECK_BOX,
            self.START_BUTTON,
            self.PREDICTIONS_DOWNLOAD_BUTTON,
            self.ANALYSIS_DOWNLOAD_BUTTON,
            self.SONAR_PATH,
            self.SONAR_HOST,
            self.SONAR_TOKEN_1
        ]

        elem_dict = self.get_gui_elements(window, list_index)
        csv_button = elem_dict[self.CSV_SWITCH]
        asa_box = elem_dict[self.ASA_CHECK_BOX]
        text_mining_box = elem_dict[self.TEXT_MINING_CHECK_BOX]
        start_button = elem_dict[self.START_BUTTON]
        sonar_path = elem_dict[self.SONAR_PATH]
        sonar_host = elem_dict[self.SONAR_HOST]
        sonar_token = elem_dict[self.SONAR_TOKEN_1]
        analysis_download_button = elem_dict[self.ANALYSIS_DOWNLOAD_BUTTON]
        predict_res_button = elem_dict[self.PREDICTIONS_DOWNLOAD_BUTTON]

        csv_button.click_input()

        sleep(2)

        asa_box.click_input()
        sleep(1)
        text_mining_box.click_input()
        sleep(1)

        sonar_path.click_input(double=True)
        send_keys("^a")
        sonar_path.type_keys(self.SONAR_PATH_TXT)

        sonar_token.click_input(double=True)
        sleep(1)
        sonar_token.type_keys("error_token")

        sonar_host.click_input(double=True)
        sonar_host.type_keys(self.SONAR_HOST_TXT)

        start_button.click_input()

        wait_until(240, 5, predict_res_button.is_visible, True)

        error_dialog = app.Dialog.Static2

        assert error_dialog.exist
        assert error_dialog.window_text() == 'Error in static analysis, check the logs!'

        app.Dialog.OK.click_input()

        sleep(2)

        analysis_download_button.click_input()

        sleep(2)

        exist_analysis_success_dialog, analysis_success_text, analysis_zip = self.save_zip_routine(app,
                                                                                                   self.TEST_ANALYSIS_NAME,
                                                                                                   test_path)
        predict_res_button.click_input()

        sleep(2)

        exist_prediction_success_dialog, prediction_success_text, prediction_zip = self.save_zip_routine(app,
                                                                                                         self.TEST_PREDICTIONS_NAME,
                                                                                                         test_path)

        assert exist_analysis_success_dialog
        assert 'File saved successfully' in analysis_success_text
        assert os.path.exists(os.path.join(test_path, self.TEST_ANALYSIS_NAME))
        assert analysis_zip.namelist() == ['asa.log', 'repo_mining.log', 'csv_mining_final.csv']

        assert exist_prediction_success_dialog
        assert 'File saved successfully' in prediction_success_text
        assert os.path.exists(os.path.join(test_path, self.TEST_PREDICTIONS_NAME))
        assert prediction_zip.namelist() == ['Predict_TM.csv']

    @pytest.mark.parametrize('manage_environment', [(False, False, 5, False)], indirect=True)
    def test_case_38(self, manage_environment):

        app, test_path = manage_environment

        # Connect to the main window, modifying with title or best_match as needed
        window = app.window(title="Perseverance")

        list_index = [
            self.CSV_SWITCH,
            self.TEXT_MINING_CHECK_BOX,
            self.ASA_CHECK_BOX,
            self.START_BUTTON,
            self.PREDICTIONS_DOWNLOAD_BUTTON,
            self.ANALYSIS_DOWNLOAD_BUTTON,
            self.SONAR_PATH,
            self.SONAR_HOST,
            self.SONAR_TOKEN_1
        ]

        elem_dict = self.get_gui_elements(window, list_index)
        csv_button = elem_dict[self.CSV_SWITCH]
        asa_box = elem_dict[self.ASA_CHECK_BOX]
        text_mining_box = elem_dict[self.TEXT_MINING_CHECK_BOX]
        start_button = elem_dict[self.START_BUTTON]
        sonar_path = elem_dict[self.SONAR_PATH]
        sonar_host = elem_dict[self.SONAR_HOST]
        sonar_token = elem_dict[self.SONAR_TOKEN_1]
        analysis_download_button = elem_dict[self.ANALYSIS_DOWNLOAD_BUTTON]
        predict_res_button = elem_dict[self.PREDICTIONS_DOWNLOAD_BUTTON]

        csv_button.click_input()

        sleep(2)

        asa_box.click_input()
        sleep(1)
        text_mining_box.click_input()
        sleep(1)

        sonar_path.click_input(double=True)
        send_keys("^a")
        sonar_path.type_keys(self.SONAR_PATH_TXT)

        sonar_token.click_input(double=True)
        sleep(1)
        sonar_token.type_keys(self.SONAR_TOKEN_TXT)

        sonar_host.click_input(double=True)
        sonar_host.type_keys("http://errorhost:9001")

        start_button.click_input()

        wait_until(240, 5, predict_res_button.is_visible, True)

        error_dialog = app.Dialog.Static2

        assert error_dialog.exist
        assert error_dialog.window_text() == 'Error in static analysis, check the logs!'

        app.Dialog.OK.click_input()

        sleep(2)

        analysis_download_button.click_input()

        sleep(2)

        exist_analysis_success_dialog, analysis_success_text, analysis_zip = self.save_zip_routine(app,
                                                                                                   self.TEST_ANALYSIS_NAME,
                                                                                                   test_path)
        predict_res_button.click_input()

        sleep(2)

        exist_prediction_success_dialog, prediction_success_text, prediction_zip = self.save_zip_routine(app,
                                                                                                         self.TEST_PREDICTIONS_NAME,
                                                                                                         test_path)

        assert exist_analysis_success_dialog
        assert 'File saved successfully' in analysis_success_text
        assert os.path.exists(os.path.join(test_path, self.TEST_ANALYSIS_NAME))
        assert analysis_zip.namelist() == ['asa.log', 'repo_mining.log', 'csv_mining_final.csv']

        assert exist_prediction_success_dialog
        assert 'File saved successfully' in prediction_success_text
        assert os.path.exists(os.path.join(test_path, self.TEST_PREDICTIONS_NAME))
        assert prediction_zip.namelist() == ['Predict_TM.csv']






















