from datetime import datetime
import json
from turtle import pu
import folium
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

from PIL                      import Image
from plotly                   import express as px
from folium.plugins           import MarkerCluster
from streamlit_folium         import folium_static
from matplotlib.pyplot        import figimage
from distutils.fancy_getopt   import OptionDummy

st.set_page_config(page_title='Proyecto Final',
                    layout="wide",
                    page_icon=':eggplant:',
                    initial_sidebar_state="expanded")

st.title('DASHBOARD HOUSES IN KING COUNTRY USA 	:derelict_house_building:')
st.write('#### Diplomado en Ciencia de datos - Juan David Quecan')
st.write(' Este dashboard se realiza con el proposito de poner en practica todo lo visto durante el diplomado. Tambien como evidencia de proyecto de grado :apple:')

def get_dataContext(pUrl):
    pData = pd.read_csv(pUrl)
    return pData

def filters_grade(pData):
    ## Grafica 'grade' vs 'price'
    min_grade = int(pData['grade'].min())
    max_grade = int(pData['grade'].max())

    f_grade = st.sidebar.slider('Evaluacion', min_grade, max_grade, min_grade)
    df = pData.loc[pData['grade'] < f_grade]
    df = df[['grade', 'price']].groupby('grade').mean().reset_index()

    fig = px.bar(df, x='grade', y='price')
    st.plotly_chart(fig, use_container_width=True)
    ##fin

    ## Grafica 'price' vs 'sqft_living'
    min_sqft_living = int(pData['sqft_living'].min())
    max_sqft_living = int(pData['sqft_living'].max())

    st.sidebar.subheader('Area maxima de construccion (Pies Cuadrados')
    f_sqft_living = st.sidebar.slider('Area construida', min_sqft_living, max_sqft_living, min_sqft_living)
    df = pData.loc[pData['sqft_living'] < f_sqft_living]
    df = df[['sqft_living', 'price']].groupby('sqft_living').mean().reset_index()

    st.header('Precio promedio por area construida')

    fig = px.bar(df, x='sqft_living', y='price')
    st.plotly_chart(fig, use_container_width=True)
    ## fin
    
    ## Grafica 'yr_built' vs 'price'
    min_yr_build = int(pData['yr_built'].min())
    max_yr_build = int(pData['yr_built'].max())

    st.sidebar.subheader('Año maximo de renovacion')
    f_yr_build = st.sidebar.slider('Año de Construccion', min_yr_build, max_yr_build)
    df = pData.loc[pData['yr_built'] < f_yr_build]
    df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

    st.header('Precio promedio por año de construccion')

    fig = px.bar(df, x='yr_built', y='price')
    st.plotly_chart(fig, use_container_width=True)
    ## fin

    return None

def map_generate(pData):

    pData['level'] = pData['price'].apply( lambda x: '<320K' if x< 320000 else 
                                           '320K-450K' if ( x > 320000) & ( x < 450000) else
                                           '450K-650K' if ( x > 450000) & ( x < 645000) else '>650K' )

    pData['is_waterfront'] = pData['waterfront'].apply( lambda x: 'Si' if x == 1 else 'No' )

    price_limit = st.slider('Maximun Price', 75000, 540000,10000000)

    f_waterfront = st.selectbox(
        'Vista al agua',
        pData['is_waterfront'].unique().tolist())

    pData['date'] = pd.to_datetime(pData['date']).dt.strftime('%Y-%m-%d')
    min_date = datetime.strptime(pData['date'].min(), '%Y-%m-%d')
    max_date = datetime.strptime(pData['date'].max(), '%Y-%m-%d')

    f_date = st.sidebar.slider('Fecha', min_date, max_date, min_date)

    houses = pData[(pData['date']>=str(f_date)) & 
                (pData['price'] <= price_limit) & 
                (pData['is_waterfront'] == f_waterfront)][['id', 'lat', 'long', 'price', 'level']]

    fig = px.scatter_mapbox( houses, 
                                lat='lat', 
                                lon='long',
                                color='level', 
                                size='price', 
                                color_continuous_scale=px.colors.cyclical.IceFire,
                                size_max=15,
                                zoom=10 )

    fig.update_layout( mapbox_style='open-street-map' )
    fig.update_layout( height=600, margin={'r':0, 't':0, 'l':0, 'b':0} )
    st.plotly_chart(fig, use_container_width=True)

    return None

def metrics(pData):
    
    f_bathrooms = st.sidebar.selectbox('Numero maximo de baños',sorted(set(pData['bathrooms'].unique())))

    f_bedrooms = st.sidebar.selectbox('Numero maximo de habitaciones',sorted(set(pData['bedrooms'].unique())))

    col1, col2 = st.columns(2)

    col1.header('Casas por No de habitaciones')
    df = pData[pData['bedrooms'] < f_bedrooms]
    fig = px.histogram(df, x='bedrooms')
    col1.plotly_chart(fig, use_container_width=True)

    col2.header('Casas por No de baños')
    df = pData[pData['bathrooms'] < f_bathrooms]
    fig = px.histogram(df, x='bathrooms')
    col2.plotly_chart(fig, use_container_width=True)
    return None

if __name__ == '__main__':
    pUrl = 'https://raw.githubusercontent.com/juanquecan94/Diplomado/master/Aplicacion/Data/kc_house_data.csv'
    pData = get_dataContext(pUrl)

    ## Parametros
    filters_grade(pData)

    ## Mapa
    map_generate(pData)

    ## Metricas
    metrics(pData)
