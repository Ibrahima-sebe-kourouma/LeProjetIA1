import streamlit as st
import numpy as np
import pickle


# Charger le modèle
with open('./BeansArbre.pkl', 'rb') as model_file:
    model_loaded = pickle.load(model_file)
# Fonction de prédiction
def pred_proba(data):
    # Convertir la donnée en un tableau numpy
    data_array = np.array([[
        data['Region_South'][0], 
        data['Region_North'][0], 
        data['Region_Central'][0], 
        data['Robusta'][0], 
        data['Arabica'][0], 
        data['Espresso'][0], 
        data['Lungo'][0], 
        data['Latte'][0], 
        data['Cappuccino'][0]
    ]])

    # Faire la prédiction avec le modèle
    prediction = model_loaded.predict(data_array)[0]
    probas = model_loaded.predict_proba(data_array)[0]


    return prediction,probas