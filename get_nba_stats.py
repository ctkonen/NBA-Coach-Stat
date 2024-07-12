from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup
import time

def scrape_team_statistics(year):
    url = f"https://www.nba.com/stats/teams/misc?SeasonType=Regular+Season&Season={year}"
    
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    # Find the table element using XPath
    try:
        table_element = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody')
    except:
        print(f"Table not found for season {year}")
        driver.quit()
        return None

    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Extract the table data into a list of rows
    table_html = str(table_element.get_attribute('outerHTML'))
    table_soup = BeautifulSoup(table_html, 'html.parser')
    rows = table_soup.find_all('tr')

    # Parse the rows into a DataFrame
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        data.append(cols)

    # Create the DataFrame
    df = pd.DataFrame(data)
    df['season'] = year

    return df

# Convert year format
def convert_year(year):
    end_year = year + 1
    end_year = str(end_year)
    year = str(year)
    end_year = end_year[-2:]
    year = f'{year}-{end_year}'
    print(year)
    return year

# List of years to scrape
years = range(1996, 1997)
years = [convert_year(year) for year in years]

# Collect statistics for all teams
all_team_stats = []
for year in years:
    team_stats = scrape_team_statistics(year)
    if team_stats is not None:
        all_team_stats.append(team_stats)
    # Sleep for 2 seconds between requests
    time.sleep(2)

# Concatenate all DataFrames
if all_team_stats:
    df = pd.concat(all_team_stats, ignore_index=True)

    nba_teams = {
        'Atlanta Hawks': 'ATL',
        'Boston Celtics': 'BOS',
        'Charlotte Hornets': 'CHA',
        'Chicago Bulls': 'CHI',
        'Cleveland Cavaliers': 'CLE',
        'Dallas Mavericks': 'DAL',
        'Denver Nuggets': 'DEN',
        'Detroit Pistons': 'DET',
        'Golden State Warriors': 'GSW',
        'Houston Rockets': 'HOU',
        'Indiana Pacers': 'IND',
        'Los Angeles Clippers': 'LAC',
        'Los Angeles Lakers': 'LAL',
        'Memphis Grizzlies': 'MEM',
        'Miami Heat': 'MIA',
        'Milwaukee Bucks': 'MIL',
        'Minnesota Timberwolves': 'MIN',
        'New Jersey Nets': 'NJN',
        'New Orleans Hornets': 'NOH',
        'New York Knicks': 'NYK',
        'Oklahoma City Thunder': 'OKC',
        'Orlando Magic': 'ORL',
        'Philadelphia 76ers': 'PHI',
        'Phoenix Suns': 'PHO',
        'Portland Trail Blazers': 'POR',
        'Sacramento Kings': 'SAC',
        'San Antonio Spurs': 'SAS',
        'Toronto Raptors': 'TOR',
        'Utah Jazz': 'UTA',
        'Washington Wizards': 'WAS',
        'Seattle SuperSonics': 'OKC',  # Moved and became the Oklahoma City Thunder
        'New Orleans Pelicans': 'NOH',  # Originally New Orleans Hornets before rebranding
        'Washington Bullets': 'WAS',  # Rebranded to Washington Wizards
        'Brooklyn Nets': 'NJN',  # Previously the New Jersey Nets
        'Vancouver Grizzlies': 'MEM',  # Moved and became the Memphis Grizzlies
        'Charlotte Bobcats': 'CHA'  # Rebranded back to Charlotte Hornets
    }

    df['team'] = df[0].map(nba_teams)

    # Display the DataFrame
    print(df)

    # Save to CSV if needed
    df.to_csv('nba_misc_stats.csv', index=False)
else:
    print("No data collected.")
