from datetime import datetime
import pytz
import requests
from bs4 import BeautifulSoup
import re

def match_results(collection_name, match_date_time):
    # Convert match_date_time to a datetime object
    match_datetime = datetime.strptime(match_date_time, '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc)
    match_date = re.findall(r'(\d{4}-\d{2}-\d{2})',match_date_time)[0]
    
    # Get the current time in UTC
    now_utc = datetime.now(pytz.utc)
    
    # Check if the match date is in the past or future
    if match_datetime > now_utc:
        # If the match is in the future, we cannot find the result as there is none
        winner, scorelines = "Match Yet to Start", "Match Yet to Start"
    else:
        # If the match is in the past, find the winner
        winner, scorelines = find_match_winner_and_score(collection_name,match_date)
    
    return winner, scorelines

def find_match_winner_and_score(collection_name,match_date):
    # Split the collection_name to get the team names
    teams = collection_name.split(' vs ')
    team1, team2 = teams[0], teams[1]
    
    # Define the search query
    query = f"{collection_name} {match_date} match result espn"
    # print("\n\n",query)
    # Send a request to Google
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # # Extract the text after "Featured snippet from the web"
    # snippet_div = soup.find(lambda tag: tag.name == "div" and "Featured snippet from the web" in tag.text)
    if soup.text:
        snippet_text = soup.text
        # print("\n\n",snippet_text)
        # Use regex to extract the result string
        patterns = [
            r'(\w+\s\d+-\d+\s\w+\s\(\w+\s\d+,\s\d+\)\sFinal Score - ESPN\.)',
            r'([A-Za-z\s]+\d+-\d+\s[A-Za-z\s]+\(\w+\s\d+,\s\d+\)\sFinal\sScore\s-\sESPN)',
            r'([A-Za-z\s]+\d+-\d+\s[A-Za-z\s]+\(\w+\s\d+,\s\d+\)\sFinal ScoreESPN)'
        ]

        # Try each pattern until one matches
        match = None
        for pattern in patterns:
            result_pattern = re.compile(pattern)
            match = result_pattern.search(snippet_text)
            if match:
                break

        if match:
            result_str = match.group(1)
            # Use another regex to extract scores from the result string
            score_pattern = re.compile(r'(\d+)-(\d+)')
            score_match = score_pattern.search(result_str)
            # print("\n\n",score_match)
            
            if score_match:
                team1_score, team2_score = int(score_match.group(1)), int(score_match.group(2))
                scorelines = f"{team1_score}-{team2_score}"
                if team1_score > team2_score:
                    winner = team1
                elif team2_score > team1_score:
                    winner = team2
                else:
                    winner = "Draw"
            else:
                winner, scorelines = None, None
        else:
            winner, scorelines = None, None
    else:
        winner, scorelines = None, None
    
    return winner, scorelines

