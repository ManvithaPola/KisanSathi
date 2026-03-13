import os
import cv2
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from keras.models import model_from_json
from keras.optimizers import Adam
from sklearn.metrics import accuracy_score, confusion_matrix, r2_score
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split

# ===============================
# 1️⃣ CNN DISEASE MODEL EVALUATION
# ===============================

def load_cnn():
    with open("model/model.json", "r") as f:
        model = model_from_json(f.read())

    model.load_weights("model/model_weights.h5")
    model.compile(
        optimizer=Adam(),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model


def evaluate_cnn_images():
    print("\n===== CNN DISEASE MODEL =====")

    model = load_cnn()
    images = []
    image_files = []

    for file in os.listdir("testImages"):
        if file.lower().endswith(".jpg"):
            img = cv2.imread(os.path.join("testImages", file))
            img = cv2.resize(img, (64, 64))
            img = img.astype("float32") / 255.0
            images.append(img)
            image_files.append(file)

    X_test = np.array(images)
    preds = model.predict(X_test)
    predicted_classes = np.argmax(preds, axis=1)

    print("Total Test Images:", len(image_files))
    print("Predicted Class Indices:", predicted_classes)

    print("\n⚠️ Accuracy & confusion matrix require true labels.")
    print("Current folder contains unlabeled images.")


# ===============================
# 2️⃣ CROP YIELD MODEL (R² SCORE)
# ===============================

def evaluate_yield():
    print("\n===== CROP YIELD MODEL =====")

    dataset = pd.read_csv("Dataset/Crop_yield.csv")

    le = LabelEncoder()
    dataset['Crops'] = le.fit_transform(dataset['Crops'])

    dataset.fillna(dataset.mean(), inplace=True)

    y = dataset['yield'].values
    X = dataset.drop(['yield'], axis=1).values

    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    rf = RandomForestRegressor()
    rf.fit(X_train, y_train)

    preds = rf.predict(X_test)
    r2 = r2_score(y_test, preds)

    print("R² Score:", round(r2, 3))


# ===================================
# 3️⃣ FERTILIZER MODEL (ACCURACY)
# ===================================

def evaluate_fertilizer():
    print("\n===== FERTILIZER MODEL =====")

    dataset = pd.read_csv("Dataset/FertilizerPrediction.csv")

    label_encoders = {}
    for col in dataset.columns:
        if dataset[col].dtype == 'object':
            le = LabelEncoder()
            dataset[col] = le.fit_transform(dataset[col])
            label_encoders[col] = le

    y = dataset['Fertilizer Name'].values
    X = dataset.drop(['Fertilizer Name'], axis=1).values

    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    with open("model/fertilizer.pckl", "rb") as f:
        model = pickle.load(f)

    preds = model.predict(X_test)

    acc = accuracy_score(y_test, preds)
    cm = confusion_matrix(y_test, preds)

    print("Accuracy:", round(acc, 3))
    print("Confusion Matrix:\n", cm)


# ===============================
# MAIN
# ===============================

if __name__ == "__main__":
    evaluate_cnn_images()
    evaluate_yield()
    evaluate_fertilizer()
