import streamlit as st
import pandas as pd
import numpy as np
from model import pred_proba
from client import input_Vente_features
from pandas import read_csv
import matplotlib.pyplot as plt
import seaborn as sn


def main():
    st.set_page_config(page_title="Prédiction du Canal de Vente", page_icon=":coffee:")
    st.title(":red[Prédiction du Canal de Vente]")
    st.write(
        """
        # :orange[Application de prédiction pour le canal de vente]
        ## Cette application prédit si la vente se fait en ligne ou en magasin:
        """
    )

    # Sidebar to collect features
    st.sidebar.header("Entrer les caractéristiques de la vente :")
    analyse = input_Vente_features()  # Collecter les données de vente via les sliders
    st.write(analyse)  # Afficher les données entrées

    # Prédiction
    prediction,probas = pred_proba(analyse)
    
    if prediction == 1:
        st.write("## :green[Canal de vente : Online] :coffee:")
    else:
        st.write("## :red[Canal de vente : Store] :shopping_cart:")

    st.write(f"## Prédiction : Le canal de vente est : {'Online' if prediction == 1 else 'Store'}")
    st.write(f"Probabilité : {probas[1]*100:.2f}% (Online), {probas[0]*100:.2f}% (Store)")

    # --- Analysis and Visualization Sections ---
    menu = st.sidebar.selectbox("Navigation", ['Peek at the data', 'Visualisation', 'Rapport d''analyse'])

    fichier = 'BeansDataSet.csv'
    data = read_csv(fichier, header=0)
    patient = [f'Vente{i}' for i in range(len(data))]

    if menu == 'Peek at the data':
        st.subheader("Chargement des donnees")

        try:
            data.index = patient
            st.dataframe(data)
            st.subheader("Affichage des 5 premieres Vente :")
            st.dataframe(data.head())

        except Exception as e:
            st.error(f"erreur de lecture {e}") 

        # Number of items by class
        st.subheader("Nombre d'éléments par canal :")
        class_count = data.groupby('Channel').size()
        st.write(class_count)

        # Repartition des patients par classe
        st.subheader("Répartition des Ventes par canal :")
        fig, ax_class = plt.subplots(figsize=(6, 4))
        data['Channel'].value_counts().plot(kind='bar', color=['green', 'red'], ax=ax_class)
        ax_class.set_xlabel("class (0=Store, 1=Online)")
        st.pyplot(fig)

        # Statistiques descriptives
        st.subheader("Statistiques descriptives :")
        st.write(data.describe())

    elif menu == 'Visualisation':
        st.subheader("Visualisation des données")

        # Histogramme
        st.subheader('Histogramme des données')
        data.hist(bins=15, figsize=(12, 10), layout=(2,3))
        plt.suptitle("Histogramme des données")
        st.pyplot(plt.gcf())

        # Histogramme de la région
        st.subheader("Histogramme de la région")
        fig, ax_class = plt.subplots(figsize=(6, 4))
        ax_class.hist(data['Region'], bins=15, color='blue')
        st.pyplot(fig)

        # Matrice de corrélation
        st.subheader("Matrice de corrélation")
        data = pd.get_dummies(data)
        fig, ax_class = plt.subplots(figsize=(12, 8))
        sn.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax_class)
        st.pyplot(fig)

        #----------------------------------------------------------------
        st.subheader("Boite a moustache")
        data.plot(kind='box',layout=(3,3),subplots=True,sharex=False,sharey=False,figsize=(12,10))
        st.pyplot(plt.gcf())
        #----------------------------------------------------------------
        st.subheader("Graphe de densite")
        data.plot(kind='density',layout=(3,3),subplots=True,sharex=False,sharey=False,figsize=(12,10))
        st.pyplot(plt.gcf())
        #----------------------------------------------------------------
        st.subheader("Pairplot Pour les vente en magasin")
        fig=sn.pairplot(data,hue='Channel_Store', height=1.5)
        st.pyplot(fig)
        #----------------------------------------------------------------
        st.subheader("Pairplot pour les vente en ligne")
        fig=sn.pairplot(data,hue='Channel_Online', height=1.5)
        st.pyplot(fig)
        #----------------------------------------------------------------
        st.subheader("Pairplot pour les vente en ligne et les ventes en magasin")
        data['Channel'] = data[['Channel_Store', 'Channel_Online']].idxmax(axis=1)

        # Remplace les noms "Channel_Store" et "Channel_Online" par "Store" et "Online"
        data['Channel'] = data['Channel'].replace({'Channel_Store': 'Store', 'Channel_Online': 'Online'})

        # Pairplot avec une seule colonne catégorielle
        fig = sn.pairplot(data, hue='Channel', height=1.5)
        st.pyplot(fig)

    elif menu == 'Rapport d''analyse':
        st.subheader("Rapport d'analyse des données")
        st.write("""
            ## Résumé de l'analyse des données.
            
        """)


if __name__ == "__main__":
    main()
