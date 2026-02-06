# 🦠 Pharma Dashboard – Analyse des ventes pharmaceutiques

Ce projet consiste en la création d’un **dashboard interactif** permettant d’analyser les ventes de produits pharmaceutiques selon différentes dimensions temporelles et commerciales.  
Il a été réalisé dans le cadre **d'aider une pharmacie** et s’appuie sur **Python, Pandas et Streamlit**.

---

## 🎯 Objectifs du projet

- Visualiser l’évolution du chiffre d’affaires dans le temps  
- Identifier les **produits moteurs** et les produits à faible contribution  
- Analyser la **saisonnalité des ventes** (mois forts / périodes creuses)  
- Proposer une aide à la décision pour :
  - le pharmacien (gestion des stocks)
  - le responsable commercial
  - le dirigeant

---

## 🧱 Structure des données

Le projet utilise plusieurs fichiers CSV issus d’exports Excel :

- `Pharma_Ventes_Daily.csv` → ventes journalières  
- `Pharma_Ventes_Weekly.csv` → ventes hebdomadaires  
- `Pharma_Ventes_Monthly.csv` → ventes mensuelles  
- `Pharma_Ventes_Hourly.csv` → ventes horaires  

Chaque fichier contient les ventes par produit (M01AB, N02BE, N05B, etc.) ainsi qu’une dimension temporelle.

---

## 🛠️ Technologies utilisées

- **Python 3**
- **Pandas** : traitement et agrégation des données
- **Streamlit** : création du dashboard interactif
- **GitHub Codespaces / VS Code**

---

## 📊 Fonctionnalités du dashboard

- Sélection du **niveau d’analyse** (journalier / mensuel)
- Visualisation du **chiffre d’affaires par année**
- Analyse du **chiffre d’affaires par produit et par mois**
- Mise en évidence de la **saisonnalité**
- Calcul de la **proportion des ventes par produit**
- Identification des produits les plus vendus

---
