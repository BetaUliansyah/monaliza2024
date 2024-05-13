import pandas as pd
import streamlit as st
#import geopandas as gpd
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
    
    # Selectbox for smallest unit
    #if extent_analysis == 'Nasional':
    #    unit_list = ['PROVINSI', 'KAB_KOTA']
    #elif extent_analysis == 'Provinsi':
    #    unit_list = ['KAB_KOTA', 'KECAMATAN']
    #else: 
    #    unit_list = ['KECAMATAN', 'DESA_KELURAHAN']
    #unit_analysis = st.selectbox('Unit Analisis', options=unit_list, key='units')
    
    # ---------------------------------------
    st.markdown('### Lokasi')

    # Selectbox for Province subset
    if extent_analysis == 'Nasional':
        province_list = ['Seluruh Provinsi se-Indonesia']
    else:
        # province_list = list(base_df.sort_values(by='NAMA_PROVINSI').NAMA_PROVINSI.unique())
        province_list = pd.read_csv('https://raw.githubusercontent.com/rijdz/folium-maps-jakarta/master/ID_provinces.csv').iloc[:, 1]
    province_analysis = st.selectbox('Pilih Provinsi', options=province_list, key='provinsi')

    # Selectbox for city subset
    if extent_analysis == 'Kab/Kota':
        # city_list = list(base_df[base_df.NAMA_PROVINSI == province_analysis].sort_values(by='NAMA_KAB_KOTA').NAMA_KAB_KOTA.unique())
        city_list = ['Yogyakarta']
    else:
        #city_list = ['All Cities'] + list(base_df[base_df.NAMA_PROVINSI == province_analysis].sort_values(by='NAMA_KAB_KOTA').NAMA_KAB_KOTA.unique())
        city_list = ['Seluruh Kab/Kota']
    city_analysis = st.selectbox('cities', options=city_list, key='city')
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
            geojson_data = requests.get(
            #"https://geoservices.big.go.id/rbi/rest/services/INDEKS/RBI_StatusBatas_ProvKabKota/MapServer/layers?f=pjson",
            #"https://raw.githubusercontent.com/rijdz/folium-maps-jakarta/master/JK_regencies.json",
            #"https://geoservices.big.go.id/rbi/rest/services/BATASWILAYAH/RBI_2014_25K_ACEH01_BATASWILAYAH/MapServer/2?f=pjson",
            "https://raw.githubusercontent.com/ans-4175/peta-indonesia-geojson/master/indonesia-prov.geojson",
            verify=False).json()
        
        m = folium.Map(location=[-6.2, 120], zoom_start=4)
        folium.GeoJson(geojson_data).add_to(m)
        st_data = st_folium(m, use_container_width=True)
