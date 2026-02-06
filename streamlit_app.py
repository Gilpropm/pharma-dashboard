# ==============================
# Importation des bibliothèques
# ==============================

# Streamlit : permet de créer l’interface web du dashboard
import streamlit as st

# Pandas : permet de lire et manipuler les données (CSV, Excel, calculs)
import pandas as pd

# Plotly : permet de créer des graphiques interactifs
import plotly.express as px


# ==============================
# Titre principal du dashboard
# ==============================

# Titre affiché en haut de l’application
st.title("🦠 Pharma Dashboard")

# Slogan : message court, engageant, orienté usage quotidien
st.write(
    "Pilotez vos ventes pharmaceutiques au quotidien, "
    "identifiez les produits clés et anticipez les périodes critiques, car votre travail sauve des vies"
)


# ==============================
# Chargement des données
# ==============================

# Chargement des ventes journalières depuis le fichier CSV
df_daily = pd.read_csv("Pharma_Ventes_Daily.csv")

# Chargement des ventes mensuelles depuis le fichier CSV
df_monthly = pd.read_csv("Pharma_Ventes_Monthly.csv")


# ==============================
# Calcul du chiffre d'affaires par an
# ==============================

# Liste des colonnes produits (ventes)
produits = ["M01AB", "M01AE", "N02BA", "N02BE", "N05B", "N05C", "R03", "R06"]

# Création d'une nouvelle colonne "CA_total"
# qui correspond à la somme des ventes de tous les produits
df_monthly["CA_total"] = df_monthly[produits].sum(axis=1)

# Conversion de la colonne "datum" en datetime
df_monthly["datum"] = pd.to_datetime(df_monthly["datum"], format="%d/%m/%Y")

# Extraction de l'année
df_monthly["Year"] = df_monthly["datum"].dt.year

# Agrégation du chiffre d'affaires par année
# (somme du CA pour chaque année)
ca_par_an = (
    df_monthly
    .groupby("Year")["CA_total"]
    .sum()
    .reset_index()
)


# ==============================
# Affichage du graphique
# ==============================

# Titre de la section
st.subheader("📈 Chiffre d’affaires par année")

# Affichage du graphique en barres
st.bar_chart(
    data=ca_par_an,
    x="Year",
    y="CA_total"
)


# ============================================
# SAISONNALITÉ : CA PAR PRODUIT ET PAR MOIS
# (Graphique en barres avec mois en lettres)
# ============================================

# Liste des produits
produits = ["M01AB", "M01AE", "N02BA", "N02BE", "N05B", "N05C", "R03", "R06"]

# Conversion de la colonne date en format datetime
df_monthly["datum"] = pd.to_datetime(df_monthly["datum"])

# Dictionnaire pour mapper les numéros de mois aux noms français
mois_francais = {
    1: "janvier", 2: "février", 3: "mars", 4: "avril",
    5: "mai", 6: "juin", 7: "juillet", 8: "août",
    9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre"
}

# Création d'une colonne "Mois" en lettres (janvier, février, etc.)
df_monthly["Mois"] = df_monthly["datum"].dt.month.map(mois_francais)

# Ordre correct des mois (important pour l'affichage)
ordre_mois = [
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre"
]

# Convertir la colonne "Mois" en catégorie ordonnée
df_monthly["Mois"] = pd.Categorical(
    df_monthly["Mois"],
    categories=ordre_mois,
    ordered=True
)

# Calcul du chiffre d'affaires moyen par mois et par produit
df_saisonnalite = (
    df_monthly
    .groupby("Mois", observed=True)[produits]
    .mean()
)

# Titre de la section
st.subheader("📊 Saisonnalité du chiffre d’affaires par produit (mensuel)")

# Affichage du graphique en barres
st.bar_chart(df_saisonnalite)


# ==============================
# Proportion de vente par produit
# ==============================

# Calcul du total des ventes pour chaque produit
total_ventes_par_produit = df_monthly[produits].sum()

# Calcul de la proportion (pourcentage)
proportion_produits = (total_ventes_par_produit / total_ventes_par_produit.sum() * 100).round(2)

# Création d'un DataFrame pour afficher les résultats
df_proportion = pd.DataFrame({
    "Produit": proportion_produits.index,
    "Proportion (%)": proportion_produits.values
}).sort_values("Proportion (%)", ascending=False)

