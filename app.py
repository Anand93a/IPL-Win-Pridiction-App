import pickle

import streamlit as st

import pandas as pd
import numpy as np

st.title('IPL Win Prediction')

teams=['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Lucknow Super Giants',
 'Gujarat Titans',
 'Delhi Capitals',
 'Kings XI Punjab',
 'Chennai Super Kings',
 'Rajasthan Royals']
cities=['Bangalore', 'Chandigarh', 'Delhi', 'Mumbai', 'Kolkata', 'Jaipur',
       'Hyderabad', 'Chennai', 'Cape Town', 'Port Elizabeth', 'Durban',
       'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Bengaluru', 'Indore', 'Dubai', 'Sharjah', 'Navi Mumbai',
       'Lucknow', 'Guwahati']

pipe=pickle.load(open('pipe.pkl','rb'))
col1,col2=st.columns(2)

with col1:

    batting_team=st.selectbox('Select the batting team',sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams))

selected_city=st.selectbox('Select host city',sorted(cities))

target= st.number_input('Target')

col3,col4,col5=st.columns(3)

with col3:
    score=st.number_input('Score')
with col4:
    overs=st.number_input('Overs completed')
with col5:
    wickets=st.number_input('Wickets out')

if st.button('Predict Probability'):
    runs_left=target-score
    balls_left=120-(overs*6)
    wickets=10-wickets
    crr=score/overs
    rrr=(runs_left*6)/balls_left
    input_df=pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],
                  'runs_left':[runs_left],'balls_left':[balls_left],'wickets':[wickets],
                  'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})

    input_df = input_df.astype({
        'runs_left': 'int',
        'balls_left': 'int',
        'wickets': 'int',
        'total_runs_x': 'int',
        'crr': 'float',
        'rrr': 'float'
    })

    st.table(input_df)
    result=pipe.predict_proba(input_df)


    loss =  result[0][0]
    win =  result[0][1]

    st.header(batting_team + "- " + str(round(win.item() * 100)) + "%")
    st.header(bowling_team + "- " + str(round(loss.item() * 100)) + "%")


