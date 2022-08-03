# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 22:17:25 2022

@author: Ed.Morris
"""

# Import modules
import pandas as pd
from mplsoccer import VerticalPitch, add_image
import matplotlib.pyplot as plt
from PIL import Image
import os

# Set wd path
wd_path = r"C:\Users\ed.morris\Documents\Python Scripts\WSL"
os.chdir(wd_path)

# Import data
def load_data():
    mcwfc_shots = pd.read_csv('MCWFC_shots.csv')
    cfc_shots = pd.read_csv('Chelsea_FCW_shots.csv')
    afc_shots = pd.read_csv('Arsenal_WFC_shots.csv')
    mcwfc_events = pd.read_csv('MCWFC_events.csv')
    cfc_events = pd.read_csv('Chelsea_FCW_events.csv')
    afc_events = pd.read_csv('Arsenal_WFC_events.csv')
    bcfc_shots = pd.read_csv('Birmingham_City_WFC_shots.csv')
    bcfc_events = pd.read_csv('Birmingham_City_WFC_events.csv')
    
    return mcwfc_events, mcwfc_shots, cfc_events, cfc_shots, afc_events, afc_shots, bcfc_events, bcfc_shots

mcwfc_events, mcwfc_shots, cfc_events, cfc_shots, afc_events, afc_shots, bcfc_events, bcfc_shots = load_data()

# Filter for Ellen White
    # Season 1
season1_EW = bcfc_events.loc[bcfc_events.player == 'Ellen White'].reset_index(drop=True)
season2_EW = mcwfc_events.loc[(mcwfc_events.season == 2) & (mcwfc_events.player == 'Ellen White')].reset_index(drop=True)
season3_EW = mcwfc_events.loc[(mcwfc_events.season == 3) & (mcwfc_events.player == 'Ellen White')].reset_index(drop=True)

# Pull Ellen White BCFC event data for 2018/19 heatmap comparison
pitch = VerticalPitch(line_color='#000009', line_zorder=2)

def EW_heatmaps():
    fig, axs = pitch.grid(ncols=3, axis=False, endnote_height=0.05)
    
    bcfc_plot = pitch.kdeplot(season1_EW.start_x, season1_EW.start_y, ax=axs['pitch'][0],
                               shade=True, levels=100, shade_lowest=True,
                               cut=4, cmap='Blues')
    bcfc_logo = add_image(Image.open('BCFC_logo.png'), 
                          fig, 
                          left = 0.04,
                          bottom = axs['title'].get_position().y0,
                          height = axs['title'].get_position().height)
    axs['title'].text(0.09,0.5,'Season: 2018/19', fontsize = 20)
    axs['title'].text(0.09,0.3,'Minutes played: 647', fontsize = 15)
    
    mcfc1_plot = pitch.kdeplot(season2_EW.start_x, season2_EW.start_y, ax=axs['pitch'][1],
                              shade=True, levels=100, shade_lowest=True,
                              cut=4, cmap='Blues')
    city_logo1 = add_image(Image.open('MCFC_logo.png'), 
                          fig, 
                          left = 0.36,
                          bottom = axs['title'].get_position().y0,
                          height = axs['title'].get_position().height)
    axs['title'].text(0.465,0.5,'Season: 2019/20', fontsize = 20)
    axs['title'].text(0.465,0.3,'Minutes played: 857', fontsize = 15)
    
    mcf2_plot = pitch.kdeplot(season3_EW.start_x, season3_EW.start_y, ax=axs['pitch'][2],
                              shade=True, levels=100, shade_lowest=True,
                              cut=4, cmap='Blues')
    city_logo2 = add_image(Image.open('MCFC_logo.png'), 
                          fig, 
                          left = 0.68,
                          bottom = axs['title'].get_position().y0,
                          height = axs['title'].get_position().height)
    axs['title'].text(0.81,0.5,'Season: 2020/21', fontsize = 20)
    axs['title'].text(0.81,0.3,'Minutes played: 1,534', fontsize = 15)
    
    axs['endnote'].text(0.14,0.5,'Ellen White Heatmaps: WSL 2018/19 - 2020/21', fontsize=30)
        
    plt.show()
    
EW_heatmaps()