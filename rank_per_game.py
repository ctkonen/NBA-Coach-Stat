import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_team_statistics(team_abbr):
    url = f"https://www.basketball-reference.com/teams/{team_abbr}/stats_per_game_ranks.html"
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
        'avg_age_rank': 'td[data-stat="avg_age"]',
        'avg_height_rank': 'td[data-stat="avg_ht"]',
        'avg_weight_rank': 'td[data-stat="avg_wt"]',
        'fg_rank': 'td[data-stat="fg_per_g"]',
        'fga_rank': 'td[data-stat="fga_per_g"]',
        'fg_pct_rank': 'td[data-stat="fg_pct"]',
        '3p_rank': 'td[data-stat="fg3_per_g"]',
        '3pa_rank': 'td[data-stat="fg3a_per_g"]',
        '3p_pct_rank': 'td[data-stat="fg3_pct"]',
        '2p_rank': 'td[data-stat="fg2_per_g"]',
        '2pa_rank': 'td[data-stat="fg2a_per_g"]',
        '2p_pct_rank': 'td[data-stat="fg2_pct"]',
        'ft_rank': 'td[data-stat="ft_per_g"]',
        'fta_rank': 'td[data-stat="fta_per_g"]',
        'ft_pct_rank': 'td[data-stat="ft_pct"]',
        'orb_rank': 'td[data-stat="orb_per_g"]',
        'drb_rank': 'td[data-stat="drb_per_g"]',
        'trb_rank': 'td[data-stat="trb_per_g"]',
        'ast_rank': 'td[data-stat="ast_per_g"]',
        'stl_rank': 'td[data-stat="stl_per_g"]',
        'blk_rank': 'td[data-stat="blk_per_g"]',
        'tov_rank': 'td[data-stat="tov_per_g"]',
        'pf_rank': 'td[data-stat="pf_per_g"]',
        'pts_rank': 'td[data-stat="pts_per_g"]',
    }

    # Find all rows in the table with the team ID
    rows = soup.select('#stats tbody tr')

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
        print(f"Season: {stats.get('season', 'N/A')}, Team: {team_abbr}, FG: {stats.get('fg', 'N/A')}, FGA: {stats.get('fga', 'N/A')}")

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
df.to_csv('rank_per_game.csv', index=False)
