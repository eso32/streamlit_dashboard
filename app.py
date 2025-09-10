import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import numpy as np
from ydata_profiling import ProfileReport

REPORT_PATH = Path() / 'welcome_poll.html'

df = pd.read_csv('35__welcome_survey_cleaned.csv', sep=';')

st.title("Welcome Poll Analysis")

st.dataframe(df.head(), hide_index=True);

st.header("Basic metrics")

c0,c1,c2,c3 = st.columns([1,1,1,1])

with c0:
    st.metric("answers", len(df))

with c1:
    no_men = (df['gender'] == 1).sum()
    st.metric("men", no_men)

with c2:
    no_women = (df['gender'] == 0).sum()
    st.metric("women", no_women)

with c3:
    empty = df['gender'].isna().sum()
    st.metric("empty", empty)

age_order = ['<18', '18-24', '25-34', '35-44', '45-54', '55-64', '>=65', 'unknown']

fig_age = px.histogram(
    df,
    x='age',
    color='gender',
    barmode='stack',
    category_orders={'age': age_order},  # wymuszona kolejność
    color_discrete_map={0:'blue', 1:'orange'},
    labels={'age':'Age', 'gender':'Gender'},
    title='Histogram of people by age and gender')
st.plotly_chart(fig_age)

fig_education = px.histogram(
    df,
    x='edu_level',
    title='Histogram of people\'s education'
)

st.plotly_chart(fig_education)

st.header("Advanced section")

if REPORT_PATH.exists():
    with open("welcome_pool.html", "rb") as f:
        st.download_button("Download report", f, file_name="welcome_pool.html")

elif st.button("Generate Ydata-profile"):
    with st.spinner("Generating report, please wait..."):
        ydata_analysis = ProfileReport(df, title="Welcome Poll detailed analysis")
        ydata_analysis.to_file(REPORT_PATH.name)
    st.rerun()