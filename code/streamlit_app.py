# Travail de Maison - Théorie des Jeux avec Streamlit
# Objectif : Implémenter et analyser des jeux classiques en théorie des jeux à l'aide d'une application Streamlit.

import streamlit as st
import itertools

# Partie I : Jeux statiques
def jeu_statique(payoffs_j1, payoffs_j2):
    """
    payoffs_j1: Matrice de gains pour le Joueur 1 (liste de listes).
    payoffs_j2: Matrice de gains pour le Joueur 2 (liste de listes).
    Retourne les équilibres de Nash.
    """
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

# Partie II : Jeux dynamiques
def explorer_arbre(noeud, chemin):
    """
    Explore un arbre de jeu récursivement.
    noeud: Dictionnaire ou feuille de l'arbre.
    chemin: Chemin actuel dans l'arbre.
    Retourne une liste des chemins et gains.
    """
    resultats = []
    if isinstance(noeud, dict):
        for action, sous_noeud in noeud.items():
            resultats.extend(explorer_arbre(sous_noeud, chemin + [action]))
    else:
        resultats.append((chemin, noeud))
    return resultats

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
    st.header("Jeux Statique : Équilibres de Nash")
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
        if equilibres:
            st.write("Équilibres de Nash trouvés :")
            for eq in equilibres:
                st.write(f"Joueur 1 : Stratégie {eq[0]}, Joueur 2 : Stratégie {eq[1]}")
        else:
            st.write("Aucun équilibre de Nash trouvé.")

with onglets[2]:
    st.header("Jeux Dynamiques : Exploration de l'arbre")
    arbre_texte = st.text_area("Définissez l'arbre du jeu en format dictionnaire", value="{\n    'A': {\n        'AA': (3, 2),\n        'AB': {\n            'ABA': (0, 1),\n            'ABB': (4, 0)\n        }\n    },\n    'B': {\n        'BA': (1, 1),\n        'BB': {\n            'BBA': (2, 3),\n            'BBB': (0, 0)\n        }\n    }\n}")

    if st.button("Explorer l'arbre"):
        try:
            arbre = eval(arbre_texte)
            chemins = explorer_arbre(arbre, [])
            st.write("Chemins et gains dans l'arbre :")
            for chemin, gain in chemins:
                st.write(f"Chemin : {' -> '.join(chemin)}, Gains : {gain}")
        except Exception as e:
            st.error(f"Erreur dans la définition de l'arbre : {e}")

with onglets[3]:
    st.header("Notions de Théorie des Jeux")
    st.write("La théorie des jeux est une branche des mathématiques qui analyse les interactions stratégiques entre des agents rationnels.")
    st.subheader("Équilibre de Nash")
    st.write("Un équilibre de Nash est une situation où aucun joueur ne peut améliorer son gain en changeant unilatéralement de stratégie.")
    st.subheader("Jeux Dynamiques")
    st.write("Les jeux dynamiques modélisent des décisions séquentielles où les joueurs agissent à tour de rôle en observant les actions précédentes.")
    st.subheader("Applications")
    st.write("La théorie des jeux est utilisée en économie, biologie, politique, informatique, etc.")
