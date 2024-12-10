import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

cwd = os.path.dirname(os.path.abspath(__file__))

# Load datasets
abortion_train = pd.read_csv(cwd + '\\data\\abortion_train.csv')
abortion_test = pd.read_csv(cwd + '\\data\\abortion_test.csv')

gun_control_train = pd.read_csv(cwd + '\\data\\gun_control_train.csv')
gun_control_test = pd.read_csv(cwd + '\\data\\gun_control_test.csv')

# Preprocess function to handle text and labels
def preprocess_data(train, test, text_column, label_column):
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train = vectorizer.fit_transform(train[text_column])
    y_train = train[label_column]
    
    X_test = vectorizer.transform(test[text_column])
    y_test = test[label_column]
    d
    return X_train, y_train, X_test, y_test

# Function to train SVM and evaluate
def train_and_evaluate_svm(X_train, y_train, X_test, y_test):
    model = SVC(kernel='linear', random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    return accuracy

# Abortion stance
X_train_abortion_stance, y_train_abortion_stance, X_test_abortion_stance, y_test_abortion_stance = preprocess_data(abortion_train, abortion_test, text_column='text', label_column='stance')

# Abortion persuasiveness
X_train_abortion_persuasion, y_train_abortion_persuasion, X_test_abortion_persuasion, y_test_abortion_persuasion = preprocess_data(abortion_train, abortion_test, text_column='text', label_column='persuasiveness')

# Gun control stance
X_train_gun_stance, y_train_gun_stance, X_test_gun_stance, y_test_gun_stance = preprocess_data(gun_control_train, gun_control_test, text_column='text', label_column='stance')

# Gun control persuasiveness
X_train_gun_persuasion, y_train_gun_persuasion, X_test_gun_persuasion, y_test_gun_persuasion = preprocess_data(gun_control_train, gun_control_test, text_column='text', label_column='persuasiveness')

# Function to train SVM and evaluate
def train_and_evaluate_svm(X_train, y_train, X_test, y_test):
    model = SVC(kernel='linear', random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    return accuracy

accuracy_abortion_stance = train_and_evaluate_svm(X_train_abortion_stance, y_train_abortion_stance, X_test_abortion_stance, y_test_abortion_stance)
print(f"Abortion Dataset (Stance) Accuracy: {accuracy_abortion_stance:.2f}")

accuracy_abortion_persuasion = train_and_evaluate_svm(X_train_abortion_persuasion, y_train_abortion_persuasion, X_test_abortion_persuasion, y_test_abortion_persuasion)
print(f"Abortion Dataset (Persuasiveness) Accuracy: {accuracy_abortion_persuasion:.2f}")

accuracy_gun_stance = train_and_evaluate_svm(X_train_gun_stance, y_train_gun_stance, X_test_gun_stance, y_test_gun_stance)
print(f"Gun Control Dataset (Stance) Accuracy: {accuracy_gun_stance:.2f}")

accuracy_gun_persuasion = train_and_evaluate_svm(X_train_gun_persuasion, y_train_gun_persuasion, X_test_gun_persuasion, y_test_gun_persuasion)
print(f"Gun Control Dataset (Persuasiveness) Accuracy: {accuracy_gun_persuasion:.2f}")
