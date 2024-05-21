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
            geojson_data = gpd.read_file("indonesia-prov.geojson")
            
        st.markdown(geojson_data.head())
        bounds = geojson_data.total_bounds
        [y_map, x_map] = [geojson_data.centroid.y.mean(), geojson_data.centroid.x.mean()]
        m = folium.Map(location=[y_map, x_map],  tiles = 'CartoDB positron', zoom_start=4)
        # m.fit_bounds([[bounds[0],bounds[1]], [bounds[2],bounds[3]]])
        merged_gdf = geojson_data.merge(base_df, left_on='Propinsi', right_on='PETA_REF', how='outer')
        print(merged_gdf.head())
        folium.Choropleth(
            geo_data=merged_gdf,
            name="choropleth",
            data=merged_gdf,
            columns= ["PETA_REF","PAD"],
            key_on="feature.id",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Percobaan").add_to(m)

        #folium.LayerControl().add_to(m)

        # folium.GeoJson(geojson_data).add_to(m)
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
