import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

url = "https://www.basketball-reference.com/friv/continuity.html"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

# Initialize an empty list to hold the stats
all_stats = []

# Define the selectors for each stat
stat_selectors = {
    'season': 'th[data-stat="season"] a',
    'ATL': 'td[data-stat="ATL"]',
    'BOS': 'td[data-stat="BOS"]',
    'CHA': 'td[data-stat="CHA"]',
    'CHI': 'td[data-stat="CHI"]',
    'CLE': 'td[data-stat="CLE"]',
    'DAL': 'td[data-stat="DAL"]',
    'DEN': 'td[data-stat="DEN"]',
    'DET': 'td[data-stat="DET"]',
    'GSW': 'td[data-stat="GSW"]',
    'HOU': 'td[data-stat="HOU"]',
    'IND': 'td[data-stat="IND"]',
    'LAC': 'td[data-stat="LAC"]',
    'LAL': 'td[data-stat="LAL"]',
    'MEM': 'td[data-stat="MEM"]',
    'MIA': 'td[data-stat="MIA"]',
    'MIL': 'td[data-stat="MIL"]',
    'MIN': 'td[data-stat="MIN"]',
    'NJN': 'td[data-stat="NJN"]',
    'NOH': 'td[data-stat="NOH"]',
    'NYK': 'td[data-stat="NYK"]',
    'OKC': 'td[data-stat="OKC"]',
    'ORL': 'td[data-stat="ORL"]',
    'PHI': 'td[data-stat="PHI"]',
    'PHO': 'td[data-stat="PHO"]',
    'POR': 'td[data-stat="POR"]',
    'SAC': 'td[data-stat="SAC"]',
    'SAS': 'td[data-stat="SAS"]',
    'TOR': 'td[data-stat="TOR"]',
    'UTA': 'td[data-stat="UTA"]',
    'WAS': 'td[data-stat="WAS"]'
}

# Find all rows in the table with the team ID
rows = soup.select('tbody tr')

for row in rows:
    stats = {}
    for key, selector in stat_selectors.items():
        try:
            element = row.select_one(selector)
            if element and element.a:  # If there's an anchor tag within the element
                stats[key] = element.a.text
            else:
                stats[key] = element.get_text().strip()
        except AttributeError:
            stats[key] = 'N/A'
    print(stats)
    all_stats.append(stats)
    print(f"Season: {stats.get('season', 'N/A')}")

# Convert the collected data into a DataFrame
df = pd.DataFrame(all_stats)

# Display the DataFrame
print(df)

rost_cont_long = df.melt(id_vars=['season'], var_name='team', value_name='roster_continuity')

# Save to CSV if needed
rost_cont_long.to_csv('rost_cont.csv', index=False)
