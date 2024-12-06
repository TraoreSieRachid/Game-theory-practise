# Travail de Maison - Théorie des Jeux avec Streamlit
# Objectif : Implémenter et analyser des jeux classiques en théorie des jeux à l'aide d'une application Streamlit.

import streamlit as st
import nashpy as nash
import numpy as np

# Partie I : Jeux statiques avec Nashpy
def jeu_statique(payoffs_j1, payoffs_j2):
    """
    Calcule les équilibres de Nash à l'aide de Nashpy.
    payoffs_j1: Matrice de gains pour le Joueur 1 (liste de listes).
    payoffs_j2: Matrice de gains pour le Joueur 2 (liste de listes).
    Retourne les équilibres de Nash sous forme de liste.
    """
    jeu = nash.Game(np.array(payoffs_j1), np.array(payoffs_j2))
    return list(jeu.support_enumeration())

# Partie II : Jeux dynamiques
# Non implémenté avec des bibliothèques spécifiques dans ce cas

# Streamlit App
st.set_page_config(page_title="Théorie des Jeux", page_icon="🎲", layout="wide")
st.title("Analyse de Théorie des Jeux")

# Onglets horizontaux
onglets = st.tabs(["Accueil", "Jeux Statique", "Jeux Dynamique", "Notions de Théorie des Jeux"])

with onglets[0]:
    st.header("Bienvenue")
    st.write("Cette application permet d'analyser des jeux en théorie des jeux. Utilisez les onglets pour naviguer entre les sections :")
    st.markdown("- **Jeux Statique** : Trouver les équilibres de Nash pour une matrice de gains donnée.")
    st.markdown("- **Jeux Dynamique** : Explorer un arbre de jeu défini par l'utilisateur.")
    st.markdown("- **Notions de Théorie des Jeux** : Découvrir les concepts clés.")

with onglets[1]:
    st.header("Jeux Statique : Équilibres de Nash avec Nashpy")
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
        try:
            equilibres = jeu_statique(payoffs_j1, payoffs_j2)
            if equilibres:
                st.write("Équilibres de Nash trouvés :")
                for eq in equilibres:
                    st.write(f"Joueur 1 : {eq[0]}, Joueur 2 : {eq[1]}")
            else:
                st.write("Aucun équilibre trouvé.")
        except Exception as e:
            st.error(f"Erreur dans le calcul des équilibres : {e}")

with onglets[2]:
    st.header("Jeux Dynamiques : Exploration de l'arbre")
    st.write("Cette section peut être enrichie à l'avenir avec des bibliothèques comme Gambit pour une analyse plus poussée des arbres de jeu.")

with onglets[3]:
    st.header("Notions de Théorie des Jeux")
    st.write("La théorie des jeux est une branche des mathématiques qui analyse les interactions stratégiques entre des agents rationnels.")
    st.subheader("Équilibre de Nash")
    st.write("Un équilibre de Nash est une situation où aucun joueur ne peut améliorer son gain en changeant unilatéralement de stratégie.")
    st.subheader("Jeux Dynamiques")
    st.write("Les jeux dynamiques modélisent des décisions séquentielles où les joueurs agissent à tour de rôle en observant les actions précédentes.")
    st.subheader("Applications")
    st.write("La théorie des jeux est utilisée en économie, biologie, politique, informatique, etc.")
