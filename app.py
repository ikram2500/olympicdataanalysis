import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")

df = preprocessor.preprocess(df, region_df)

st.sidebar.title('Olympics Analysis')
st.sidebar.image('olympic.png')

user_menu = st.sidebar.radio(
    "Select an Option",
    ("Medal Tally", "Overall Analysis", "Country-Wise Analysis", "Athlete wise Analysis")
)

if user_menu == "Medal Tally":
    # st.sidebar.header('Medal Tally')
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox('Select year ', years)
    selected_country = st.sidebar.selectbox('Select country ', country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    # st.title(' Medal Tally ')
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Country wise over all Performance ')

    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Overall Performance')

    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Performance in ' + str(selected_year) + ' Olympics')
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('nations')
        st.title(nations)
    with col2:
        st.header('athletes')
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Editions", y="region")
    st.title('Participatting Nations over the years')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x="Editions", y='Event')
    st.title('Events over the years')
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Editions", y='Name')
    st.title('Athletes over the years')
    st.plotly_chart(fig)

    st.title("No of Events over time(Every sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int),annot=True)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a sport', sport_list)


if user_menu == 'Country-Wise Analysis':

    st.sidebar.title('Country-Wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df =helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + ' Medal tally over the  years')
    st.plotly_chart(fig)

    st.title(selected_country + ' excels in the following sports')
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    # selected_country = st.sidebar.selectbox('Select a Country', country_list)
    top10_df = helper.most_successful_countrywise((df, selected_country))
    st.table(top10_df)


if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
    show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    name = []
    x = []
    famous_sports = ['Basketball','Football','Tug-Of-War','Athletics','Swimming','Badminton','Sailing','Judo','Gymnastics','Art Competitions','Handball',
                      'Weightlifting','Wrestling','Water Polo','Hockey','Rowing','Fencing','Equestrianism','Shooting','Boxing','Taekwondo','Cycling',
                      'Diving','Canoeing','Tennis','Modern Pentathlon','Golf', 'Softball', 'Archery', 'Volleyball', 'Synchronized Swimming','Table Tennis',
                      'Baseball', 'Rhythmic Gymnastics', 'Rugby Sevens', 'Trampolining','Beach Volleyball', 'Triathlon', 'Rugby','Lacrosse', 'Polo', 'Ice Hockey']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt sport(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height VS Weight ')
    selected_sport = st.selectbox('Select a sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(data =temp_df, x = 'Weight', y ='Height', hue = 'Medal',
     style = 'Sex',s=60)
    st.pyplot(fig)

    st.title('Men Vs Women Participation over the years')
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=900, height=600)
    st.plotly_chart(fig)