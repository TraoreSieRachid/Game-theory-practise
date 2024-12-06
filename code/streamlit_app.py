import streamlit as st
import itertools
import matplotlib.pyplot as plt
import numpy as np
from graphviz import Digraph

# Partie I : Fonctions pour les jeux statiques
def jeu_statique(payoffs_j1, payoffs_j2):
    n_strategies_j1 = len(payoffs_j1)
    n_strategies_j2 = len(payoffs_j1[0])

    resultats = []
    for i in range(n_strategies_j1):
        for j in range(n_strategies_j2):
            payoff_j1 = payoffs_j1[i][j]
            payoff_j2 = payoffs_j2[i][j]

            if all(payoff_j1 >= payoffs_j1[k][j] for k in range(n_strategies_j1)) and \
               all(payoff_j2 >= payoffs_j2[i][l] for l in range(n_strategies_j2)):
                resultats.append((i + 1, j + 1))
    return resultats

def afficher_matrice(payoffs_j1, payoffs_j2, equilibres):
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(payoffs_j1, cmap="cool", alpha=0.8)
    axes[1].imshow(payoffs_j2, cmap="cool", alpha=0.8)

    for i in range(len(payoffs_j1)):
        for j in range(len(payoffs_j1[0])):
            axes[0].text(j, i, f"{payoffs_j1[i][j]}", ha="center", va="center", color="black")
            axes[1].text(j, i, f"{payoffs_j2[i][j]}", ha="center", va="center", color="black")
    
    for eq in equilibres:
        axes[0].scatter(eq[1] - 1, eq[0] - 1, color="red", s=100)
        axes[1].scatter(eq[1] - 1, eq[0] - 1, color="red", s=100)

    axes[0].set_title("Gains Joueur 1")
    axes[1].set_title("Gains Joueur 2")
    st.pyplot(fig)

# Partie II : Jeux dynamiques
def explorer_arbre(noeud, chemin):
    resultats = []
    if isinstance(noeud, dict):
        for action, sous_noeud in noeud.items():
            resultats.extend(explorer_arbre(sous_noeud, chemin + [action]))
    else:
        resultats.append((chemin, noeud))
    return resultats

def dessiner_arbre(arbre, nom="Arbre de jeu"):
    def ajouter_noeud(g, noeud, parent=None, action=None):
        if isinstance(noeud, dict):
            for act, sous_noeud in noeud.items():
                nouveau_noeud = f"{parent}_{act}" if parent else act
                g.node(nouveau_noeud, label=act)
                if parent:
                    g.edge(parent, nouveau_noeud, label=action if action else "")
                ajouter_noeud(g, sous_noeud, parent=nouveau_noeud, action=act)
        else:
            feuille = f"{parent}_resultat" if parent else "resultat"
            g.node(feuille, label=str(noeud), shape="box")
            g.edge(parent, feuille, label=action if action else "")

    g = Digraph(nom, format="png")
    ajouter_noeud(g, arbre)
    return g

# Streamlit App
st.set_page_config(page_title="Théorie des Jeux", page_icon="🎲", layout="wide")
st.title("Analyse de Théorie des Jeux")

# Onglets horizontaux
onglets = st.tabs([
    "Accueil",
    "Jeux Statique (Information Complète)",
    "Jeux Statique (Information Incomplète)",
    "Jeux Dynamique (Information Complète)",
    "Jeux Dynamique (Information Incomplète)",
    "Notions de Théorie des Jeux"
])

# Accueil
with onglets[0]:
    st.header("Bienvenue")
    st.write("Explorez les jeux classiques en théorie des jeux avec des visualisations et des analyses interactives.")

# Jeux Statique (Information Complète)
with onglets[1]:
    st.header("Jeux Statique à Information Complète")
    rows_j1 = st.number_input("Nombre de stratégies Joueur 1", min_value=2, max_value=10, value=2)
    cols_j2 = st.number_input("Nombre de stratégies Joueur 2", min_value=2, max_value=10, value=2)

    st.subheader("Matrice de gains pour Joueur 1")
    payoffs_j1 = []
    for i in range(rows_j1):
        row = st.text_input(f"Gains pour la stratégie {i+1} de Joueur 1 (séparés par des virgules)", value="0,0")
        payoffs_j1.append([int(x) for x in row.split(",")])

    st.subheader("Matrice de gains pour Joueur 2")
    payoffs_j2 = []
    for i in range(rows_j1):
        row = st.text_input(f"Gains pour la stratégie {i+1} de Joueur 2 (séparés par des virgules)", value="0,0")
        payoffs_j2.append([int(x) for x in row.split(",")])

    if st.button("Calculer les Équilibres de Nash"):
        equilibres = jeu_statique(payoffs_j1, payoffs_j2)
        afficher_matrice(payoffs_j1, payoffs_j2, equilibres)

# Jeux Statique (Information Incomplète)
with onglets[2]:
    st.header("Jeux Statique à Information Incomplète")
    st.write("Modèle et analyse des jeux avec des types et des probabilités.")

# Jeux Dynamique (Information Complète)
with onglets[3]:
    st.header("Jeux Dynamique à Information Complète")
    arbre_texte = st.text_area("Définissez l'arbre du jeu en format dictionnaire", value="{\n    'A': {\n        'AA': (3, 2),\n        'AB': {\n            'ABA': (0, 1),\n            'ABB': (4, 0)\n        }\n    },\n    'B': {\n        'BA': (1, 1),\n        'BB': {\n            'BBA': (2, 3),\n            'BBB': (0, 0)\n        }\n    }\n}")

    if st.button("Afficher l'arbre de jeu"):
        try:
            arbre = eval(arbre_texte)
            g = dessiner_arbre(arbre)
            st.graphviz_chart(g.source)
        except Exception as e:
            st.error(f"Erreur dans la définition de l'arbre : {e}")

# Jeux Dynamique (Information Incomplète)
with onglets[4]:
    st.header("Jeux Dynamique à Information Incomplète")
    st.write("Explorez des arbres de jeu où les joueurs ont des types inconnus avec des probabilités associées.")

# Notions de Théorie des Jeux
with onglets[5]:
    st.header("Notions de Théorie des Jeux")
    st.write("Découvrez les concepts clés de la théorie des jeux avec des illustrations.")
