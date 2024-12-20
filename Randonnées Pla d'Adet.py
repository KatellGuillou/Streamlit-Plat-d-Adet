import streamlit as st
import folium
from streamlit_folium import folium_static

# Configuration de la page
st.set_page_config(
    page_title="Randonnées St Lary",
    page_icon="🏔️",
    layout="wide"
)

# Titre
st.title("🏔️ Randonnées à St Lary")
st.subheader("Itinéraires en raquettes et porte-bébé")

# Données des randonnées
randonnees = [
    {
        "nom": "Plat d'Adet",
        "description": "Belle randonnée familiale accessible en raquettes et porte-bébé",
        "difficulte": "Facile",
        "duree": "2h30",
        "denivele": "300m",
        "points": [
            {"lat": 42.8167, "lon": 0.3167, "elev": 1600},
            # Ajoutez vos points GPS ici
        ]
    }
]

# Création de la carte
m = folium.Map(location=[42.8167, 0.3167], zoom_start=12)

# Ajout des randonnées sur la carte
for rando in randonnees:
    points = [(p["lat"], p["lon"]) for p in rando["points"]]
    
    # Tracé de l'itinéraire
    folium.PolyLine(
        points,
        weight=3,
        color='red',
        popup=rando["nom"]
    ).add_to(m)
    
    # Marqueurs début/fin
    folium.Marker(
        points[0],
        popup=f"Début: {rando['nom']}",
        icon=folium.Icon(color='green')
    ).add_to(m)
    
    folium.Marker(
        points[-1],
        popup=f"Fin: {rando['nom']}",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Création de deux colonnes
col1, col2 = st.columns([2, 1])

with col1:
    # Affichage de la carte
    folium_static(m)

with col2:
    # Sélection de la randonnée
    selected_rando = st.selectbox(
        "Sélectionnez une randonnée",
        [rando["nom"] for rando in randonnees]
    )
    
    # Affichage des détails
    for rando in randonnees:
        if rando["nom"] == selected_rando:
            st.write("### Détails")
            st.write(f"**Difficulté:** {rando['difficulte']}")
            st.write(f"**Durée:** {rando['duree']}")
            st.write(f"**Dénivelé:** {rando['denivele']}")
            st.write("**Description:**")
            st.write(rando["description"])

# Footer
st.markdown("---")
st.markdown("*Fait avec ❤️ pour les randonneurs en famille*")
