import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('../data/museum_list_cat.csv')
museum = df.drop(['Type', 'Summary'], axis=1)
museum.set_index('Name', inplace=True)

museum_sim = pd.DataFrame(cosine_similarity(museum), columns=museum.index, index=museum.index)

st.title('Paris Museum Recommender')

choice = st.selectbox(label='Choose a museum from the drop-down list', options=museum.index)
st.write('You choose:', choice)

museum_series = museum_sim[choice].drop(choice).sort_values(ascending=False).head(10)
st.write('Here are the recommendations')
st.dataframe(museum_series)
