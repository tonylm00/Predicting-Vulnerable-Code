import os

import pytest
from pandas.errors import EmptyDataError

from Dataset2.Main import Main


class TestPredictionIntegration:
    BASE_DIR = os.getcwd()

    @pytest.fixture(autouse=True)
    def setup(self):
        self.main = Main(self.BASE_DIR)

    def test_case_1(self):
        with pytest.raises(FileNotFoundError, match="File not found: invalid_vocab.pkl"):
            self.main.run_prediction("test.csv", "invalid_model.pkl", "invalid_label.pkl","invalid_vocab.pkl","output.csv")

    def test_case_2(self, create_temp_file):
        vocab_path = os.path.join(self.BASE_DIR, "vocab.pkl")
        create_temp_file(vocab_path, 'MaxEssential, SumEssential, CountLinesOfCode')
        with pytest.raises(KeyError):
            self.main.run_prediction("test.csv", "invalid_model.pkl", "invalid_label.pkl",vocab_path,"output.csv")


    def test_case_3(self):
        vocab_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "vocab", "original_vocab_TMASA.pkl")
        with pytest.raises(FileNotFoundError, match="r.*'invalid_model.pkl'"):
            self.main.run_prediction("test.csv", "invalid_model.pkl", "invalid_label.pkl", vocab_path,
                                     "output.csv")

    def test_case_4(self, create_temp_file):
        vocab_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "vocab", "original_vocab_TMASA.pkl")
        model_path = os.path.join(self.BASE_DIR, "model.pkl")
        create_temp_file(model_path, 'modello random forest')
        with pytest.raises(KeyError):
            self.main.run_prediction("test.csv", model_path, "invalid_label.pkl", vocab_path,
                                     "output.csv")

    def test_case_5(self):
        vocab_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "vocab", "original_vocab_TMASA.pkl")
        model_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "model", "random_forest_TMASA.pkl")
        with pytest.raises(FileNotFoundError, match="r.*'invalid_label.pkl'"):
            self.main.run_prediction("test.csv", model_path, "invalid_label.pkl", vocab_path,
                                     "output.csv")


    def test_case_6(self):
        vocab_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "vocab", "original_vocab_TMASA.pkl")
        model_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "model", "random_forest_TMASA.pkl")
        label_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "label_encoder.pkl")
        with pytest.raises(FileNotFoundError, match="r.*'test.csv'"):
            self.main.run_prediction("test.csv", model_path, label_path, vocab_path,
                                     "output.csv")

    def test_case_7(self, create_temp_file):
        vocab_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "vocab", "original_vocab_TMASA.pkl")
        model_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "model", "random_forest_TMASA.pkl")
        label_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "label_encoder.pkl")
        csv_input_path = os.path.join(self.BASE_DIR, "test.csv")
        create_temp_file(csv_input_path, "")

        with pytest.raises(EmptyDataError, match="No columns to parse from file"):
            self.main.run_prediction(csv_input_path, model_path, label_path, vocab_path,
                                     "output.csv")

    def test_case_8(self, create_temp_file):
        vocab_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "vocab", "original_vocab_TMASA.pkl")
        model_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "model", "random_forest_TMASA.pkl")
        label_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "label_encoder.pkl")
        csv_input_path = os.path.join(self.BASE_DIR, "test.csv")
        create_temp_file(csv_input_path, 'Colonna1,Colonna2,Colonna3\n1, 2, 3')

        with pytest.raises(KeyError):
            self.main.run_prediction(csv_input_path, model_path, label_path, vocab_path,
                                     "output.csv")

    def test_case_9(self, create_temp_file):
        vocab_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "vocab", "original_vocab_TMASA.pkl")
        model_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "model", "random_forest_TMASA.pkl")
        label_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "label_encoder.pkl")
        csv_input_path = os.path.join(self.BASE_DIR, "test.csv")
        output_path = os.path.join(self.BASE_DIR, "output.csv")
        create_temp_file(csv_input_path, 'Name,Colonna1,Colonna2,Colonna3\nfile.java,1,2,3')

        self.main.run_prediction(csv_input_path, model_path, label_path, vocab_path, output_path)
        assert os.path.exists(output_path)
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert content == 'Name,CLS\nfile.java,neg\n' or content == 'Name,CLS\nfile.java,pos\n'
        os.remove(output_path)

    def test_case_10(self, create_temp_file):
        vocab_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "vocab", "original_vocab_TMASA.pkl")
        model_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "model", "random_forest_TMASA.pkl")
        label_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "label_encoder.pkl")
        csv_input_path = os.path.join(self.BASE_DIR, "test.csv")
        output_path = os.path.join(self.BASE_DIR, "output.csv")
        create_temp_file(csv_input_path, 'Name,Colonna1,Colonna2,Colonna3\nfile.java,ciao,2,3')

        self.main.run_prediction(csv_input_path, model_path, label_path, vocab_path, output_path)
        assert os.path.exists(output_path)
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert content == 'Name,CLS\nfile.java,neg\n' or content == 'Name,CLS\nfile.java,pos\n'
        os.remove(output_path)

    def test_case_11(self, create_temp_file):
        vocab_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "vocab", "original_vocab_SM.pkl")
        model_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "model", "random_forest_SM.pkl")
        label_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "label_encoder.pkl")
        csv_input_path = os.path.join(self.BASE_DIR, "test.csv")
        output_path = os.path.join(self.BASE_DIR, "output.csv")
        create_temp_file(csv_input_path, 'Kind,Name,CountLineCode,CountDeclClass,CountDeclFunction,CountLineCodeDecl,SumEssential,SumCyclomaticStrict,MaxEssential,MaxCyclomaticStrict,MaxNesting\nFile,file.java,1,2,3,4,5,6,7,8,9')

        self.main.run_prediction(csv_input_path, model_path, label_path, vocab_path, output_path)
        assert os.path.exists(output_path)
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert content == 'Name,CLS\nfile.java,neg\n' or content == 'Name,CLS\nfile.java,pos\n'
        os.remove(output_path)

    def test_case_12(self, create_temp_file):
        vocab_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "vocab", "original_vocab_SM.pkl")
        model_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "model", "random_forest_SM.pkl")
        label_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "label_encoder.pkl")
        csv_input_path = os.path.join(self.BASE_DIR, "test.csv")
        output_path = os.path.join(self.BASE_DIR, "output.csv")
        create_temp_file(csv_input_path, 'Kind,Name,CountLineCode,CountDeclClass,CountDeclFunction,CountLineCodeDecl,SumEssential,SumCyclomaticStrict,MaxEssential,MaxCyclomaticStrict,MaxNesting\nFile,file.java,1,2,3,ciao,5,6,7,8,9')

        with pytest.raises(ValueError):
            self.main.run_prediction(csv_input_path, model_path, label_path, vocab_path, output_path)

    def test_case_13(self, create_temp_file):
        vocab_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "vocab", "original_vocab_SM.pkl")
        model_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "model", "random_forest_SMASA.pkl")
        label_path = os.path.join(os.path.dirname(os.path.dirname(self.BASE_DIR)), "AI_Module", "label_encoder.pkl")
        csv_input_path = os.path.join(self.BASE_DIR, "test.csv")
        output_path = os.path.join(self.BASE_DIR, "output.csv")
        create_temp_file(csv_input_path,'Kind,Name,CountLineCode,CountDeclClass,CountDeclFunction,CountLineCodeDecl,SumEssential,SumCyclomaticStrict,MaxEssential,MaxCyclomaticStrict,MaxNesting\nFile,file.java,1,2,3,4,5,6,7,8,9')

        with pytest.raises(ValueError):
            self.main.run_prediction(csv_input_path, model_path, label_path, vocab_path, output_path)
