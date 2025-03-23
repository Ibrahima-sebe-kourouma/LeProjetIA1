import streamlit as st
import numpy as np
import pickle
import pandas as pd



# Liste des colonnes utilisées lors de l'entraînement
model_columns = ['Region_South', 'Region_North', 'Region_Central', 'Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']

# Fonction pour saisir les données de vente
def input_Vente_features():
    with st.sidebar:
        # Entrée pour les quantités de café
        Robusta = st.slider('Robusta', 0, 30000, 22615)
        Arabica = st.slider('Arabica', 0, 30000, 5410)
        Espresso = st.slider('Espresso', 0, 20000, 7198)
        Lungo = st.slider('Lungo', 0, 5000, 3915)
        Latte = st.slider('Latte', 0, 5000, 1777)
        Cappuccino = st.slider('Cappuccino', 0, 10000, 5185)

        # Sélection de la région (optionnelle, ici c'est une variable binaire)
        Region_South = st.radio('Région', ['South', 'North', 'Central'])
        if Region_South == 'South':
            Region_South = 1
            Region_North = 0
            Region_Central = 0
        elif Region_South == 'North':
            Region_South = 0
            Region_North = 1
            Region_Central = 0
        else:
            Region_South = 0
            Region_North = 0
            Region_Central = 1

        # Organiser les données sous forme de dictionnaire
        data = {
            'Region_South': Region_South,
            'Region_North': Region_North,
            'Region_Central': Region_Central,
            'Robusta': Robusta,
            'Arabica': Arabica,
            'Espresso': Espresso,
            'Lungo': Lungo,
            'Latte': Latte,
            'Cappuccino': Cappuccino
        }

        # Convertir en DataFrame
        features = pd.DataFrame(data, index=[0])
        
    return features