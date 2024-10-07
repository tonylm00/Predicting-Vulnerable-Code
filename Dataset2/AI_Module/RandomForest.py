import os

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def save_vocabulary(data, name_vocab):
    original_vocab = data.columns.tolist()

    os.makedirs(os.path.dirname(name_vocab), exist_ok=True)

    joblib.dump(original_vocab, name_vocab)

def train(csv_path, name_model, name_vocab):
    data = pd.read_csv(csv_path)
    data.columns = data.columns.str.strip()

    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    if 'Name' in data.columns:
        data = data[~data['Name'].str.contains('9730cd6a3bbb481ee4e400b51952b537589c469d|d934c6e7430b7b98e43a0a085a2304bd31a75c3d|0c8366cb792227d484b9ca13e537037dd0cb57dc', case=False, na=False)]

    string_columns = data.select_dtypes(include='object').columns

    # Stampa i nomi delle colonne che contengono stringhe
    print("Colonne con valori di tipo stringa:", string_columns.tolist())

    if 'CLS_x' in data.columns:
        data.rename(columns={'CLS_x': 'CLS'}, inplace=True)
    if 'CLS_y' in data.columns:
        data.rename(columns={'CLS_y': 'CLS'}, inplace=True)

    if (data.columns == 'CLS').sum() > 1:
        # Rimuovi le colonne duplicate chiamate 'CLS', mantenendo solo la prima occorrenza
        data = data.loc[:, ~data.columns.duplicated()]

    label_encoder = LabelEncoder()
    data['CLS'] = label_encoder.fit_transform(data['CLS'])
    # Dividi il dataset in feature (X) e target (y)
    if "Kind" in data.columns:
        data = data.drop("Kind", axis=1)
    data = data.drop('Name', axis=1)

    X = data.drop('CLS', axis=1)
    y = data['CLS']

    save_vocabulary(X, name_vocab)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

    rf = RandomForestClassifier(n_estimators=100, max_depth=None, random_state=1)

    # Addestra il modello
    rf.fit(X_train, y_train)

    os.makedirs(os.path.dirname(name_model), exist_ok=True)

    # Salva il modello su un file
    joblib.dump(rf, name_model)
    joblib.dump(label_encoder, 'label_encoder.pkl')

def predict_dict(input_dict, model_path, label_encoder_path, vocab_path):
    # Converti il dizionario in DataFrame
    original_vocab = joblib.load(vocab_path)
    model = joblib.load(model_path)
    label_encoder = joblib.load(label_encoder_path)

    new_data_vector = np.zeros(len(original_vocab))

    # Fill the array by matching words from the dictionary with the original vocabulary
    for i, column_name in enumerate(original_vocab):
        if column_name in input_dict:
            new_data_vector[i] = input_dict[column_name]
        else:
            new_data_vector[i] = 0

    new_data_vector = new_data_vector.reshape(1, -1)

    # Effettua la predizione
    prediction_numeric = model.predict(new_data_vector)

    # Riconverti la predizione in pos o neg
    predicted_class = label_encoder.inverse_transform(prediction_numeric)

    return predicted_class[0]

def predict_csv(input_csv_path, model_path, label_encoder_path, vocab_path, path_csv):
    # Converti il dizionario in DataFrame
    original_vocab = joblib.load(vocab_path)
    model = joblib.load(model_path)
    label_encoder = joblib.load(label_encoder_path)

    df_new = pd.read_csv(input_csv_path)

    aligned_data = pd.DataFrame(0, index=df_new.index, columns=original_vocab)

    # Fill the aligned DataFrame with the values from df_new where the column names match
    for column in df_new.columns:
        if column in original_vocab:
            aligned_data[column] = df_new[column]

    X_new = aligned_data.to_numpy()

    # Make predictions for all rows
    predictions = model.predict(X_new)

    # Riconverti la predizione in pos o neg
    predicted_classes = label_encoder.inverse_transform(predictions)

    df = pd.DataFrame({'Name': df_new['Name'], 'CLS': predicted_classes})
    os.makedirs(os.path.dirname(path_csv), exist_ok=True)
    df.to_csv(path_csv, index=False)

    return predicted_classes.tolist()

if __name__ == '__main__':
    train('../mining_results_asa/csv_ASA_final.csv', 'model/random_forest_ASA.pkl', 'vocab/original_vocab_ASA.pkl')
    train('../mining_results/csv_mining_final.csv', 'model/random_forest_TM.pkl', 'vocab/original_vocab_TM.pkl')
    train('../Software_Metrics/mining_results_sm_final.csv', 'model/random_forest_SM.pkl',
          'vocab/original_vocab_SM.pkl')
    train('../Union/Union_TM_SM.csv', 'model/random_forest_TMSM.pkl', 'vocab/original_vocab_TMSM.pkl')
    train('../Union/Union_SM_ASA.csv', 'model/random_forest_SMASA.pkl', 'vocab/original_vocab_SMASA.pkl')
    train('../Union/Union_TM_ASA.csv', 'model/random_forest_TMASA.pkl', 'vocab/original_vocab_TMASA.pkl')
    train('../Union/3COMBINATION.csv', 'model/random_forest_3Combination.pkl', 'vocab/original_vocab_3Combination.pkl')

    #print(predict_csv('../../Dataset2/mining_results/csv_mining_final_neg.csv', 'random_forest_TM.pkl', 'label_encoder.pkl', 'original_vocab_TM.pkl'))
    #print(predict_dict({'class':1, 'public':3, 'pasquale': 5}, 'random_forest_TM.pkl', 'label_encoder.pkl', 'original_vocab_TM.pkl'))
