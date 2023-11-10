import streamlit as st
import pandas as pd
import numpy as np
import eligible_loadfactor as elf

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_title="Bhinneka", page_icon=":reminder_ribbon:", layout="wide")

rute = pd.read_csv('routes.csv')

with st.container():
    st.markdown("<h1 style='text-align: center; color: black;'>Eligible Schedule & Number of Departures</h1>", unsafe_allow_html=True)

with st.container():
    origin = st.selectbox("Pick the origin", rute['origin_name'].unique())
    dayofweek = st.selectbox("Pick the day of week", ["Monday","Tuesday","Wednesday","Thursday",'Friday','Saturday','Sunday'])
    origin_kode = rute.loc[rute['origin_name'] == origin, 'origin'].unique()[0]
    table_to_show = st.selectbox("Pick the type of table to show", ['Detail','Compact'])


    if table_to_show == 'Detail':
        data_to_show = elf.all_eligible_schedule(origin_kode, dayofweek, table_to_show.lower())
        dict_col_name = {col:f'{col[:-1]}go' if col[-1] == 'x' else f'{col[:-1]}back' for col in data_to_show.columns}
        data_to_show.rename(columns=dict_col_name, inplace=True)

        data_to_show['total_penumpang_go'] = data_to_show['total_penumpang_go'].astype('int')
        data_to_show['total_penumpang_back'] = data_to_show['total_penumpang_back'].fillna(0).astype('int')
        
        data_to_show['number_of_departures'] = data_to_show['minimal_n_departures_go'].astype('int')
        data_to_show.drop(['minimal_n_departures_go', 'minimal_n_departures_back'], inplace=True, axis=1)
        
        data_to_show.rename(columns={'statuback':'status'}, inplace=True)

    else:
        data_to_show = elf.all_eligible_schedule(origin_kode, dayofweek, table_to_show.lower())
        dict_col_name = {col:f'{col[:-2]}' for col in data_to_show.columns if col[-1] == 'x' }
        data_to_show.rename(columns=dict_col_name, inplace=True)

        data_to_show.rename(columns={'minimal_n_departures':'number_of_departures'}, inplace=True)
        data_to_show['number_of_departures'] = data_to_show['number_of_departures'].astype('int')

    st.dataframe(data_to_show)
    
    
