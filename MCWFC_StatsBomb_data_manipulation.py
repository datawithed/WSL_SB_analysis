# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 21:06:25 2022

@author: Ed.Morris
"""

# StatsBomb FA WSL 2018/19 - 2020/2021 data

# MCWFC season analysis

# Import modules
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsbombpy import sb
from mplsoccer import VerticalPitch, Pitch
import streamlit as st
import openpyxl
import os

# Set wd path
file_path = r"C:\Users\ed.morris\Documents\Python Scripts\WSL"
os.chdir(file_path)

# Set StatsBomb API IDs
comp_id = 37 # FA WSL
season_id1 = 4 # 2018/2019
season_id2 = 42 # 2019/2020
season_id3 = 90 # 2020/2021

# Call matches for each season using comp_id and season_id
season1_matches = sb.matches(competition_id = comp_id, season_id = season_id1)
season2_matches = sb.matches(competition_id = comp_id, season_id = season_id2)
season3_matches = sb.matches(competition_id = comp_id, season_id = season_id3)

# Filter team for MCWFC
mcwfc_matches1 = season1_matches.loc[(season1_matches.home_team == 'Manchester City WFC') | (season1_matches.away_team == 'Manchester City WFC')].reset_index(drop = True)
mcwfc_matches2 = season2_matches.loc[(season2_matches.home_team == 'Manchester City WFC') | (season2_matches.away_team == 'Manchester City WFC')].reset_index(drop = True)
mcwfc_matches3 = season3_matches.loc[(season3_matches.home_team == 'Manchester City WFC') | (season3_matches.away_team == 'Manchester City WFC')].reset_index(drop = True)

# Filter team for CFC
cfc_matches1 = season1_matches.loc[(season1_matches.home_team == 'Chelsea FCW') | (season1_matches.away_team == 'Chelsea FCW')].reset_index(drop = True)
cfc_matches2 = season2_matches.loc[(season2_matches.home_team == 'Chelsea FCW') | (season2_matches.away_team == 'Chelsea FCW')].reset_index(drop = True)
cfc_matches3 = season3_matches.loc[(season3_matches.home_team == 'Chelsea FCW') | (season3_matches.away_team == 'Chelsea FCW')].reset_index(drop = True)

# Filter for Arsenal
afc_matches1 = season1_matches.loc[(season1_matches.home_team == 'Arsenal WFC') | (season1_matches.away_team == 'Arsenal WFC')].reset_index(drop = True)
afc_matches2 = season2_matches.loc[(season2_matches.home_team == 'Arsenal WFC') | (season2_matches.away_team == 'Arsenal WFC')].reset_index(drop = True)
afc_matches3 = season3_matches.loc[(season3_matches.home_team == 'Arsenal WFC') | (season3_matches.away_team == 'Arsenal WFC')].reset_index(drop = True)

# Filter for Birmingham City WFC
bcfc_matches1 = season1_matches.loc[(season1_matches.home_team == 'Birmingham City WFC') | (season1_matches.away_team == 'Birmingham City WFC')].reset_index(drop = True)
bcfc_matches2 = season2_matches.loc[(season2_matches.home_team == 'Birmingham City WFC') | (season2_matches.away_team == 'Birmingham City WFC')].reset_index(drop = True)
bcfc_matches3 = season3_matches.loc[(season3_matches.home_team == 'Birmingham City WFC') | (season3_matches.away_team == 'Birmingham City WFC')].reset_index(drop = True)

# Create list to pull match_ids into lists for each season
def list_match_ids(match1, match2, match3):
    match_ids1 = []
    match_ids2 = []
    match_ids3 = []

    for i in range(len(match1)):
        x = match1.match_id[i]
        match_ids1.append(x)
    for i in range(len(match2)):
        x = match2.match_id[i]
        match_ids2.append(x)
    for i in range(len(match3)):
        x = match3.match_id[i]
        match_ids3.append(x)
    
    return match_ids1, match_ids2, match_ids3

# Pull Arsenal, Chelsea and MCWFC match ids
mcwfc_matches_1, mcwfc_matches_2, mcwfc_matches_3 = list_match_ids(mcwfc_matches1, mcwfc_matches2, mcwfc_matches3)
cfc_matches_1, cfc_matches_2, cfc_matches_3 = list_match_ids(cfc_matches1, cfc_matches2, cfc_matches3)
afc_matches_1, afc_matches_2, afc_matches_3 = list_match_ids(afc_matches1, afc_matches2, afc_matches3)
bcfc_matches_1, bcfc_matches_2, bcfc_matches_3 = list_match_ids(bcfc_matches1, bcfc_matches2, bcfc_matches3)

# Merge lists for all seasons match_ids
all_mcwfc_match_ids = mcwfc_matches_1 + mcwfc_matches_2 + mcwfc_matches_3
all_cfc_match_ids = cfc_matches_1 + cfc_matches_2 + cfc_matches_3
all_afc_match_ids = afc_matches_1 + afc_matches_2 + afc_matches_3
all_bcfc_match_ids = bcfc_matches_1 + bcfc_matches_2 + bcfc_matches_3

# Create seasonal match_ids
season1_match_ids = mcwfc_matches_1 + cfc_matches_1 + afc_matches_1 + bcfc_matches_1
season2_match_ids = mcwfc_matches_2 + cfc_matches_2 + afc_matches_2 + bcfc_matches_2
season3_match_ids = mcwfc_matches_3 + cfc_matches_3 + afc_matches_3 + bcfc_matches_3

# Remove duplicates for creation of lookup table later
season1_match_ids = list(dict.fromkeys(season1_match_ids))
season2_match_ids = list(dict.fromkeys(season2_match_ids))
season3_match_ids = list(dict.fromkeys(season3_match_ids))

# Pull shot event data from API using match_id lists
def get_shots(match_ids, events_list = []):
    for i in range(len(match_ids)):
        events = sb.events(match_id = match_ids[i])
        shots = events.loc[events.type == 'Shot']
        shots = shots[['match_id','team','player','minute','second','type','location','shot_end_location','shot_body_part','shot_outcome','shot_statsbomb_xg']]
        events_list.append(shots)
        x = pd.concat(events_list)
    
    return x

# Call shot data, filter for MCWFC, Arsenal and Chelsea
mcwfc_season1_shots = get_shots(mcwfc_matches_1)
mcwfc_season1_shots = mcwfc_season1_shots.loc[mcwfc_season1_shots.team == 'Manchester City WFC']
mcwfc_season2_shots = get_shots(mcwfc_matches_2)
mcwfc_season2_shots = mcwfc_season2_shots.loc[mcwfc_season2_shots.team == 'Manchester City WFC']
mcwfc_season3_shots = get_shots(mcwfc_matches_2)
mcwfc_season3_shots = mcwfc_season3_shots.loc[mcwfc_season3_shots.team == 'Manchester City WFC']
cfc_season1_shots = get_shots(cfc_matches_1)
cfc_season1_shots = cfc_season1_shots.loc[cfc_season1_shots.team == 'Chelsea FCW']
cfc_season2_shots = get_shots(cfc_matches_2)
cfc_season2_shots = cfc_season2_shots.loc[cfc_season2_shots.team == 'Chelsea FCW']
cfc_season3_shots = get_shots(cfc_matches_3)
cfc_season3_shots = cfc_season3_shots.loc[cfc_season3_shots.team == 'Chelsea FCW']
afc_season1_shots = get_shots(afc_matches_1)
afc_season1_shots = afc_season1_shots.loc[afc_season1_shots.team == 'Arsenal WFC']
afc_season2_shots = get_shots(afc_matches_2)
afc_season2_shots = afc_season2_shots.loc[afc_season2_shots.team == 'Arsenal WFC']
afc_season3_shots = get_shots(afc_matches_3)
afc_season3_shots = afc_season3_shots.loc[afc_season3_shots.team == 'Arsenal WFC']
bcfc_season1_shots = get_shots(bcfc_matches_1)
bcfc_shots = bcfc_season1_shots.loc[bcfc_season1_shots.team == 'Birmingham City WFC']

#all_shots = get_mcwfc_shots(all_match_ids)

mcwfc_shots = pd.concat([mcwfc_season1_shots, mcwfc_season2_shots, mcwfc_season3_shots]).reset_index(drop=True)
cfc_shots = pd.concat([cfc_season1_shots, cfc_season2_shots, cfc_season3_shots]).reset_index(drop=True)
afc_shots = pd.concat([afc_season1_shots, afc_season2_shots, afc_season3_shots]).reset_index(drop=True)

# Define function to split the start and end x/y coordinates into 4 separate columns
def location_split(shots_df):
    shots_df['start_x'] = 0
    shots_df['start_y'] = 0
    shots_df['end_x'] = 0
    shots_df['end_y'] = 0
    for i in range(len(shots_df)):
        shots_df['start_x'].iloc[i] = shots_df['location'].iloc[i][0]
        shots_df['start_y'].iloc[i] = shots_df['location'].iloc[i][1]
        shots_df['end_x'].iloc[i] = shots_df['shot_end_location'].iloc[i][0]
        shots_df['end_y'].iloc[i] = shots_df['shot_end_location'].iloc[i][1]
    
    return shots_df

mcwfc_season1_shots = location_split(mcwfc_season1_shots)
mcwfc_season2_shots = location_split(mcwfc_season2_shots)
mcwfc_season3_shots = location_split(mcwfc_season3_shots)
mcwfc_shots = location_split(mcwfc_shots)
cfc_season1_shots = location_split(cfc_season1_shots)
cfc_season2_shots = location_split(cfc_season2_shots)
cfc_season3_shots = location_split(cfc_season3_shots)
cfc_shots = location_split(cfc_shots)
afc_season1_shots = location_split(afc_season1_shots)
afc_season2_shots = location_split(afc_season2_shots)
afc_season3_shots = location_split(afc_season3_shots)
afc_shots = location_split(afc_shots)
bcfc_shots = location_split(bcfc_shots)

# Create match_id lookup by season
match_id_lookup1 = pd.DataFrame(season1_match_ids, columns = ['match_id'])
match_id_lookup1['season'] = 1
match_id_lookup2 = pd.DataFrame(season2_match_ids, columns = ['match_id'])
match_id_lookup2['season'] = 2
match_id_lookup3 = pd.DataFrame(season3_match_ids, columns = ['match_id'])
match_id_lookup3['season'] = 3
match_id_lookups = pd.concat([match_id_lookup1,match_id_lookup2,match_id_lookup3])

# Merge on match_id to create 'season' col
mcwfc_shots = pd.merge(mcwfc_shots,match_id_lookups,on='match_id',how='left')
cfc_shots = pd.merge(cfc_shots,match_id_lookups,on='match_id',how='left')
afc_shots = pd.merge(afc_shots,match_id_lookups,on='match_id',how='left')
bcfc_shots['season'] = 1

# Write data to excel file to save load each time
mcwfc_shots.to_csv('MCWFC_shots.csv')
cfc_shots.to_csv('Chelsea_FCW_shots.csv')
afc_shots.to_csv('Arsenal_WFC_shots.csv')
bcfc_shots.to_csv('Birmingham_City_WFC_shots.csv')


# Pull event data from API using match_id lists
def get_events(match_ids, team):
    events_list = []
    for i in range(len(match_ids)):
        events = sb.events(match_id = match_ids[i])
        events = events.loc[events.team == team]
        events = events.loc[events.type.isin(['Shot','Carry','Pass'])]
        events = events[['match_id','team','player','minute','second','type','location',
                         'shot_end_location','shot_body_part','shot_outcome',
                         'shot_statsbomb_xg','ball_receipt_outcome','carry_end_location',
                         'dribble_outcome','pass_body_part','pass_cross',
                         'pass_end_location','pass_length','pass_outcome','pass_recipient',
                         'shot_freeze_frame']]
        events_list.append(events)
        x = pd.concat(events_list)
    
    return x

all_mcwfc_events = get_events(all_mcwfc_match_ids, 'Manchester City WFC').reset_index(drop=True)
all_cfc_events = get_events(all_cfc_match_ids, 'Chelsea FCW').reset_index(drop=True)
all_afc_events = get_events(all_afc_match_ids, 'Arsenal WFC').reset_index(drop=True)
all_bcfc_events = get_events(all_bcfc_match_ids, 'Birmingham City WFC').reset_index(drop=True)

# Merge on match_id to create 'season' col
all_mcwfc_events = pd.merge(all_mcwfc_events,match_id_lookups,on='match_id',how='left')
all_cfc_events = pd.merge(all_cfc_events,match_id_lookups,on='match_id',how='left')
all_afc_events = pd.merge(all_afc_events,match_id_lookups,on='match_id',how='left')
all_bcfc_events = pd.merge(all_bcfc_events,match_id_lookups,on='match_id',how='left')

# Create x and y start/end coords for shot, pass and carry (each has own column)
def location_split_type(events_df):
    events_df['start_x'] = 0
    events_df['start_y'] = 0
    events_df['end_x'] = 0
    events_df['end_y'] = 0
    shot_df = events_df.loc[events_df.type == 'Shot']
    pass_df = events_df.loc[events_df.type == 'Pass']
    carry_df = events_df.loc[events_df.type == 'Carry']
    for i in range(len(shot_df)):
        shot_df['start_x'].iloc[i] = shot_df['location'].iloc[i][0]
        shot_df['start_y'].iloc[i] = shot_df['location'].iloc[i][1]
        shot_df['end_x'].iloc[i] = shot_df['shot_end_location'].iloc[i][0]
        shot_df['end_y'].iloc[i] = shot_df['shot_end_location'].iloc[i][1]
    for i in range(len(pass_df)):
        pass_df['start_x'].iloc[i] = pass_df['location'].iloc[i][0]
        pass_df['start_y'].iloc[i] = pass_df['location'].iloc[i][1]
        pass_df['end_x'].iloc[i] = pass_df['pass_end_location'].iloc[i][0]
        pass_df['end_y'].iloc[i] = pass_df['pass_end_location'].iloc[i][1]
    for i in range(len(carry_df)):
        carry_df['start_x'].iloc[i] = carry_df['location'].iloc[i][0]
        carry_df['start_y'].iloc[i] = carry_df['location'].iloc[i][1]
        carry_df['end_x'].iloc[i] = carry_df['carry_end_location'].iloc[i][0]
        carry_df['end_y'].iloc[i] = carry_df['carry_end_location'].iloc[i][1]
    
    concat = pd.concat([shot_df,pass_df,carry_df]).reset_index(drop = True)
        
    return concat

all_mcwfc_events = location_split_type(all_mcwfc_events)
all_cfc_events = location_split_type(all_cfc_events)
all_afc_events = location_split_type(all_afc_events)
all_bcfc_events = location_split_type(all_bcfc_events)

# Write events to excel
all_mcwfc_events.to_csv('MCWFC_events.csv')
all_cfc_events.to_csv('Chelsea_FCW_events.csv')
all_afc_events.to_csv('Arsenal_WFC_events.csv')
all_bcfc_events.to_csv('Birmingham_City_WFC_events.csv')

