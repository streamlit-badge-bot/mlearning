import streamlit as st
from sklearn import datasets
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd



st.title("Quick Greenhouse")

st.write("""
# Clasificación para la optimización de la producción de aguacates
Mediante el uso del machine learning, se desea obtener
el resultado de la clasificación de diversos factores ambientales
así como si son viables o no
""")

dataset_name = st.sidebar.selectbox("Select Dataset",("Clima","Humedad","PH"))

classffier_name = st.sidebar.selectbox("Select Classifier",("KNN","SVM","Random Forest"))

def get_dataset(dataset_name):
    if dataset_name == "Clima":
        data = datasets.load_iris()
    elif dataset_name == "Humedad":
        data = datasets.load_breast_cancer()
    else:
        data = datasets.load_wine()
    X = data.data
    y = data.target
    return X, y

X, y = get_dataset(dataset_name)
st.write("Tamaño del dataset",X.shape)
st.write("Numero de clases", len(np.unique(y)))

def add_paramete_ui(clf_name):
    params = dict()
    if clf_name == "KNN":
        K = st.sidebar.slider("K", 1, 15)
        params["K"] = K
    elif clf_name == "SVM":
        C = st.sidebar.slider("C", 0.01, 10.0)
        params["C"] = C
    else:
        max_depth = st.sidebar.slider("max_depth",2,15)
        n_estimators = st.sidebar.slider("n_estimators", 1 , 100)
        params["max_depth"] = max_depth
        params["n_estimators"] = n_estimators
    return params
params = add_paramete_ui(classffier_name)

def get_classifier(clf_name, params):
    if clf_name == "KNN":
        clf = KNeighborsClassifier(n_neighbors=params["K"])
    elif clf_name == "SVM":
        clf = SVC(C=params["C"])
    else:
        clf = RandomForestClassifier(n_estimators=params["n_estimators"],
                                     max_depth=params["max_depth"], random_state=1234)
    return clf

clf = get_classifier(classffier_name, params)

#Clasification model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1234)

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

acc = accuracy_score(y_test, y_pred)
st.write(f"Clasificación = {classffier_name}")
st.write(f"Precisión = {acc}")




#plot
pca = PCA(2)
X_projected = pca.fit_transform(X)

x1 = X_projected[:, 0]
x2 = X_projected[:, 1]

fig = plt.figure()
plt.scatter(x1,x2,c=y,alpha=00.8,cmap="viridis")
plt.xlabel("Caso positivo")
plt.ylabel("Caso negativo")
plt.colorbar()

#plt.show
st.pyplot()




