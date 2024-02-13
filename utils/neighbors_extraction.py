import streamlit as st

import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import numpy as np
import ast

def return_neighbors(gdf,fuelTypeID):

    if fuelTypeID == "1":
        df_neighbors = pd.read_csv('data/fuels/Unleaded 95/neighbors_95.csv',dtype='str')
        df_neighbors = df_neighbors.loc[:,["KALCODE","neighbors"]]

        df_clustering = pd.read_csv('data/fuels/Unleaded 95/results_95_average.csv',dtype='str')
    elif fuelTypeID == "2":
        df_neighbors = pd.read_csv('data/fuels/Unleaded 98-100/neighbors_98_100.csv',dtype='str')
        df_neighbors = df_neighbors.loc[:,["KALCODE","neighbors"]]

        df_clustering = pd.read_csv('data/fuels/Unleaded 98-100/results_98_100_average.csv',dtype='str')
    elif fuelTypeID == "4":
        df_neighbors = pd.read_csv('data/fuels/Diesel/neighbors_diesel.csv',dtype='str')
        df_neighbors = df_neighbors.loc[:,["KALCODE","neighbors"]]

        df_clustering = pd.read_csv('data/fuels/Diesel/results_diesel_average.csv',dtype='str')

    df_neighbors_clustering = pd.merge(df_neighbors,df_clustering,on="KALCODE",how="left")

    final_gdf = pd.merge(gdf,df_neighbors_clustering,on="KALCODE",how="left")
    final_gdf = final_gdf.dropna(subset=['Result'])

    return(final_gdf)

def return_islands():

    df_islands = pd.read_excel('data/islands.xlsx',dtype='str')
    df_islands = df_islands.loc[:,["KALCODE","ISLAND","ISLAND_NAME","ISLAND_COMPLEX"]]

    return(df_islands)

def return_complex_results(fuelTypeID):

    if fuelTypeID == '1':
        results = pd.read_excel('data/fuels/Unleaded 95/complex_island_clustering.xlsx')
    elif fuelTypeID == '2':
        results = pd.read_excel('data/fuels/Unleaded 98-100/complex_island_clustering.xlsx')
    elif fuelTypeID == '4':
        results = pd.read_excel('data/fuels/Diesel/complex_island_clustering.xlsx')

    return(results)

def return_prefecture_clustering_results(fuelTypeID):

    codes_2021 = pd.read_excel('data/mit_2021.xlsx',dtype='str')

    if fuelTypeID == '1':
        clustering_df = pd.read_excel('data/fuels/Unleaded 95/prefecture_clustering.xlsx',dtype='str')
        average_prices_df = pd.read_excel('data/fuels/Unleaded 95/average_95_prices.xlsx',dtype='str')
    elif fuelTypeID == '2':
        clustering_df = pd.read_excel('data/fuels/Unleaded 98-100/prefecture_clustering.xlsx',dtype='str')
        average_prices_df = pd.read_excel('data/fuels/Unleaded 98-100/average_98_prices.xlsx',dtype='str')
    elif fuelTypeID == '4':
        clustering_df = pd.read_excel('data/fuels/Diesel/prefecture_clustering.xlsx',dtype='str')
        average_prices_df = pd.read_excel('data/fuels/Diesel/average_diesel_prices.xlsx',dtype='str')


    return(clustering_df,average_prices_df,codes_2021)

def return_neighbors_x_islands(gdf,fuelTypeID):

    df_islands = pd.read_excel('data/islands.xlsx',dtype='str')
    df_islands = df_islands.loc[:,["KALCODE","ISLAND","ISLAND_NAME","ISLAND_COMPLEX"]]

    if fuelTypeID == "1":
        df_neighbors = pd.read_csv('data/fuels/Unleaded 95/neighbors_95.csv',dtype='str')
        df_neighbors = df_neighbors.loc[:,["KALCODE","neighbors"]]

        df_clustering = pd.read_csv('data/fuels/Unleaded 95/results_95_average.csv',dtype='str')
    elif fuelTypeID == "2":
        df_neighbors = pd.read_csv('data/fuels/Unleaded 98-100/neighbors_98_100.csv',dtype='str')
        df_neighbors = df_neighbors.loc[:,["KALCODE","neighbors"]]

        df_clustering = pd.read_csv('data/fuels/Unleaded 98-100/results_98_100_average.csv',dtype='str')
    elif fuelTypeID == "4":
        df_neighbors = pd.read_csv('data/fuels/Diesel/neighbors_diesel.csv',dtype='str')
        df_neighbors = df_neighbors.loc[:,["KALCODE","neighbors"]]

        df_clustering = pd.read_csv('data/fuels/Diesel/results_diesel_average.csv',dtype='str')

    df_neighbors_clustering = pd.merge(df_neighbors,df_clustering,on="KALCODE",how="left")

    tmp_final_gdf = pd.merge(gdf,df_neighbors_clustering,on="KALCODE",how="left")
    final_gdf = pd.merge(tmp_final_gdf,df_islands,on="KALCODE",how="left")
    final_gdf = final_gdf.dropna(subset=['Result','ISLAND'])



    return(final_gdf)
    
def clustering(dd_code,gdf,final_gdf,df_dummy_neighbors):

    neighbors_df = final_gdf[final_gdf["KALCODE"] == dd_code]  
    neighbors = neighbors_df["neighbors"].values
    neighbors = [ast.literal_eval(x) for x in neighbors]

    #print(neighbors)

    if len(neighbors) == 0:
        st.write("No Information about the selected community")
    else:

        temp_df = final_gdf[final_gdf["KALCODE"].isin(neighbors[0])]

        dummy_neighbors_df = df_dummy_neighbors[df_dummy_neighbors["KALCODE"] == dd_code]
        dummy_neighbors = dummy_neighbors_df["neighbors"].values
        dummy_neighbors = [ast.literal_eval(x) for x in dummy_neighbors]
        dummy_neighbors = [item for item in dummy_neighbors[0] if item not in neighbors[0]]

        dummy_df = gdf[gdf["KALCODE"].isin(dummy_neighbors)]

        clusters = neighbors_df["Result"].values
        clusters = [str(x) for x in ast.literal_eval(clusters[0])]

        return(temp_df,dummy_df,clusters,neighbors)
