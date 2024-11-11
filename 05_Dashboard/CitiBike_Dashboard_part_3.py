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
from numerize.numerize import numerize
from PIL import Image

########################### Initial settings for the dashboard ##################################################################

st.set_page_config(page_title = 'New York Citi Bike Strategy Dashboard', layout='wide')
st.title("New York Citi Bike Strategy Dashboard")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","The relationship between bike usage and the weather",
   "The Top 20 most popular start stations",
    "Interactive map showing popular bike trips", "A comparison of bike type usage per average temperature", "Conclusion and recommendations"])

########################## Import data ###########################################################################################

url = 'https://raw.githubusercontent.com/MSikos/Citi-Bike/refs/heads/main/05_Dashboard/reduced_data_to_7_percent.csv'
url2 = 'https://raw.githubusercontent.com/MSikos/Citi-Bike/refs/heads/main/05_Dashboard/df_top_500_routes.csv'
url3 = 'https://raw.githubusercontent.com/MSikos/Citi-Bike/refs/heads/main/05_Dashboard/daily_rides_per_day.csv'
df_small = pd.read_csv(url, index_col = 0)
top500 = pd.read_csv(url2, index_col = 0)
daily_rides = pd.read_csv(url3)


# ######################################### DEFINE THE PAGES #####################################################################

### Intro page

if page == "Intro page":
    st.markdown("#### New York Citi Bike is a bike-sharing company that has seen its popularity increase since its launch in 2013. Due to this increased popularity, Citi Bike is having distribution problems, resulting in bike shortages at popular bike stations which is leading to increased customer complaints. This dashboard will help illustrate and offer resolutions to this problem.")
    st.markdown("Currently, Citi bikes are often not available at popular stations at certain times. This analysis will highlight several details of this shortage so a strategy can be developed to help remediate it. The dashboard is separated into 5 parts:")
    st.markdown("- The relationship between bike usage and the weather")
    st.markdown("- The top 20 most popular start stations")
    st.markdown("- An interactive map showing the most popular bike trips")
    st.markdown("- A comparison of bike type usage per average temperature")
    st.markdown("- Conclusion and recommendations")
    st.markdown("The Aspect Selector dropdown menu on the left will take you to the different pages of the analyses that were focused on.")   

    IntroImage = Image.open("./05_Dashboard/citibike1.jpg") #source: https://unsplash.com/s/photos/citi-bike
    st.image(IntroImage)

    ### Create a dual axis line chart page ###
    
elif page == 'The relationship between bike usage and the weather':

    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
    go.Scatter(x = daily_rides['date'], y = daily_rides['total_rides'], name = 'Daily bike rides', marker={'color': daily_rides['total_rides'],'color': 'blue'}),
    secondary_y = False
)

    fig_2.add_trace(
    go.Scatter(x=daily_rides['date'], y = daily_rides['avg_daily_temp'], name = 'Daily temperature (°C)', marker={'color': daily_rides['avg_daily_temp'],'color': 'red'}),
    secondary_y=True
)

    fig_2.update_layout(
    title = 'Daily bike trips and temperatures in 2022',
    height = 600
)

    st.plotly_chart(fig_2, use_container_width=True)

    st.markdown("When looking at the dual axis line plot, it becomes clear that there is a strong correlation between temperature and daily bike rides. When the temperature rises, the number of daily bike rides increase as well. When the temperature drops and it is cold outside there are less people using a bike as a means of transportation.") 
    st.markdown("This insight shows that the bike shortage problem occurs in the warmer months in spring, summer and fall, from May to October.")

### Most popular bike stations page

    # Create the season variable

