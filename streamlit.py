import streamlit as st
import datetime
from main import run_sentiment_analysis

# Set page layout to wide
st.set_page_config(layout="wide")

# Custom CSS to increase the size of input fields and add spacing
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
            self.league_name = st.text_input('League Name', '', help='Provide League Name')

            # Team 1 and Team 2 inputs
            col1_1, col1_2, col1_3 = st.columns([1, 0.2, 1])
            with col1_1:
                self.team1 = st.text_input('Team 1', '', help='Enter your team name')
            with col1_2:
                st.write('vs')
            with col1_3:
                self.team2 = st.text_input('Team 2', '', help='Enter the opponent team name')
            
            # Date and Time inputs
            col2_1, col2_2 = st.columns([1, 1])
            with col2_1:
                self.match_date = st.date_input('Date of the match', help='Pick the date of the match.')
            with col2_2:
                self.match_time = st.time_input('Time of the match', help='Pick the time of the match.')

            self.match_details = f'{self.team1} vs {self.team2}'

            # Combine the date and time into a datetime object
            match_date_time_obj = datetime.datetime.combine(self.match_date, self.match_time)

            # Convert the datetime object to the desired string format
            self.match_date_time = match_date_time_obj.strftime("%Y-%m-%d %H:%M:%S")

            return st.button('Get Details')

    st.subheader('Sentiments Online')

    def display_results(self, bow_results, tb_results, bert_results,match_result,scoreline):
        

        # Create columns for displaying the results side by side with larger proportions
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1,1,1])

        with col1:
            st.subheader('Bag of Words Model')
            st.dataframe(bow_results)

        with col2:
            st.subheader('TextBlob Model')
            st.dataframe(tb_results)

        with col3:
            st.subheader('BERT Model')
            st.dataframe(bert_results)
        with col4:
            st.subheader('Match Result')
            st.write(match_result)
        with col5:
            st.subheader('Match Scoreline')
            st.write(scoreline)

    def run(self):
        if self.get_user_input():
            bow_results, tb_results, bert_results,match_result,scoreline = run_sentiment_analysis(
                self.league_name, self.match_details, self.match_date_time, skip_scraping=False
            )
            self.display_results(bow_results, tb_results, bert_results,match_result,scoreline)
            # '''
            # '''

# Create an instance of the app and run it
app = SentimentAnalysisApp()
app.run()