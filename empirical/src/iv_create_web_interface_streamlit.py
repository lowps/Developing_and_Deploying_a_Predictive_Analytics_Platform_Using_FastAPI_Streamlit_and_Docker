import os
import sys
import pandas as pd
import numpy as np
import streamlit as st
import requests
import json



sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.logger import Logger
from utils.helpers import get_directory_name

absolute_path = 'Developing_and_Deploying_a_Predictive_Analytics_Platform_Using_FastAPI_Streamlit_and_Docker/empirical/src/iv_create_web_interface_streamlit.py'
inspector_gadget = get_directory_name(absolute_path)
inspector_gadget = Logger(inspector_gadget)

#-------Minor preprocessing start-------

fpath = os.path.join(os.path.abspath('..'), 'data', 'processed', 'cleaned_car_data.csv')
df = pd.read_csv(fpath)
df_copy = df.copy()

col = ['Unnamed: 0']
df_copy.drop(columns=col, inplace=True)
df_copy.reset_index(drop=True, inplace=True)

values_to_drop = [0]
df_filtered = df_copy[~df_copy['price'].isin(values_to_drop)]
values_to_drop2 = [0]
df_filtered = df_filtered[~df_filtered['miles_driven'].isin(values_to_drop2)]
values_to_drop3 = ['Mahindra', 'Maruti', 'Skoda', 'Renault', 'Datsun', 'Tata', 'Hindustan', 'Force', 'Land', 'Volvo']
df_filtered = df_filtered[~df_filtered['automaker'].isin(values_to_drop3)]

df_filtered.reset_index(inplace=True)
df_filtered.drop(columns='index', inplace=True)

#-------Minor preprocessing end-------


#-------streamlit logic start---------

def run():
    '''
    Creates web interface via Streamlit for client interaction

    Parameters:
    :name: A list of options, pulling from  pd.DataFrame, for the client to choose from 'name' drop down box.
    :automaker: A list of options, pulling from  pd.DataFrame, for the client to choose from 'automaker' drop down box.
    :year: A selectbox labelled "Year". Client inserts a specified "Year"
    :miles_driven: A selectbox labelled "Miles driven". Client inserts a specified "Miles driven"
    :fuel_type: A list of options, pulling from pd.DataFrame, for the client to choose from 'Fuel type' drop down box.

    :data:(dict): store the client data we receive through the web interface in the “data” variable.
    
    '''
    st.title("Car Prediction")

    name = st.selectbox("Cars Model",
                        df_filtered.name.unique())
    
    automaker = st.selectbox("Automaker Name",
                             df_filtered.automaker.unique())
    
    year = st.number_input("Year")

    miles_driven = st.number_input("Miles driven")

    fuel_type = st.selectbox("Fuel type",
                             df_filtered.fuel_type.unique())
    
    #store the data we receive 
    data = {
        'name': name,
        'automaker': automaker,
        'year': year,
        'miles_driven': miles_driven,
        'fuel_type': fuel_type
        }
    
    if st.button("Predict"): #GUI button 'Precit'
        response = requests.post("http://127.0.0.1:8000/predict", json=data)

        prediction = response.text

        st.success(f"The result of the linear regression prediction is: {prediction}")


#-------streamlit logic end-----------

def main():
    run()


if __name__ == '__main__':
    main()





