import requests #HTTP requests to steam API and steamcharts
import os
from bs4 import BeautifulSoup #get game data from steamcharts
import timeit
import pandas as pd

start = timeit.timeit()

"""All active steam games, using Steam API"""
steam_games_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
r = requests.get(steam_games_url)
steam_json = r.json() #JSON of all active steam games

game_id_list = []
for game in steam_json['applist']['apps'] : # game ids needed for steam charts
    game_id_list.append(game['appid'])

"""Make call for a game"""
raw_data_list = []
for game_id in game_id_list:
    steam_monthly_url = f'https://steamcharts.com/app/{game_id}'
    r = requests.get(steam_monthly_url)

    if r.ok : # If call is successful, read in html
        # Use another site to get URL to logo image on Steam
        picture_url = f'https://steamcdn-a.akamaihd.net/steam/apps/{game_id}/logo.png'

        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'html.parser')

        game_title = soup.find(id="app-title").text

        # In html, read in the table with monthly data
        table = soup.find('tbody')
        monthly_data_list = table.find_all('tr')# iterable monthly data
        for month_interable in monthly_data_list:
            # TODO: convert into datetime object
            month = month_interable.find(class_="month-cell").text
            peak_users = int(month_interable.find(class_="num").text)

            # in monthly data, append to list of raw data
            raw_data_list.append([game_id, game_title, month, peak_users, picture_url])
            percentage_complete = (game_id_list.index(game_id)+ 1)/len(game_id_list)

            print(game_title + ': Successfully appended for -- ' + month)
            print('percentage completed: ' + str(percentage_complete))

# after append, convert into a excel file
labels = ['game_id', 'game_title', 'month', 'peak_users','picture_url']

df = pd.DataFrame.from_records(raw_data_list, columns=labels)
df.to_csv('data.csv')

end = timeit.timeit()
print(end - start)
