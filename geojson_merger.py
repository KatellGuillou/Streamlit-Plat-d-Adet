import streamlit as st
import geopandas as gpd
import pandas as pd
from shapely.ops import unary_union
import json
import folium
from streamlit_folium import folium_static

# Configuration de la page
st.set_page_config(page_title="GeoJSON Combiner", layout="wide")

# Titre et description
st.title("GeoJSON and CSV Feature Combiner")

st.markdown("""
### Key Benefits:
- Simplifiez vos workflows géospatiaux en convertissant facilement entre CSV et GeoJSON
- Visualisez instantanément vos données géographiques
- Combinez plusieurs caractéristiques géométriques en une seule forme
""")

# Fonction pour afficher la carte
def display_map(gdf):
    # Créer une carte centrée sur les données
    m = folium.Map(location=[gdf.geometry.centroid.y.mean(), 
                           gdf.geometry.centroid.x.mean()],
                  zoom_start=11)
    
    # Ajouter les données GeoJSON à la carte
    folium.GeoJson(
        gdf.__geo_interface__,
        style_function=lambda x: {'fillColor': 'blue',
                                'color': 'blue',
                                'weight': 1,
                                'fillOpacity': 0.1}
    ).add_to(m)
    
    return m

# Zone de téléchargement
uploaded_files = st.file_uploader(
    "Déposez vos fichiers GeoJSON ici",
    type=['geojson', 'json'],
    accept_multiple_files=True
)

if uploaded_files:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Données originales")
        # Liste pour stocker tous les GeoDataFrames
        gdfs = []
        
        for uploaded_file in uploaded_files:
            try:
                gdf = gpd.read_file(uploaded_file)
                gdfs.append(gdf)
                st.success(f"✅ {uploaded_file.name} chargé avec succès!")
                
                # Afficher la carte des données originales
                st.write(f"Aperçu de {uploaded_file.name}:")
                m = display_map(gdf)
                folium_static(m, width=400)
                
            except Exception as e:
                st.error(f"❌ Erreur lors du chargement de {uploaded_file.name}: {str(e)}")
    
    with col2:
        st.subheader("Résultat de la combinaison")
        if gdfs and st.button("Combiner les caractéristiques"):
            try:
                # Combiner tous les GeoDataFrames
                combined_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))
                
                # Fusionner les géométries
                combined_geometry = unary_union(combined_gdf.geometry)
                
                # Créer un nouveau GeoDataFrame avec la géométrie combinée
                result_gdf = gpd.GeoDataFrame(geometry=[combined_geometry])
                
                # Afficher la carte du résultat
                m_result = display_map(result_gdf)
                folium_static(m_result, width=400)
                
                # Convertir en GeoJSON pour le téléchargement
                result_json = result_gdf.to_json()
                
                # Bouton de téléchargement
                st.download_button(
                    label="📥 Télécharger le résultat (GeoJSON)",
                    data=result_json,
                    file_name="combined_features.geojson",
                    mime="application/json"
                )
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la combinaison: {str(e)}")

# Ajouter des informations d'aide
with st.expander("ℹ️ Guide d'utilisation"):
    st.markdown("""
    1. Téléchargez un ou plusieurs fichiers GeoJSON
    2. Visualisez les données sur la carte
    3. Cliquez sur 'Combiner les caractéristiques' pour fusionner
    4. Téléchargez le résultat
    """)
