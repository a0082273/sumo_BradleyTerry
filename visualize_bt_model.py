# -*- coding: utf-8 -*-
import pandas as pd


bt_ability = pd.read_csv('torikumi_btmodel_data/201805_bt_ability_all.csv', index_col=0)
basho_torikumi = pd.read_csv('torikumi_btmodel_data/201805_bt_all.csv', index_col=0)
# bt_ability = pd.read_csv('torikumi_btmodel_data/bt_ability_rm_ketsujo.csv', index_col=0)
# basho_torikumi = pd.read_csv('torikumi_btmodel_data/201807_bt_rm_ketsujo.csv', index_col=0)

grouped = basho_torikumi.groupby('e_rikishi')
n_win = grouped.sum()['e_win']
rikishi_status = pd.concat([bt_ability, n_win], axis=1)

#for rikishi_status_all.csv
rikishi_status = rikishi_status[grouped.sum()['e_win'] + grouped.sum()['w_win'] >= 10]

rikishi_status = rikishi_status.sort_values('ability', ascending = False)
rikishi_status.columns = ['bt_ability', 'bt_s.e.', 'wins']

rikishi_status.to_csv('torikumi_btmodel_data/201805_rikishi_status_all.csv')
# rikishi_status.to_csv('torikumi_btmodel_data/rikishi_status_rm_ketsujo.csv')
