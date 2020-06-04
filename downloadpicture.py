import requests #HTTP requests to steam API and steamcharts
import os
from bs4 import BeautifulSoup #get game data from steamcharts
import timeit
import pandas as pd #reading data_clean

from PIL import Image
from io import BytesIO

# TODO: When saving pictures, need to not include special characters

start = timeit.timeit()
print('Saving Images')

# Storing df of the top ten peak users by month
df = pd.read_csv('pics/monthly_top10.csv')

# # Getting unique list of top ten df
# game_id_series = monthly_top10_df.game_id
# unique_game_id_list = list(game_id_series.unique())

# subsetting i
subset_df = df[['game_id', 'game_title']]
subset_df.drop_duplicates(inplace = True)
subset_df.sort_values(by=['game_title'], inplace=True)
subset_df.reset_index(inplace=True)

# print(subset_df)

# id_list = list(subset_df.game_id)
# game_list = list(subset_df.game_title)
# print(subset_df.count())

# print(len(id_list), len(game_list))
# print(game_list)

# Test
for index, row in subset_df.iterrows(): #exclude the .head(10)
     # access data using column names
    print(row['game_id'], row['game_title'])

    # game_id = row['game_id']
    pic_url =  f'https://steamcdn-a.akamaihd.net/steam/apps/{row["game_id"]}/logo.png'
    r = requests.get(pic_url)

    if r.ok:
    #If there is an image online, read in the data as bytes
        img = Image.open(BytesIO(r.content))
    else:
    #If there isn't an image online, save a default image
        img = Image.open("steam-logo-default-small.png")

    # formatting filename to align with Tableau auto Align
    filename = "{:03d}".format(index)
    # img.save(f"pics/{index}.png")
    img.save(f"pics/{filename}.png")

# for loop to download pictures
# for i in range(len(id_list)):
#     pic_url =  f'https://steamcdn-a.akamaihd.net/steam/apps/{id_list[i]}/logo.png'
#     r = requests.get(pic_url)
#
#     if r.ok:
#         #If there is an image online, read in the data as bytes
#         img = Image.open(BytesIO(r.content))
#     else:
#         #If there isn't an image online, save a default image
#         img = Image.open("steam-logo-default-small.png")
#
#     img.save(f"pics/{game_list[i]}.png")
# print('Images saved')

end = timeit.timeit()
print(end - start)
