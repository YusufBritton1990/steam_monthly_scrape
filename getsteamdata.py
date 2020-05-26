import requests
import os

# All active steam games
steam_games_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
r = requests.get(steam_games_url)
steam_json = r.json()

game_id_list = []

for game in steam_json['applist']['apps'] : # list game ids for steam charts
    game_id_list.append(game['appid'])

print(game_id_list[0:10])

# TODO: Need to account for pages without data. Some may not exist

# format to make call

# https://steamcharts.com/app/752590 #successful call

# https://steamcharts.com/app/216938 #unsuccessful call
