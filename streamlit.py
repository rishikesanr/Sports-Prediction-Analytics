import streamlit as st
import datetime
from main import run_sentiment_analysis
import pandas as pd
import plotly.express as px

# Set page layout to wide to use whole screen
st.set_page_config(layout="wide")

# CSS to increase the size of input fields and add spacing
st.markdown(
    """
    <style>
    .css-1d391kg, .css-1d3k3y7, .css-1d3k3y7, .stTextInput, .stDateInput, .stTimeInput, .stSelectbox {  
        font-size: 16px;
        height: 3em;
        margin-bottom: 1.5em;  /* Add space between fields */
    }
    .stButton button {  
        width: 100%;
        height: 3em;
        font-size: 16px;
        margin-top: 1.5em;  /* Add space above the button */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

class SentimentAnalysisApp:
    def __init__(self):
        self.league_name = None
        self.team1 = None
        self.team2 = None
        self.match_date = None
        self.match_time = None
        self.match_details = None
        self.match_date_time = None

    def get_user_input(self):
        with st.sidebar:
            st.title('Input Details')
            
            # Input fields
            self.league_name = st.text_input('League Name', '', help='Provide Subreddit name of the League (e.g. PremierLeague)')

            # Team 1 and Team 2 inputs
            col1_1, col1_2, col1_3 = st.columns([1, 0.2, 1])
            with col1_1:
                self.team1 = st.text_input('Team 1', '', help='Enter the home side/host name')
            with col1_2:
                st.write('vs')
            with col1_3:
                self.team2 = st.text_input('Team 2', '', help='Enter the opponent/away team name')
            
            # Date and Time inputs
            col2_1, col2_2 = st.columns([1, 1])
            with col2_1:
                self.match_date = st.date_input('Date of the match', help='Pick the date of the match.')
            with col2_2:
                self.match_time = st.time_input('Time of the match', help='Pick the UTC time of the match.')

            self.match_details = f'{self.team1} vs {self.team2}'

            # Combine the date and time into a datetime object
            match_date_time_obj = datetime.datetime.combine(self.match_date, self.match_time)

            # Convert the datetime object to the desired string format
            self.match_date_time = match_date_time_obj.strftime("%Y-%m-%d %H:%M:%S")

            return st.button('Get Details')

    def aggregate_results(self, bow_results, tb_results, bert_results):
        # combined_results = pd.concat([bow_results, tb_results, bert_results], axis=0)
        combined_results = bert_results.reset_index()

        # Calculate win/lose odds
        team1_positive = combined_results['%positive'].iloc[0]
        team2_positive = combined_results['%positive'].iloc[1]
        total_positive = team1_positive + team2_positive


        combined_results['win_odds'] = [round((team1_positive / total_positive)*100,1), round((team2_positive/ total_positive)*100,1)]
        # combined_results['lose_odds'] = [team1_negative / team2_negative, team2_negative / team1_negative]

        combined_results['percent_positive'] = combined_results['positive'] * 100 / combined_results['total']
        combined_results['percent_negative'] = combined_results['negative'] * 100 / combined_results['total']
        combined_results['percent_neutral'] = combined_results['neutral'] * 100 / combined_results['total']

        return combined_results
    
    def plot_odds(self, combined_results):
        fig = px.bar(combined_results, x='team', y=['win_odds'],
                     #title='Odds of Winning and Losing for each Team',
                     labels={'value': '% Probability Winning', 'variable': 'Sentiment', 'team': 'Team'},
                     color_discrete_map={'win_odds': '#1f77b4'})
        fig.update_layout(
            barmode='group',
            plot_bgcolor='white',
            margin=dict(l=40, r=40, t=40, b=40),  # Adjust margins for better spacing
            xaxis=dict(
                showline=True,
                linewidth=2,
                linecolor='black'
            ),
            yaxis=dict(
                showline=True,
                linewidth=2,
                linecolor='black'
            )
        )
        fig.for_each_trace(lambda t: t.update(name={'win_odds': 'Probability of Winning'}[t.name]))
        return fig

    def plot_win_percent(self, combined_results):
        fig = px.bar(combined_results, x='team', y='percent_positive',
                     #title=f'{round(combined_results["positive_percent"].loc[0],1)}% of {combined_results["team"].loc[0]} have a positive sentiment for the game while {round(combined_results["positive_percent"].loc[1],1)}% of {combined_results["team"].loc[1]} have a positive sentiment about their team',
                     labels={'percent_positive': '% Positive', 'team': 'Team'},
                     color_discrete_sequence=['#1f77b4'])  # Matplotlib blue
        fig.update_layout(
            plot_bgcolor='white',
            margin=dict(l=40, r=40, t=40, b=40),  # Adjust margins for better spacing
            xaxis=dict(
                showline=True,
                linewidth=2,
                linecolor='black'
            ),
            yaxis=dict(
                showline=True,
                linewidth=2,
                linecolor='black'
            )
        )
        fig.update_traces(name='Positive Sentiment')
        return fig

    def plot_lose_percent(self, combined_results):
        fig = px.bar(combined_results, x='team', y=['percent_negative'],
                     #title='Lose Percent by Team',
                     labels={'percent_negative': '% Negative', 'team': 'Team'},
                     color_discrete_sequence=['orange'])
        fig.update_layout(
            plot_bgcolor='white',
            margin=dict(l=40, r=40, t=40, b=40),  # Adjust margins for better spacing
            xaxis=dict(
                showline=True,
                linewidth=2,
                linecolor='black'
            ),
            yaxis=dict(
                showline=True,
                linewidth=2,
                linecolor='black'
            )
        )
        fig.update_traces(name='Negative Sentiment')
        return fig

    def display_results(self, bow_results, tb_results, bert_results):
        combined_results = self.aggregate_results(bow_results, tb_results, bert_results)

        # First row: Odds of Winning and Losing
        st.title('Fan Sentiments Online')
        
        st.subheader('Odds of Winning the Match')
        odds_fig = self.plot_odds(combined_results)
        st.plotly_chart(odds_fig, use_container_width=True)

        # Second row: Win Percent and Lose Percent side by side
        col1, col2 = st.columns(2)

        with col1:
            st.subheader('Positive Sentiment')
            win_fig = self.plot_win_percent(combined_results)
            st.plotly_chart(win_fig, use_container_width=True)
            st.write(f'{round(combined_results["percent_positive"].iloc[0],1)}% of {combined_results["team"].iloc[0]} fans have a positive sentiment for the game while {round(combined_results["percent_positive"].iloc[1],1)}% of {combined_results["team"].iloc[1]} have a positive sentiment about their team')
        
        with col2:
            st.subheader('Negative Sentiment')
            lose_fig = self.plot_lose_percent(combined_results)
            st.plotly_chart(lose_fig, use_container_width=True)
            st.write(f'{round(combined_results["percent_negative"].iloc[0],1)}% of {combined_results["team"].iloc[0]} fans have a negative sentiment for the game while {round(combined_results["percent_negative"].iloc[1],1)}% of {combined_results["team"].iloc[1]} have a negetive sentiment about their team')
        


    def run(self):
        if self.get_user_input():
            with st.spinner('Fetching details...'):
                bow_results, tb_results, bert_results, match_result, scoreline = run_sentiment_analysis(
                    self.league_name, self.match_details, self.match_date_time, skip_scraping=False
                )
                self.display_results(bow_results, tb_results, bert_results)

# Create an instance of the app and run it
st.title('Name TBA - Improve your sports betting fortunes by analyzing fan sentiments online.')
st.subheader('Enter the match details below to get started.')
app = SentimentAnalysisApp()
app.run()
