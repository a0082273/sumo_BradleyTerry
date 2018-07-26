# -*- coding: utf-8 -*-
import pandas as pd
import re


for day in range(1, 16):
    url = 'https://sports.yahoo.co.jp/sumo/torikumi/stats?bashoId=201805&day='
    url = url+str(day)
    fetched_dataframes = pd.read_html(url)
    day_torikumi = fetched_dataframes[1]
    day_torikumi.columns = ['e_banduke', 'e_rikishi', 'e_win', 'kimarite', 'w_win', 'w_rikishi', 'w_banduke']


    num = '[0-9]'
    for col in range(day_torikumi.shape[0]):
        torikumi = day_torikumi.iloc[col]

        num_str = re.search(num, torikumi['e_rikishi'])
        torikumi['e_rikishi'] = torikumi['e_rikishi'][:num_str.start()]

        torikumi['e_win'] = ord(torikumi['e_win'])
        if torikumi['e_win'] == 9675:
            torikumi['e_win'] = 1
        elif torikumi['e_win'] == 9679:
            torikumi['e_win'] = 0
        elif torikumi['e_win'] == 9632 or torikumi['e_win'] == 9633:
            torikumi['e_win'] = -1

        torikumi['w_win'] = ord(torikumi['w_win'])
        if torikumi['w_win'] == 9675:
            torikumi['w_win'] = 1
        elif torikumi['w_win'] == 9679:
            torikumi['w_win'] = 0
        elif torikumi['w_win'] == 9632 or torikumi['w_win'] == 9633:
            torikumi['w_win'] = -1

        num_str = re.search(num, torikumi['w_rikishi'])
        torikumi['w_rikishi'] = torikumi['w_rikishi'][:num_str.start()]

    num_str = re.search(num, url)
    day_torikumi.to_csv(f'torikumi_data/{url[num_str.start():]}.csv')
    print(f'day={day}')