# Titre de la section
st.subheader("🏆 Proportion de ventes par produit")

# Création du diagramme en camembert avec Plotly
fig = px.pie(
    df_proportion,
    names="Produit",
    values="Proportion (%)",
    title="Proportion de ventes par produit"
)

# Affichage du diagramme
st.plotly_chart(fig, use_container_width=True)


# ============================================
# VARIATION DES VENTES PAR MOIS (2014-2019)
# ============================================

# Titre de la section
st.subheader("📈 Variation des ventes par mois (2014-2019)")

# Préparer les données
df_variation = df_monthly[["datum"] + produits].copy()
df_variation = df_variation.sort_values("datum")

# Filtrer les données entre 2014-01-01 et 2019-12-31
df_variation = df_variation[
    (df_variation["datum"] >= pd.to_datetime("2014-01-01")) &
    (df_variation["datum"] <= pd.to_datetime("2019-12-31"))
]

# Traiter la date du 31 janvier 2017 : faire la moyenne pour lisser
date_probleme = pd.to_datetime("2017-01-31")
df_probleme = df_variation[df_variation["datum"] == date_probleme]

if not df_probleme.empty:
    # Calculer la moyenne des 2 mois avant et après
    df_variation.loc[df_variation["datum"] == date_probleme, produits] = (
        df_variation.loc[df_variation["datum"] == date_probleme, produits].values[0] + 
        df_variation.loc[df_variation["datum"] < date_probleme, produits].iloc[-1].values +
        df_variation.loc[df_variation["datum"] > date_probleme, produits].iloc[0].values
    ) / 3

# Créer le graphique en aires empilées
fig = px.area(
    df_variation,
    x="datum",
    y=produits,
    labels={
        "datum": "Date (Année-Mois)",
        "value": "Ventes",
        "variable": "Produit"
    },
    title="Variation des ventes par mois (2014-2019)"
)

# Améliorer l'apparence avec des ticks tous les 3 mois
fig.update_xaxes(
    title_text="Date (Année-Mois)",
    tickformat="%Y-%m",
    tickmode="linear",
    dtick="M3",  # Un tick tous les 3 mois
    tickangle=45
)
fig.update_yaxes(title_text="Ventes totales")
fig.update_layout(
    hovermode='x unified',
    height=500
)

# Affichage du graphique
st.plotly_chart(fig, use_container_width=True)


# ============================================
# VENTE MOYENNE PAR MOIS
# ============================================

# Titre de la section
st.subheader("📅 Vente moyenne par mois")

# Créer une colonne pour le mois (1-12)
df_monthly_avg = df_monthly[["datum"] + produits].copy()
df_monthly_avg["Mois"] = df_monthly_avg["datum"].dt.month
df_monthly_avg["Mois_Nom"] = df_monthly_avg["datum"].dt.month.map(mois_francais)

# Calculer la moyenne par mois
df_mois_moyen = df_monthly_avg.groupby(["Mois", "Mois_Nom"])[produits].mean().reset_index()
df_mois_moyen = df_mois_moyen.sort_values("Mois")

# Créer le graphique en barres groupées
fig_mois = px.bar(
    df_mois_moyen,
    x="Mois_Nom",
    y=produits,
    barmode="group",
    labels={
        "Mois_Nom": "Mois",
        "value": "Ventes moyennes",
        "variable": "Produit"
    },
    title="Vente moyenne par mois (tous les ans confondus)"
)

fig_mois.update_xaxes(title_text="Mois")
fig_mois.update_yaxes(title_text="Ventes moyennes")
fig_mois.update_layout(height=500, hovermode='x unified')

# Affichage du graphique
st.plotly_chart(fig_mois, use_container_width=True)


# ==============================
# Sélecteur du niveau d'analyse
# ==============================

# Menu déroulant permettant à l'utilisateur de choisir
# le niveau d'analyse (journalier ou mensuel)
niveau = st.selectbox(
    "Choisir le niveau d'analyse",
    ["Journalier", "Mensuel"]
)


# ==============================
# Affichage des données
# ==============================

# Si l'utilisateur choisit l'analyse journalière
if niveau == "Journalier":
    
    # Affichage du tableau des ventes journalières
    st.dataframe(df_daily)

# Sinon (analyse mensuelle)
else:
    
    # Affichage du tableau des ventes mensuelles
    st.dataframe(df_monthly)