elif page == 'The Top 20 most popular start stations':
    
    # Create the filter on the side bar
    
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options = df_small['season'].unique(),
    default = df_small['season'].unique())

    df1 = df_small.query('season == @season_filter')
    
    # Define the total rides
    total_rides = float(df1['bike_rides_daily'].count())    
    st.metric(label = 'Total Bike Rides', value= numerize(total_rides))

    # Bar chart

    df1['value'] = 1 
    df_groupby_bar = df1.groupby('start_station_name', as_index = False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value']))

    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color':top20['value'],'colorscale': 'Blues'}))
    fig.update_layout(
    title = 'Top 20 most popular start stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of bike rides',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("Throughout the whole year there are 4 start stations that are the most popular:") 
    st.markdown("W 21 St & 6 Ave, West St & Chambers St, Broadway & W 58 St, followed closely by 6 Ave & W 33 St.")
    st.markdown("When looking specifically at the months in spring, summer and fall, there is a big difference in popularity between these 4 bike stations and the other 16 in the top 20.")

elif page == 'Interactive map showing popular bike trips': 

    ### Create the map ###

    st.write("Interactive map showing popular bike trips in New York")

    path_to_html = "./05_Dashboard/NYC Bike Trips Top 500 Routes.html"

    # Read file and keep in variable 
    with open(path_to_html, 'r') as f:
        html_data = f.read()

    ## Show in web page 
    st.write("#### Aggregated bike rides in New York")
    st.components.v1.html(html_data,height = 1000)
    st.markdown("This interactive map shows the aggregated bike rides in the city. Visually, it quickly becomes obvious that the most popular bike trips are alongside the waterfront and in Central Park. This explains why the most used start stations from the bar chart on the previous page are popular as they are great starting points of these scenic routes.")
   
elif page == 'A comparison of bike type usage per average temperature': 
    
    ### Create a stacked bar chart ###
    # Filter data to be within the given temperature range
    filtered_df = df_small[(df_small['avgTemp'] >= -11.7) & (df_small['avgTemp'] <= 31.3)]

    # Group by avgTemp and rideable_type and calculate the sum of trips
    grouped_df = filtered_df.groupby(['avgTemp', 'bike_type'], as_index=False).agg({'value': 'sum'})

    # Pivot the data for the stacked bar chart
    pivot_df = grouped_df.pivot(index='avgTemp', columns='bike_type', values='value').fillna(0)

    # Create the stacked bar chart
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=pivot_df.index, y=pivot_df['electric_bike'], name='Electric Bike'))
    fig3.add_trace(go.Bar(x=pivot_df.index, y=pivot_df['classic_bike'], name='Classic Bike'))

    # Update layout for stacked bar chart
    fig3.update_layout(
    barmode='stack',
    title='Sum of bike rides by average temperature and bike type',
    xaxis_title='Average temperature (°C)',
    yaxis_title='Sum of bike rides',
    width=900, height=600
    )

    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('By comparing the utilization of classic bikes and electric bikes, we can determine if both types of bike will need to be stored at stations more frequently in order to avoid a bike shortage.')
    st.markdown('The stacked bar chart shows that classic bikes are rented much more often than electric bikes. When the temperature drops, we notice that electric bikes are used as often as classic bikes, but the total amount of bike rides during this period is very low.')
    st.markdown('In general, electric bikes are used between 35 and 40 percent of the total bike use. As the temperature fluctuates we see the number of bike rides also fluctuating for both bike types, with classic bikes being the most visable as they are used more often than electric bikes.')
                                
else:
    
    st.header("Conclusion and recommendations")
    st.markdown('#### Our analysis has shown that New York Citi Bike should focus on the following objectives moving forward:')
    st.markdown('- There is a strong correlation between temperatures and daily bike rides. I recommend New York Citi bike to increase the supply of bikes during the warmer months, from May to October. In the coldest months bikes are used a lot less frequently. To reduce costs, a lower availability in bikes during these months is advisable.')
    st.markdown('- The most popular start stations are at the waterfront and at Central Park. I recommend increasing the number of bikes at these stations and reviewing these areas for any potential possibility of adding extra bike stations.')
    st.markdown('- In the warmer and more popular months, electric bikes are used between 35 to 40 percent of the total bike use. As these bikes are more expensive to rent, I would recommend exploring opportunities that will increase the use of electric bikes and therefore increase revenue.')
    st.markdown('- At present, we do not have enough information in our current data to make a determination on which bike type is more popular. I would recommend Citi Bike survey its customers on bike preference to determine if there are sufficient quantites of each bike type available at the most popular stations.')

    bikesign = Image.open("./05_Dashboard/citibike2.jpg")  #source: https://unsplash.com/s/photos/citi-bike
    st.image(bikesign)
