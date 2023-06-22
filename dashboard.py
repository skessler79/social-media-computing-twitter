import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

data = pd.read_csv('data_with_metrics.csv')

st.title("Satire News Website Social Media Monitor")

group_name1 = data['username'].unique()
selected_group = st.selectbox('Select a group', group_name1)
filtered_data = data[data['username'] == selected_group]

# Violin plot for favorite counts
st.header("Violin Plot for Favorite Counts")

fig = px.violin(filtered_data, x='username', y='favorite_count', box=True, color='username')

fig.update_layout(
    xaxis_title='Group',
    yaxis_title='Value',
    margin=dict(t=50) 
)

st.plotly_chart(fig)

# Tweet Sentiment Score histogram 
st.header("Tweet Sentiment Score histogram")
# hourly_sum = filtered_data.groupby(['hour_of_day', 'username'])['tweet_VADER_sentiment'].sum().reset_index(name='Sum')

# fig = px.bar(hourly_sum, x='hour_of_day', y='Sum', color='username', barmode='group')
fig = px.histogram(filtered_data, x='tweet_VADER_sentiment', nbins=10)
# fig.update_layout(
#     xaxis_title='Hour',
#     yaxis_title='Sum',
#     height=600,  
#     width=800,
#     margin=dict(t=50)  
# )

st.plotly_chart(fig)


group_name2 = data['username'].unique()
selected_name = st.multiselect('Select a group', group_name2)
filtered_data = data[data['username'].isin(selected_name)]

# Tweet Counts by Time 
st.header("Tweet Counts by Time")

hourly_counts = filtered_data.groupby(['hour_of_day', 'username']).size().reset_index(name='Count')

fig = px.bar(hourly_counts, x='hour_of_day', y='Count', color='username', barmode='group')
fig.update_layout(
    xaxis_title='Hour',
    yaxis_title='Count',
    height=600,  
    width=800,
    margin=dict(t=50)  
)

st.plotly_chart(fig)


# Total Average Engagement by Time
st.header("Total Average Engagement by Time")
hourly_sum = filtered_data.groupby(['hour_of_day', 'username'])['avg_engagement_rate'].sum().reset_index(name='Sum')

fig = px.bar(hourly_sum, x='hour_of_day', y='Sum', color='username', barmode='group')
fig.update_layout(
    xaxis_title='Hour',
    yaxis_title='Sum',
    height=600,  
    width=800,
    margin=dict(t=50)  
)

st.plotly_chart(fig)

# Total Amplification Rate by Time
st.header("Total Amplification Rate by Time")
hourly_sum = filtered_data.groupby(['hour_of_day', 'username'])['amplification_rate'].sum().reset_index(name='Sum')

fig = px.bar(hourly_sum, x='hour_of_day', y='Sum', color='username', barmode='group')
fig.update_layout(
    xaxis_title='Hour',
    yaxis_title='Sum',
    height=600,  
    width=800,
    margin=dict(t=50)  
)

st.plotly_chart(fig)
