import pandas as pd
import numpy as np
import re
import sys
import pyper
from time import sleep



def get_torikumi_data():
    print('get_torikumi_data')
    url_base = 'https://sports.yahoo.co.jp/sumo/torikumi/stats?'
    for day in range(1, 16):
    # for day in range(15, 16):
        url = url_base+f'bashoId={bashoId}&day={day}'
        fetched_dataframes = pd.read_html(url)
        if fetched_dataframes[1].shape[0] > 10: #優勝決定戦がない場合
            day_torikumi = fetched_dataframes[1]
        else:
            day_torikumi = pd.concat([fetched_dataframes[1], fetched_dataframes[2]], axis=0)
            day_torikumi.reset_index()
        day_torikumi = cleansing(day_torikumi)
        df2csv(url, day_torikumi)
        print(f'basho:{bashoId}   day:{day}')
        sleep(3)


def cleansing(day_torikumi):
    day_torikumi.columns = ['e_banduke', 'e_rikishi', 'e_win', 'kimarite', 'w_win', 'w_rikishi', 'w_banduke']
    num = '[0-9]'
    for col in range(day_torikumi.shape[0]):
        torikumi = day_torikumi.iloc[col]

        num_str = re.search(num, torikumi['e_rikishi'])
        if num_str != None:
            torikumi['e_rikishi'] = torikumi['e_rikishi'][:num_str.start()]

        torikumi['e_win'] = ord(torikumi['e_win'])
        if torikumi['e_win'] == 9675: #勝ち
            torikumi['e_win'] = 1.0
        elif torikumi['e_win'] == 9679: #負け
            torikumi['e_win'] = 0.0
        elif torikumi['e_win'] == 9633: #不戦勝
            torikumi['e_win'] = 1.01
        elif torikumi['e_win'] == 9632: #不戦敗
            torikumi['e_win'] = -0.1

        torikumi['w_win'] = ord(torikumi['w_win'])
        if torikumi['w_win'] == 9675:
            torikumi['w_win'] = 1.0
        elif torikumi['w_win'] == 9679:
            torikumi['w_win'] = 0.0
        elif torikumi['w_win'] == 9633:
            torikumi['w_win'] = 1.01
        elif torikumi['w_win'] == 9632:
            torikumi['w_win'] = -0.1

        num_str = re.search(num, torikumi['w_rikishi'])
        if num_str != None:
            torikumi['w_rikishi'] = torikumi['w_rikishi'][:num_str.start()]

    return day_torikumi


def df2csv(url, day_torikumi):
    num = '[0-9]'
    num_str = re.search(num, url)
    day_torikumi.to_csv(f'input/torikumi_data/{url[num_str.start():]}.csv')



def transform_data_for_btmodel():
    print('transform_data_for_btmodel')
    for day in range(1, 16):
        fname = f'{bashoId}&day={day}'
        day_torikumi = pd.read_csv(f'input/torikumi_data/{fname}.csv', index_col=0)

        day_torikumi = day_torikumi.drop(['e_banduke', 'kimarite', 'w_banduke'], axis=1)
        day_torikumi = day_torikumi.loc[:, ['e_rikishi', 'w_rikishi', 'e_win', 'w_win']]

        # for same level in BradleyTerry2
        day_torikumi_inv = day_torikumi.loc[:, ['w_rikishi', 'e_rikishi', 'w_win', 'e_win']]
        day_torikumi_inv.columns = ['e_rikishi', 'w_rikishi', 'e_win', 'w_win']
        day_torikumi = day_torikumi.append(day_torikumi_inv)

        day_torikumi.to_csv(f'input/torikumi_btmodel_data/{fname}_bt.csv')


        if day == 1:
            basho_torikumi = day_torikumi
        else:
            basho_torikumi = basho_torikumi.append(day_torikumi)
    basho_torikumi = basho_torikumi.reset_index(drop=True)

    grouped = basho_torikumi.groupby('e_rikishi')
    n_win = round(grouped.sum()['e_win']).astype(int)
    n_lose = round(grouped.sum()['w_win']).astype(int)
    n_uwin = (grouped.sum()['e_win']*100)%10 #不戦勝
    n_uwin = n_uwin.astype(int)
    n_ulose = (grouped.sum()['w_win']*100)%10 #不戦敗
    n_ulose = n_ulose.astype(int)
    n_torikumi = round(grouped.sum()['e_win']+grouped.sum()['w_win']).astype(int)
    n_kyujo = 15-n_torikumi
    ok_rikishi = n_torikumi[n_torikumi >= 10].index
    rikishi_status = pd.concat([n_win, n_lose, n_uwin, n_ulose, n_kyujo], axis=1)
    # rikishi_status = pd.concat([n_win, n_torikumi], axis=1)

    basho_torikumi = basho_torikumi[basho_torikumi['e_rikishi'].isin(ok_rikishi)]
    basho_torikumi = basho_torikumi[basho_torikumi['w_rikishi'].isin(ok_rikishi)]
    basho_torikumi = basho_torikumi.reset_index(drop=True)
    basho_torikumi['e_win'] = basho_torikumi['e_win'].astype(int)
    basho_torikumi['w_win'] = basho_torikumi['w_win'].astype(int)

    basho_torikumi.to_csv(f'input/torikumi_btmodel_data/{fname[:6]}_bt.csv')
    rikishi_status.to_csv(f'output/{bashoId}_rikishi_status.csv')



def bradley_terry():
    print('bradley_terry')
    r = pyper.R()
    r.assign('bashoId', bashoId)
    r("source(file='bt_model.R')")



def transform_data_for_visualize():
    print('transform_data_for_visualize')
    bt_ability = pd.read_csv(f'input/bt_ability/{bashoId}_bt_ability.csv', index_col=0)
    rikishi_status = pd.read_csv(f'output/{bashoId}_rikishi_status.csv', index_col=0)

    rikishi_status = pd.concat([bt_ability, rikishi_status], axis=1)
    rikishi_status = rikishi_status.sort_values('ability', ascending = False)
    rikishi_status.columns = ['bt_ability', 'bt_s.e.', 'n_win', 'n_lose', 'n_uwin', 'n_ulose', 'n_kyujo']
    # rikishi_status['bt_ability'] = min_max_normalization(rikishi_status['bt_ability'])
    rikishi_status['rank'] = range(1, rikishi_status.shape[0]+1)
    rikishi_status = rikishi_status[rikishi_status.notnull().all(axis=1)]

    rikishi_status.to_csv(f'output/{bashoId}_rikishi_status.csv')


# def min_max_normalization(x):
#     x_new = (x - x.min()) / (x.max() - x.min())
#     return x_new


# def z_score_normalization():



if __name__ == '__main__':
    year_list = [
        '2001', '2002', '2003', '2004', '2005',
        '2006', '2007', '2008', '2009', '2010', '2011',
        '2012', '2013', '2014',
        '2015', '2016', '2017', '2018'
    ]
    basho_list = ['01', '03', '05', '07', '09', '11']
    for year in year_list:
        for basho in basho_list:
            bashoId = year+basho
            get_torikumi_data()
            transform_data_for_btmodel()
            bradley_terry()
            transform_data_for_visualize()


    # year = '2011'
    # basho_list = ['07', '09', '11']
    # for basho in basho_list:
    #     bashoId = year+basho
    #     get_torikumi_data()
    #     transform_data_for_btmodel()
    #     bradley_terry()
    #     transform_data_for_visualize()


    # bashoId = '201709'
    # get_torikumi_data()
    # transform_data_for_btmodel()
    # bradley_terry()
    # transform_data_for_visualize()


#200205, 201103, 201105はデータが丸々ない
