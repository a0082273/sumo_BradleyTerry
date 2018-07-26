# -*- coding: utf-8 -*-
import pandas as pd


for day in range(1, 16):
    fname = '201805&day='
    fname = fname+str(day)
    day_torikumi = pd.read_csv(f'torikumi_data/{fname}.csv', index_col=0)

    day_torikumi = day_torikumi.drop(['e_banduke', 'kimarite', 'w_banduke'], axis=1)
    day_torikumi = day_torikumi.loc[:, ['e_rikishi', 'w_rikishi', 'e_win', 'w_win']]

    day_torikumi = day_torikumi[day_torikumi['e_win'] != -1]

#for same level in BradleyTerry2
    day_torikumi_inv = day_torikumi.loc[:, ['w_rikishi', 'e_rikishi', 'w_win', 'e_win']]
    day_torikumi_inv.columns = ['e_rikishi', 'w_rikishi', 'e_win', 'w_win']
    day_torikumi = day_torikumi.append(day_torikumi_inv)

    day_torikumi.to_csv(f'torikumi_btmodel_data/{fname}_bt.csv')


    if day == 1:
        basho_torikumi = day_torikumi
    else:
        basho_torikumi = basho_torikumi.append(day_torikumi)
basho_torikumi = basho_torikumi.reset_index(drop=True)

#only non_ketsujo fighter
# not_kyujo_rikishi = day_torikumi['e_rikishi']
# nkrl = not_kyujo_rikishi.values.tolist()
# basho_torikumi = basho_torikumi[basho_torikumi['e_rikishi'].isin(nkrl)]
# basho_torikumi = basho_torikumi[basho_torikumi['w_rikishi'].isin(nkrl)]
# basho_torikumi = basho_torikumi.reset_index(drop=True)


basho_torikumi.to_csv(f'torikumi_btmodel_data/{fname[:6]}_bt_all.csv')
# basho_torikumi.to_csv(f'torikumi_btmodel_data/{fname[:6]}_bt_rm_ketsujo.csv')
