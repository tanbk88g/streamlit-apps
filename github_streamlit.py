import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(layout='wide')

df = pd.read_csv('data/museum_list_cat.csv')
museum = df.drop(['Type', 'Summary'], axis=1)
museum.set_index('Name', inplace=True)

museum_sim = pickle.load(open('data/museum_sim.pkl', 'rb'))
st.title('Paris Museum Recommender')

col1, col2 = st.columns([0.5,0.5], gap='medium')

with col1:
    st.header('More like this')
    box_choice = st.selectbox(label='Choose a museum from the drop-down list:', options=museum.index)
    st.write('You have chosen:', box_choice)

    museum_series = museum_sim[box_choice].drop(box_choice).sort_values(ascending=False).head(10)
    st.write('Here are similar recommendations:')
    c1_choice = st.radio('Select museum button for more info:', museum_series.index)
    st.write('Description for:', c1_choice)
    st.write(df[df['Name']==c1_choice]['Summary'].item())

with col2:
    st.header('You may like')
    col = museum.columns
    my_pref =  pd.Series(data=np.zeros(len(col)), index=col)

    with st.form('my_form'):
        st.write('Choose the types of museums:')
        subcol1, subcol2 = st.columns(2)
        
        my_pref['fine_art'] = subcol1.checkbox('Fine Art')
        my_pref['modern_art'] = subcol1.checkbox('Modern Art')
        my_pref['sculpture'] = subcol1.checkbox('Sculpture')
        my_pref['science'] = subcol1.checkbox('Science/Tech')
        my_pref['history'] = subcol1.checkbox('History')
        my_pref['culture'] = subcol2.checkbox('Culture')
        my_pref['literary'] = subcol2.checkbox('Literary')
        my_pref['fashion_media'] = subcol2.checkbox('Fashion/Music/Photography')
        my_pref['kids_ok'] = subcol2.checkbox('OK for Kids')
        my_pref['special'] = subcol2.checkbox('Special')
        
        submit = st.form_submit_button('Show More')
    
    my_recommend = np.dot(museum.values, my_pref.values)
    my_series = pd.Series(my_recommend, index=museum.index)
    my_choice = my_series.sort_values(ascending=False).head(10).index
    c2_choice = st.radio('Select museum button for more info:', my_choice)
    st.write('Description for:', c2_choice)
    st.write(df[df['Name']==c2_choice]['Summary'].item())
