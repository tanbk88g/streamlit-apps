import streamlit as st
import pandas as pd
import numpy as np
import pickle


df = pd.read_csv('museum_list_cat.csv')
museum = df.drop(['Type', 'Summary'], axis=1)
museum.set_index('Name', inplace=True)
museum_sim = pickle.load(open('museum_sim.pkl', 'rb'))

st.title('Paris Museum Recommender')

choice = st.selectbox(label='Choose a museum from the drop-down list', options=museum.index)
st.write('You choose:', choice)

museum_series = museum_sim[choice].drop(choice).sort_values(ascending=False).head(10)
st.write('Here are the recommendations')
st.dataframe(museum_series)
