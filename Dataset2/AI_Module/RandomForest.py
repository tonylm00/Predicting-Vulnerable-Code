import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def save_vocabulary(data, name_vocab):
    original_vocab = data.columns.tolist()

    # Save the column names (vocabulary)
    joblib.dump(original_vocab, name_vocab)

def train(csv_path, name_model, name_vocab):
    data = pd.read_csv(csv_path)
    data.columns = data.columns.str.strip()

    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
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

    # Esegui una cross-validation a 5-fold
    scores = cross_val_score(rf, X_train, y_train, cv=5)
    print(f"Cross-validation scores: {scores}")

    # Fai le predizioni
    y_pred = rf.predict(X_test)

    # Stampa il rapporto di classificazione
    print(classification_report(y_test, y_pred))

    # Matrice di confusione
    print(confusion_matrix(y_test, y_pred))

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

def predict_csv(input_csv_path, model_path, label_encoder_path, vocab_path):
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

    return predicted_classes.tolist()

if __name__ == '__main__':
    #train('../mining_results_asa/csv_ASA_final.csv', 'random_forest_ASA.pkl', 'vocab/original_vocab_ASA.pkl')
    #train('../mining_results_asa/csv_mining_final.csv', 'random_forest_TM.pkl', 'vocab/original_vocab_TM.pkl')
    train('../Software_Metrics/mining_results_sm_final.csv', 'random_forest_SM.pkl', 'vocab/original_vocab_SM.pkl')

    #print(predict_csv('../../Dataset2/mining_results/csv_mining_final_neg.csv', 'random_forest_TM.pkl', 'label_encoder.pkl', 'original_vocab_TM.pkl'))
    #print(predict_dict({'class':1, 'public':3, 'pasquale': 5}, 'random_forest_TM.pkl', 'label_encoder.pkl', 'original_vocab_TM.pkl'))


