import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

import os 
import re

data = pd.read_csv('data_with_metrics.csv')
data_views = pd.read_csv('data_views.csv')

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

# fig = px.bar(hourly_sum, x='hour_of_day', y='Sum', color='username', barmode='group')
fig = px.histogram(filtered_data, x='tweet_VADER_sentiment', nbins=10)

st.plotly_chart(fig)


group_name2 = data['username'].unique()
selected_name = st.multiselect('Select a group', group_name2)
filtered_data = data[data['username'].isin(selected_name)]
filtered_data_views = data_views[data_views['username'].isin(selected_name)]

# Impressions by Time
st.header("Total Impressions")
st.text("Measures the number of views the tweets were seen on Twitter.")
# Grouping the data by category and calculating the total views
views_by_category = filtered_data_views.groupby('username')['views'].sum().reset_index()

# Creating the bar chart
fig = px.bar(views_by_category, x='username', y='views', color='username')

# Show the chart
st.plotly_chart(fig)

# Creating the boxplot
fig = px.box(filtered_data_views, x='username', y='views', color='username', points=False)

# Show the chart
st.plotly_chart(fig)


# Tweet Counts by Time 
st.header("Tweet Counts by Time")
st.text("The number of tweets that were published.")
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
st.header("Total Average Engagement Rate by Time")
st.subheader("Measures the number of engagements a tweet gets, to the total number of followers, in each hour") 
st.text("Formula: Average Engagement Rate = (likes + shares) / (total followers)")
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
st.subheader("Measures the total number of engagements a tweet gets, to the total number of followers, in each hour") 
st.text("Formula: Amplification Rate = (shares) / (total followers)")
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

def load_all_historical_data_csv():
    dataframes = []
    pattern = r"Historical30d_(\w+)\.csv"
    for filename in os.listdir("data"):
        match = re.search(pattern, filename)
        if match:
            profile = match.group(1)
            filepath = os.path.join("data", filename)
            df = pd.read_csv(filepath)
            df['username'] = profile  # Add a 'Profile' column to identify the data source
            dataframes.append(df)


    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df = combined_df[['username'] + list(combined_df.columns[:-1])]

    # somehow, extra spacing there
    combined_df['date'] = pd.to_datetime(combined_df['date'])
    combined_df['followers'] = combined_df[' followers']
    combined_df['following'] = combined_df[' following']
    combined_df['tweets'] = combined_df[' tweets']

    # net change
    combined_df['net_change_followers'] = combined_df.groupby('username')['followers'].diff()
    # growth rate
    combined_df['growth_rate_followers'] = combined_df.groupby('username')['followers'].pct_change() * 100  # Calculate the net change
    
    combined_df.drop([' followers', ' following', ' tweets'], axis=1, inplace=True)

    return combined_df

historical_data = load_all_historical_data_csv()

filtered_data3 = historical_data[historical_data['username'].isin(selected_name)]


# Audience Growth Rate
st.header("Audience Growth Rate")
st.text("Audience Growth Rate = ((Ending Followers - Starting Followers) / Starting Followers) * 100")

# Followers count over time
st.subheader("Followers count over time")

fig = px.line(filtered_data3, x='date', y='followers', color='username')

st.plotly_chart(fig)

# Net change of followers over time --------------------
st.subheader("Followers net changes over time")

fig = px.line(filtered_data3, x='date', y='net_change_followers', color='username')

st.plotly_chart(fig)
# ------------------------------------------------------

# Daily Growth Rate ------------------------------------
st.subheader("Daily growth rate")

fig = px.line(filtered_data3, x='date', y='growth_rate_followers', color='username')

st.plotly_chart(fig)

# Audience Growth Rate in a month
st.subheader("Audience Growth Rate in the time period")

def get_total_growth_rate_follower(df_combined):
    usernames = df_combined['username'].unique()
    df = pd.DataFrame(usernames, columns=['username'])
    total_growth_rates = {}
    for username in usernames:
        user_df = df_combined[df_combined['username'] == username]
        followers_start = user_df.iloc[0]['followers']
        followers_end = user_df.iloc[-1]['followers']
        total_growth_rate = ((followers_end - followers_start) / followers_start) * 100
        total_growth_rates[username] = total_growth_rate
    return total_growth_rates

list_total_growth_rate = get_total_growth_rate_follower(historical_data)

start_date = historical_data.iloc[0]['date']
end_date = historical_data.iloc[-1]['date']

st.subheader(f"From {start_date.strftime('%Y-%m-%d')} until {end_date.strftime('%Y-%m-%d')}")

for username, growth_rate in list_total_growth_rate.items():
    st.text(f"{username}: {growth_rate:.2f}%")