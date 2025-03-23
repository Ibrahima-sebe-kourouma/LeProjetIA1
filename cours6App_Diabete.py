import streamlit as st
from pandas import read_csv
import pandas as pd
from datetime import date
from PIL import Image
from matplotlib import pyplot as plt
import scipy
import seaborn as sn

st.markdown(
        """
        <div style='text-align:center'>
        <h1> Analyse des donnees Diabete </h1>
        </div>
        """, unsafe_allow_html=True
    )

st.sidebar.title("Analyse du diabete avec pandas")
menu = st.sidebar.selectbox("Navigation", ['Peek at the data', 'Visualisation','Rapport d''analyse'])

fichier= 'BeansDataSet.csv'
data = read_csv(fichier,header=0)
patient = [f'Patient_{i}' for i in range (len(data))]


if menu == 'Peek at the data':
    st.subheader("Chargement des donnees")

    try:
        data.index = patient
        st.dataframe(data)
        st.subheader("Afficahge des 5 premieres patientes :")
        st.dataframe(data.head())

    except Exception as e:
        st.error(f"erreur de lecture {e}") 
    #----------------------------------------------------------------
    st.subheader("Nombre d'element par classe :")
    class_count = data.groupby('Channel').size()
    st.write(class_count)  
    #----------------------------------------------------------------
    st.subheader("Repartition des patientes par classe :")
    fig,ax_class=plt.subplots(figsize=(6,4))
    data['Channel'].value_counts().plot(kind='bar',color=['green','red'],ax=ax_class)
    ax_class.set_xlabel("class (0=Store, 1=Online)")
    st.pyplot(fig)
    #----------------------------------------------------------------
    st.subheader("statistique descriptive :")
    st.write(data.describe())
elif menu == 'Visualisation':
    st.subheader("Visualisation des donnees")
    st.subheader('--------------------------------------------------------')
    st.subheader("Histogramme")
    data.hist(bins=15,figsize=(12,10),layout=(2,4))
    plt.suptitle("Histogramme des donnees")
    st.pyplot(plt.gcf())
    #----------------------------------------------------------------
    st.subheader("Histogramme de Region")
    fig,ax_class=plt.subplots(figsize=(6,4))
    ax_class.hist(data['Region'],bins=15,color='blue')
    st.pyplot(fig)
    #----------------------------------------------------------------
    st.subheader("Histogramme de Robusta")
    fig,ax_class=plt.subplots(figsize=(6,4))
    ax_class.hist(data['Robusta'],bins=15,color='blue')
    st.pyplot(fig)
    #----------------------------------------------------------------
    st.subheader("Matrice de correlation")
    data = pd.get_dummies(data)
    fig,ax_class=plt.subplots(figsize=(12,8))
    sn.heatmap(data.corr(),annot=True,cmap='coolwarm',fmt='.2f',ax=ax_class)
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

elif menu=='Rapport d''analyse':
    st.subheader("Rapport d'analyse de donnees")
