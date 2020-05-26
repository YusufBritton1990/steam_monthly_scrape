import requests #HTTP requests to steam API and steamcharts
import os
from bs4 import BeautifulSoup #get game data from steamcharts

"""All active steam games, using Steam API"""
steam_games_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
r = requests.get(steam_games_url)
steam_json = r.json() #JSON of all active steam games

game_id_list = []
for game in steam_json['applist']['apps'] : # game ids needed for steam charts
    game_id_list.append(game['appid'])

"""Steam scrape, from steam charts"""
# steam_monthly_url = 'https://steamcharts.com/app/752590' #successful call
# r = requests.get(steam_monthly_url)
# print(r.status_code) #return 200 (success)
# print(r.ok) #return True (page found)

# steam_monthly_url = 'https://steamcharts.com/app/216938' #unsuccessful call
# r = requests.get(steam_monthly_url)
# print(r.status_code) #return 404 (page not found)
# print(r.ok) #Returns False (page not found)

raw_data_list = []

# TODO: for picture_url, might need to make a default picture if image doesn't show
game_id = 752590
picture_url = f'https://steamcdn-a.akamaihd.net/steam/apps/{game_id}/logo.png'
steam_monthly_url = f'https://steamcharts.com/app/{game_id}' #successful call
r = requests.get(steam_monthly_url)
html_doc = r.text
soup = BeautifulSoup(html_doc, 'html.parser')

game_title = soup.find(id="app-title").text
print(game_title)

table = soup.find('tbody')
monthly_data_list = table.find_all('tr')# iterable monthly data
month_interable = monthly_data_list[0]

# TODO: convert into datetime object
month = month_interable.find(class_="month-cell").text
peak_users = int(month_interable.find(class_="num").text)

raw_data_list.append([game_id, game_title, month, peak_users, picture_url])
print(raw_data_list)

"""list of data: game_id, game, month, peak_users, picture_url"""
labels = ['game_id', 'game_title', 'month', 'peak_users','picture_url']

# Make call for a game
# If call is successful, read in html
# In html, read in the table with monthly data
# in monthly data, append to list of raw data
# after append, convert into a excel file
