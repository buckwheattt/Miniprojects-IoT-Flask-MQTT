#data preparation

import pandas as pd
import glob

files = glob.glob("*.csv")
dfs = [pd.read_csv(f) for f in files]
df = pd.concat(dfs)

print(f"number of lines: {len(df)}")
df.head()

#-----------------------------------------------
#data to windows

import numpy as np

WINDOW_SIZE = 50
X = []
y = []

for i in range(0, len(df) - WINDOW_SIZE, WINDOW_SIZE):
    window = df.iloc[i:i+WINDOW_SIZE]
    label = window['label'].mode()[0]
    features = window.drop('label', axis=1).values.flatten()
    X.append(features)
    y.append(label)

X = np.array(X)
y = np.array(y)

print("number of windows:", len(X))

#------------------------------------------------
#teaching model

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

preds = model.predict(X_test)
print(classification_report(y_test, preds))

#------------------------------------------------
#model import

import joblib
joblib.dump(model, "model.pkl")
