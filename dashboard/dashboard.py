import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set_theme(style='dark')

all_df = pd.read_csv('dashboard/main_data.csv')

min_date = datetime.datetime.strptime(all_df['dteday'].min(), '%Y-%m-%d').date()
max_date = datetime.datetime.strptime(all_df['dteday'].max(), '%Y-%m-%d').date()

all_df['dteday'] = pd.to_datetime(all_df['dteday'])

with st.sidebar:
    st.image('https://avatars.githubusercontent.com/u/29939062?v=4')
    url = 'https://joydozer.github.io/'
    st.subheader('[Jonathan W.](%s)' % url)
    st.subheader('ID Dicoding: weiss001')
    start_date, end_date = st.date_input(
        label='Time span', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
#Filterisasi DataFrame
tot_date = end_date - start_date
filtered_df = all_df.loc[(all_df['dteday'].dt.date >= start_date)
                     & (all_df['dteday'].dt.date <= end_date)]

st.header(':bike: Bike Sharing Final Project :bike:')
st.markdown('#')
st.subheader('Bike Sharing Daily Orders :medal:')
col1, col2, col3 = st.columns(3)

with col1:
    total_orders = filtered_df['cnt_hour'].sum()
    st.metric("Total orders in the last " + str(tot_date.days) + " days:", value=total_orders)

with col2:
    peak_order = filtered_df['cnt_day'].max()
    st.metric("Highest order per day:", value=peak_order)

with col3:
    lowest_order = filtered_df['cnt_day'].min()
    st.metric("Lowest order per day:", value=lowest_order)

sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(16,8))
ax = sns.lineplot(data=all_df, x='dteday', y='cnt_day', marker="o")
ax.set_xlim(start_date, end_date)
plt.xlabel('Date')
plt.ylabel('Total order per day')
st.pyplot(fig)

st.markdown('#')
st.subheader('Bike Sharing Orders with Temperature (°C) :thermometer: ')

real_temp = []
for x in filtered_df['temp_hour']:
    real_temp.append(round(x * 41))

fig, axs = plt.subplots(ncols=2)
fig.set_figwidth(14)
fig.set_figheight(6)
sns.lineplot(data=filtered_df, x=real_temp, y='cnt_hour', marker="o", ax=axs[0])
sns.scatterplot(data=filtered_df, x='dteday', y='cnt_day', hue=real_temp, ax=axs[1])
axs[0].set_xlabel('Temperature (°C)')
axs[1].set_xlabel('Date')
axs[0].set_ylabel('Total Bike Sharing')
axs[1].set_ylabel('Total Bike Sharing')
axs[1].legend(title='Temperature (°C)')
st.pyplot(fig)

st.markdown('#')
st.subheader('Bike Sharing based on the season :bar_chart: ')

data_season = filtered_df.groupby('season_desc_hour')['cnt_hour'].mean()
nama_musim = []
for x in filtered_df['season_desc_hour']:
    if x in nama_musim:
        continue
    else:
        nama_musim.append(x)
fig = plt.figure(figsize=(16,8))
sns.barplot(x=nama_musim, y=data_season)
for i in range(len(nama_musim)):
    plt.text(i, data_season.iloc[i]//2, round(data_season.iloc[i]), ha = 'center')
plt.xlabel('Season')
plt.ylabel('Total Mean Bike Sharing per Hour')
st.pyplot(fig)