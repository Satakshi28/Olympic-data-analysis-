import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg",
    width=200,)
user_menu = st.sidebar.radio('select an option',('Medal Tally', 'Overall Analysis','Country-wise Analysis','Athlete wise Analysis'))
st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")

    st.table(medal_tally)
if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df,'region')
    nations_over_time.rename(columns=lambda x: x.strip(), inplace=True)
    nations_over_time = nations_over_time.sort_values("Edition")
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    events_over_time.rename(columns=lambda x: x.strip(), inplace=True)
    events_over_time = events_over_time.sort_values("Edition")
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    athlete_over_time.rename(columns=lambda x: x.strip(), inplace=True)
    athlete_over_time = athlete_over_time.sort_values("Edition")
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No of events over time(Every sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)
    from helper import most_successful
    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df,selected_sport)

    st.table(x)

if user_menu == 'Country-wise Analysis':
        st.sidebar.title("Country wise analysis")
        country_list = df['region'].dropna().unique().tolist()
        country_list.sort()

        selected_country = st.sidebar.selectbox('Select a Country', country_list)

        country_df = helper.yearwise_medal_tally(df, selected_country)

        if country_df.empty:
            st.warning(f"No data found for {selected_country}.")
        else:
            fig = px.line(country_df, x="Year", y="Medal", title=f"{selected_country} Medal Tally Over the Years")
            st.plotly_chart(fig)

            st.title(selected_country + " excels in the following sports")
            pt = helper.country_event_heatmap(df, selected_country)
            fig,ax = plt.subplots(figsize=(20,20))
            ax = sns.heatmap(pt,annot=True)
            st.pyplot(fig)

            import helper

            st.title("Top 10 athletes of " + selected_country)
            top10_df = helper.most_successful_countrywise(df, selected_country)
            st.table(top10_df)

if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna().to_list()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna().to_list()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna().to_list()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna().to_list()

    st.write("Plotting Age Distributions...")
    fig = ff.create_distplot(
        [x1, x2, x3, x4],
        ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
        show_hist=False,
        show_rug=False
    )
    fig.update_layout(autosize=False, width=1000,height=600)
    st.title("Age Distributions")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = [
        'Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
        'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
        'Art competitions', 'Handball', 'Weightlifting', 'Wrestling',
        'Water Polo', 'Hockey', 'Rowing', 'Fencing',
        'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
        'Tennis', 'Golf', 'Softball', 'Archery',
        'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
        'Rhythmic Gymnastics', 'Trampolining', 'Beach Volleyball', 'Triathlon', 'Ice Hockey'
    ]
    x = []  # list of lists of ages
    name = []  # list of sport names

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        gold_ages = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()

        if not gold_ages.empty:
            x.append(gold_ages.tolist())
            name.append(sport)

    if x and name:
        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=1000, height=600)
        st.title("Age Distributions with respect to Sport(Gold Medalist)")
        st.plotly_chart(fig)
    else:
        st.warning("No data available to plot the age distributions.")

    sport_list = df['Sport'].dropna().unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    # Get user selection
    selected_sport = st.selectbox('Select a Sport', sport_list)

    # Filter DataFrame
    if selected_sport == 'Overall':
        temp_df = df.copy()
    else:
        temp_df = df[df['Sport'] == selected_sport]

    # Drop missing height/weight if needed
    temp_df = temp_df.dropna(subset=['Weight', 'Height', 'Sex', 'Medal'])

    # Plot
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=temp_df,
        x='Weight',
        y='Height',
        hue='Medal',
        style='Sex',
        s=60,
        ax=ax
    )
    ax.set_title(f'Weight vs Height - {selected_sport}')
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)