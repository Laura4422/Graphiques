import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Titre de l'application
st.title("Manipulation de données et création de graphiques")

# Menu de sélection pour choisir le dataset
dataset_choice = st.selectbox("Quel dataset veux-tu utiliser ?", ['Flights', 'Planets', 'Taxis'])

# Chargement du dataset sélectionné
if dataset_choice == "Flights":
    df = sns.load_dataset("flights")
elif dataset_choice == "Planets":
    df = sns.load_dataset("planets")
else:
    df = sns.load_dataset("taxis")

# Affichage des données
st.subheader(f"Dataset sélectionné : {dataset_choice}")
num_rows = st.slider("Nombre de lignes à afficher :", min_value=1, max_value=50, value=10)
st.table(df.head(num_rows))

# Vérification des colonnes numériques
if not df.select_dtypes(include=['number']).empty:
    st.subheader("Création de Graphiques")

    # Choix des colonnes pour X et Y
    x_col = st.selectbox("Choisissez la colonne X :", df.columns)
    y_col = st.selectbox("Choisissez la colonne Y :", df.select_dtypes(include=['number']).columns)

    # Choix du type de graphique
    chart_type = st.radio("Type de graphique :", ["Bar Chart", "Scatter Chart", "Line Chart"])

    # Génération du graphique
    st.subheader(f"Graphique : {chart_type}")
    if chart_type == "Bar Chart":
        try:
            st.bar_chart(df.set_index(x_col)[y_col])
        except KeyError:
            st.error("Les colonnes choisies ne sont pas compatibles pour créer un graphique.")
    elif chart_type == "Scatter Chart":
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
        st.pyplot(fig)
    elif chart_type == "Line Chart":
        try:
            st.line_chart(df.set_index(x_col)[y_col])
        except KeyError:
            st.error("Les colonnes choisies ne sont pas compatibles pour créer un graphique.")

    # Option pour afficher la matrice de corrélation
    show_corr_matrix = st.checkbox("Afficher la matrice de corrélation")
    if show_corr_matrix:
        st.subheader("Matrice de Corrélation")
        corr_matrix = df.select_dtypes(include=['number']).corr()  # Calculer la matrice de corrélation
        st.write("Matrice de corrélation brute :")
        st.dataframe(corr_matrix)  # Afficher les valeurs sous forme de tableau

        # Visualisation sous forme de heatmap
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, ax=ax)
        st.pyplot(fig)
else:
    st.warning("Le dataset sélectionné ne contient pas de colonnes numériques pour créer une matrice de corrélation.")
