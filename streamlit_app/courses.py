
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image

st.title("Upload excel file and view courses and credits earned")

st.write("")
st.write("")
img = Image.open('screenshot.png')
st.image(img, caption='Where to download the file')
st.write("")
file = st.file_uploader("Upload an excel file download from sejong portal", type='xlsx')


# read the file
if file is not None:
    df = pd.read_excel('course.xlsx')

# drop and rename the columns
df = df[['Unnamed: 4', 'Unnamed: 5', 'Unnamed: 8']].drop([0,1,2]).reset_index(drop=True)
df.columns = ['Course Name', 'Type', 'Credits']

# define course types
types = {'Major: Elective': 'M.Elective', 'Major: Required': 'M.Required', '1': 'L.A.', '3': 'M.Cores', '9': 'D.M.Required'}
all_types = ['D.M.Required', 'D.M.Elective', 'M.Required', 'M.Elective', 'L.A.', 'M.Cores']
required_credits = {'D.M.Required': 15, 'D.M.Elective': 24, 'M.Required': 15, 'M.Elective': 24, 'L.A.': 36, 'M.Cores': 15}

# change the course types
df.Type = df.Type.apply(lambda x: types[x] if x in types else x)
df.Credits = df.Credits.astype(int) # change the dtype

# groupby types
credits_earned = df.groupby('Type')[['Credits']].sum()
credits_earned['Course'] = df.groupby('Type')['Course Name'].unique().apply(lambda x: '<br>'.join(x))
credits_earned = credits_earned.reindex(all_types, fill_value=0.1).reset_index()

# add required credits
credits_earned['Required Credits'] = credits_earned.Type.apply(lambda x: required_credits[x] if x in required_credits else 0)

# calculate the remaining credits
credits_earned['Remaining'] = credits_earned['Required Credits'] - credits_earned['Credits']

fig, ax = plt.subplots(figsize=(10, 5))
plot_df = credits_earned.melt(
    id_vars=['Type', 'Course'],
    value_vars=['Credits', 'Required Credits'],
    var_name = 'Metric',
    value_name='Value'
)

fig = px.bar(
    plot_df,
    x='Value',
    y='Type',
    color='Metric',
    orientation='h',
    barmode='group',
    text='Value',
    hover_data={'Value': False, 'Metric': False, 'Course': True},
    color_discrete_sequence=['#1db954', '#7DE5B4']
)

fig.update_layout(
    xaxis_title = 'Credits',
    yaxis_title = 'Course Type',
    xaxis=dict(dtick=15, rangemode='tozero'),
    template='plotly_white',
    legend_title=""
)

# Set x-ticks at multiples of 3
fig.update_traces(texttemplate="%{text:.0f}", textposition="outside", cliponaxis=False)


# plt.show()
st.plotly_chart(fig,use_container_width=True)
