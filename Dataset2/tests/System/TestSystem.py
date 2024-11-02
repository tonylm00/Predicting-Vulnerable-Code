import os
from time import sleep

import pytest
from pywinauto import Application, Desktop
from pywinauto.controls.uia_controls import ButtonWrapper
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

        Application().start('Perseverance.exe')

        sleep(6)

        app = Application().connect(title='Perseverance')

        print("APP:", dir(app))

        # Wait for CPU usage to lower, indicating the app is ready
        app.wait_cpu_usage_lower(threshold=5, timeout=20)

        yield app, test_path

        app.kill()

        os.remove(os.path.join(test_path, self.TEST_DATASET_NAME))

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

    def test_software_metrics(self, ):
        # Start notepad.exe and connect to it (when a new process is spawned).
        print(os.getcwd())
        # Kill the app.


        print('open windows: ', app.windows())

        # Connect to the main window, modifying with title or best_match as needed
        window = app.window(title="Perseverance")

        children = window.children()
        gui_elem = []
        for idx, child in enumerate(children):
            gui_elem.append(child)

        list_index = [
            self.UPLOAD_BUTTON,
            self.SOFTWARE_METRICS_CHECK_BOX_1,
            self.START_BUTTON,
            self.PREDICTIONS_DOWNLOAD_BUTTON
        ]

        elem_dict = self.get_gui_elements(window, list_index)
        upload_button = elem_dict[self.UPLOAD_BUTTON]
        software_metrics_button = elem_dict[self.SOFTWARE_METRICS_CHECK_BOX_1]
        start_button = elem_dict[self.START_BUTTON]
        predict_res_button = elem_dict[self.PREDICTIONS_DOWNLOAD_BUTTON]

        upload_button.click_input()

        sleep(4)

        load_csv_app = Application().connect(title='Load CSV')

        load_csv_window = load_csv_app.window(title="Load CSV")
        #load_csv_window.print_control_identifiers()

        send_keys('initial_dataset.csv')

        sleep(2)

        send_keys('^l')

        sleep(2)

        send_keys('C:\\Users\\Utente\\Documents\\UNISA-MAGISTRALE\\IGES\\progetti\\Perseverance\\prova_dataset')

        sleep(2)

        send_keys('{ENTER}')

        sleep(2)

        apri_button = load_csv_window.child_window(title="&Apri")
        apri_button.click_input()

        software_metrics_button.click_input()

        start_button.click_input()

        print(dir(predict_res_button))

        wait_until(240, 5, predict_res_button.is_visible, True)

        predict_res_button.click_input()

        send_keys('results')

        sleep(3)

        send_keys('^l')

        sleep(2)

        send_keys('C:\\Users\\Utente\\PycharmProjects\\Predicting-Vulnerable-Code\\Dataset2\\tests\\System')

        sleep(2)

        send_keys('{ENTER}')

        save_zip_app = Application().connect(title='Save ZIP file as')

        save_zip_window = save_zip_app.window(title="Save ZIP file as")
        save_zip_window.print_control_identifiers()

        salva_button = save_zip_window.child_window(title="&Salva", class_name="Button")
        salva_button.click_input()

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

        children = window.children()
        gui_elem = []
        for idx, child in enumerate(children):
            gui_elem.append(child)

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

        load_csv_app = Application().connect(title='Load CSV')

        load_csv_window = load_csv_app.window(title="Load CSV")
        # load_csv_window.print_control_identifiers()

        send_keys('test_dataset.csv')

        sleep(2)

        send_keys('^l')

        sleep(2)

        send_keys(test_path)

        sleep(2)

        send_keys('{ENTER}')

        sleep(2)

        apri_button = load_csv_window.child_window(title="&Apri")
        apri_button.click_input()

        sleep(2)

        start_button.click_input()

        sleep(4)

        error_dialog = app.Dialog.Static2

        assert error_dialog.exist
        assert error_dialog.window_text() == 'You must select at least one option'

    @pytest.mark.parametrize('manage_environment', [(True, False, 0, True)], indirect=True)
    def test_case_5(self, manage_environment):

        app, test_path = manage_environment

        # Connect to the main window, modifying with title or best_match as needed
        window = app.window(title="Perseverance")

        children = window.children()
        gui_elem = []
        for idx, child in enumerate(children):
            gui_elem.append(child)

        list_index = [
            self.UPLOAD_BUTTON,
            self.SOFTWARE_METRICS_CHECK_BOX_1,
            self.START_BUTTON,
            self.TEXT_MINING_CHECK_BOX,
            self.PREDICTIONS_DOWNLOAD_BUTTON
        ]

        elem_dict = self.get_gui_elements(window, list_index)
        upload_button = elem_dict[self.UPLOAD_BUTTON]
        software_metrics_box = elem_dict[self.SOFTWARE_METRICS_CHECK_BOX_1]
        text_mining_box = elem_dict[self.TEXT_MINING_CHECK_BOX]
        start_button = elem_dict[self.START_BUTTON]
        predict_res_button = elem_dict[self.PREDICTIONS_DOWNLOAD_BUTTON]

        upload_button.click_input()

        sleep(4)

        load_csv_app = Application().connect(title='Load CSV')

        load_csv_window = load_csv_app.window(title="Load CSV")
        # load_csv_window.print_control_identifiers()

        send_keys('test_dataset.csv')

        sleep(2)

        send_keys('^l')

        sleep(2)

        send_keys(test_path)

        sleep(2)

        send_keys('{ENTER}')

        sleep(2)

        apri_button = load_csv_window.child_window(title="&Apri")
        apri_button.click_input()

        sleep(2)

        software_metrics_box.click_input()
        text_mining_box.click_input()

        sleep(2)

        start_button.click_input()

        sleep(4)

        wait_until(240, 5, predict_res_button.is_visible, True)

        predict_res_button.click_input()

        send_keys('results.zip')

        sleep(3)

        send_keys('^l')

        sleep(2)

        send_keys(test_path)

        sleep(2)

        send_keys('{ENTER}')

        save_zip_app = Application().connect(title='Save ZIP file as')

        save_zip_window = save_zip_app.window(title="Save ZIP file as")
        save_zip_window.print_control_identifiers()

        salva_button = save_zip_window.child_window(title="&Salva", class_name="Button")
        salva_button.click_input()














