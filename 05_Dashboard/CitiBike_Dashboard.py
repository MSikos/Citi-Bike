################################################ CITI BIKE DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt

########################### Initial settings for the dashboard ##################################################################


st.set_page_config(page_title = 'Citi Bike Strategy Dashboard', layout='wide')
st.title("Citi Bike Strategy Dashboard")
st.markdown("The dashboard will help with the expansion problems Citi Bikes currently faces")
st.markdown("Right now, Citi Bikes run into a situation where customers complain about bikes not being avaibale at certain times. This analysis aims to look at the potential reasons behind this.")

########################## Import data ###########################################################################################

df_dual = pd.read_csv('final_data.csv', index_col = 0)
top500 = pd.read_csv('df_top_500_routes.csv', index_col = 0)
daily_rides = pd.read_csv('daily_rides_per_day.csv')

# ######################################### DEFINE THE CHARTS #####################################################################

## Bar chart

fig = go.Figure(go.Bar(x = top500['start_station_name'], y = top500['value'], marker={'color': top500['value'],'colorscale': 'Blues'}))
fig.update_layout(
    title = 'Top 500 most popular bike stations in New York City',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width=True)


## Line chart 

fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

fig_2.add_trace(
go.Scatter(x = daily_rides['date'], y = daily_rides['total_rides'], name = 'Daily bike rides', marker={'color': daily_rides['total_rides'],'color': 'blue'}),
secondary_y = False
)

fig_2.add_trace(
go.Scatter(x=daily_rides['date'], y = daily_rides['avg_daily_temp'], name = 'Daily temperature', marker={'color': daily_rides['avg_daily_temp'],'color': 'red'}),
secondary_y=True
)

fig_2.update_layout(
    title = 'Daily bike trips and temperatures in 2022',
    height = 600
)

st.plotly_chart(fig_2, use_container_width=True)


### Add the map ###

path_to_html = "NYC Bike Trips Top 500 Routes.html" 

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Aggregated Bike Trips in New York City")
st.components.v1.html(html_data,height=1000)
