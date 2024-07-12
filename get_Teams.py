import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_team_statistics(team_abbr):
    url = f"https://www.basketball-reference.com/teams/{team_abbr}/"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch page for team {team_abbr}. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Initialize an empty list to hold the stats
    all_stats = []

    # Define the selectors for each stat
    stat_selectors = {
        'season': 'th[data-stat="season"] a',
        'wins': 'td[data-stat="wins"]',
        'losses': 'td[data-stat="losses"]',
        'win_loss_pct': 'td[data-stat="win_loss_pct"]',
        'rank_team': 'td[data-stat="rank_team"]',
        'srs': 'td[data-stat="srs"]',
        'pace': 'td[data-stat="pace"]',
        'rel_pace': 'td[data-stat="pace_rel"]',
        'off_rtg': 'td[data-stat="off_rtg"]',
        'rel_off_rtg': 'td[data-stat="off_rtg_rel"]',
        'def_rtg': 'td[data-stat="def_rtg"]',
        'rel_def_rtg': 'td[data-stat="def_rtg_rel"]',
        'playoffs': 'td[data-stat="rank_team_playoffs"]',
        'coaches': 'td[data-stat="coaches"]'
    }

    # Find all rows in the table with the team ID
    rows = soup.select(f'#{team_abbr} tbody tr')

    for row in rows:
        stats = {'team': team_abbr}
        for key, selector in stat_selectors.items():
            try:
                element = row.select_one(selector)
                if element and element.a:  # If there's an anchor tag within the element
                    stats[key] = element.a.text
                else:
                    stats[key] = element.get_text().strip()
            except AttributeError:
                stats[key] = 'N/A'
        all_stats.append(stats)
        print(f"Season: {stats.get('season', 'N/A')}, Team: {team_abbr}, Wins: {stats.get('wins', 'N/A')}, Losses: {stats.get('losses', 'N/A')}")

    return all_stats

# List of NBA team abbreviations
nba_teams = ['ATL', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NJN', 'NOH', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

# Collect statistics for all teams
all_team_stats = []
for team in nba_teams:
    team_stats = scrape_team_statistics(team)
    if team_stats:
        all_team_stats.extend(team_stats)
    # Sleep for 2 seconds between requests
    time.sleep(2)

# Convert the collected data into a DataFrame
df = pd.DataFrame(all_team_stats)

# Display the DataFrame
print(df)

# Save to CSV if needed
df.to_csv('team_core.csv', index=False)


