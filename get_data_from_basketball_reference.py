
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

def get_data_from_basketball_reference(year_start, year_end):

    list_data = []
    for year in range(year_start, year_end+1):
        url = f'https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html'
        html = urlopen(url)
        soup = BeautifulSoup(html)
        headers = [th.getText() for th in soup.find_all('tr')[0].find_all('th')]
        headers = headers[1:] + ['Season'] # columns
        
        rows = soup.find_all('tr')
        player_stats_1 = [[td.getText() for td in rows[i].find_all('td')] for i in range(len(rows))]  # rows

        for row in player_stats_1:
            if row:  
                row.append(str(year))

        tmp_df = pd.DataFrame(player_stats_1, columns=headers)
        tmp_mat = tmp_df.values
        list_data.append(tmp_mat)

    return list_data, headers


def get_data_from_nba(years):

    list_data = []
    for year in years:
        url = f'https://www.nba.com/stats/players/advanced?SeasonType=Regular+Season&Season={year}'
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        trs = soup.find_all('table')
        print(trs)
"""
        headers = [th.getText() for th in soup.find_all('tr', class_='com_headers__mzI_m')[0].find_all('th')]
        print(headers)
         # columns
        
        rows = soup.find('tbody', class_='Crom_body__UYOcU').find_all('tr')
        player_stats_1 = [[td.getText() for td in rows[i].find_all('td')] for i in range(len(rows))]  # rows

        tmp_df = pd.DataFrame(player_stats_1, columns=headers)
        tmp_mat = tmp_df.values
        list_data.append(tmp_mat)

    return list_data, headers
"""

def build_df(data,  columns):
    df = pd.DataFrame(data[0][1:], columns=columns)
    for i in range(1, len(data)):
        tmp_df = pd.DataFrame(data[i], columns=columns)
        df = pd.concat([df, tmp_df], ignore_index=True)
    return df


def create_csv(path, df: pd.DataFrame):
    df.to_csv(path, index=False)
    
    

#data, columns = get_data_from_basketball_reference(2015, 2024)

data, columns = get_data_from_nba(['2023-24'])
#df = build_df(data, columns)
#create_csv('advanced_data_2023_24.csv', df)