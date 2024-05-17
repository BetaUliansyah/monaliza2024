import pandas as pd
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import requests
import json

# set page config
st.set_page_config(
    page_title="Peta Analisis Keuangan Daerah",
    layout="wide",
    page_icon="🗺️",
    initial_sidebar_state="collapsed"
    )
    
# ------------
st.title("Peta Analisis Keuangan Daerah")
# ------------

with st.sidebar:
    st.subheader('Bergabung ke CAFDA!')
    st.markdown("""
    [web](https://s.id/cafda)
    [email](beta.uliansyah@pknstan.ac.id)
    [github](https://github.com/BetaUliansyah/)
    
    """)

# ------------
col1, col2 = st.columns([0.3, 0.7], gap='medium')

with col1:   
    # Selectbox Skala Data
    st.markdown('#### Skala')
    extent_list = ['Nasional', 'Provinsi', 'Kab/Kota']
    extent_analysis = st.selectbox('Pilih Skala', options=extent_list, key='extent')
       
    # ---------------------------------------
    st.markdown('### Lokasi')

    #pemdadf = pd.read_csv('509-pemda-2024.csv')
    base_df = pd.read_csv('dataset-monaliza - DATAFRAME.csv')
    
    # Selectbox for Province subset
    if extent_analysis == 'Nasional':
        province_list = ['Seluruh Provinsi se-Indonesia']
    else:
        province_list = list(base_df.sort_values(by='NAMA_PROVINSI').NAMA_PROVINSI.unique())
    province_analysis = st.selectbox('Pilih Provinsi', options=province_list, key='provinsi')
    
    # Selectbox for city subset
    if extent_analysis == 'Kab/Kota':
        city_list = list(base_df[(base_df.NAMA_PROVINSI == province_analysis)].sort_values(by='NAMA_PEMDA').NAMA_PEMDA.unique())
        city_list = list(base_df[(base_df.NAMA_PROVINSI == province_analysis)].sort_values(by='NAMA_PEMDA').NAMA_PEMDA.unique())
    elif extent_analysis == 'Provinsi':
        city_list = ['Seluruh Kab/Kota se-Provinsi']
    else:
        city_list = ['Seluruh Kab/Kota se-Indonesia']
    city_analysis = st.selectbox('Pilih Kab/Kota', options=city_list, key='pemda')
    # ---------------------------------------
    st.markdown('### Analisis')

    # Multi Select Pilihan Data
    data_list = ['APBD', 'DAU', 'DBH', 'DAK Fisik', 'DAK Nonfisik']
    data_analysis = st.multiselect('Pilih Data', options=data_list, key='data', default=data_list)

    # Selectbox for demographic normalizer
    normalizer_list = [None, 'Per KM persegi', 'Per Jumlah Penduduk', 'Per IKK']
    normalizer = st.selectbox('Normalisasi Data', options=normalizer_list, key='normalizer')
    # ---------------------------------------

    # getting the correct geometry address
    
    #if extent_analysis == 'National-wide':
    #    geom_URL = f'geom/ALL_{unit_analysis}.geojson'
    #else:
    #    geom_URL = f'geom/{unit_analysis}_BY_PROVINCE/{province_analysis}_{unit_analysis}.geojson'

    


with col2:
    tab1, tab2, tab3, tab4 = st.tabs(["peta", "grafik", "metadata", "unduh"])
    with tab1:
        with st.spinner('digambar dulu ya... '):
            geojson_file = open("kabkot.json")
            # geojson_file = open('indonesia-prov.geojson', 'r')
            geojson_data = json.load(geojson_file)

        
        m = folium.Map(location=[-6.2, 120],  tiles = 'CartoDB positron', zoom_start=4)
        folium.GeoJson(geojson_data).add_to(m)
        st_data = st_folium(m, use_container_width=True)
        
        
        '''
        cmap = 'OrRd'
        map = pivot_gdf.explore(column = pivot_gdf['val'],
                            cmap = cmap,
                            tiles = 'CartoDB positron',
                            #tiles = map_tile,
                            attr = "mapbox",
                            color = 'white',
                            tooltip = [f'NAMA_{unit_analysis}', 'RESULT'],
                            scheme = 'EqualInterval', 
                            k = 10, 
                            highlight = True, 
                            popup = True,
                            legend = True,
                            style_kwds = {'stroke':0.5,
                                            'color' : 'black',
                                            'weight' : 0.5,
                                            'fillOpacity' : 0.8
                                            }, 
                            legend_kwds = {'colorbar': False, 'caption': title, 'fmt':'{:,.0f}'}
                            )
        
        with st.container(border=True, height= 550):
            st_folium(map, 
                #center = (106.8,-6.8),
                returned_objects= [],
                #width= 1000, 
                height = 500, 
                use_container_width=True
                )
'''