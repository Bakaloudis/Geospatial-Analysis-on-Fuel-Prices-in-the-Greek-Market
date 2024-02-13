import streamlit as st

import sys
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

from utils.neighbors_extraction import return_neighbors,return_neighbors_x_islands,clustering,return_islands,return_complex_results,return_prefecture_clustering_results
from utils.plots import print_main_map,print_target_dd_with_neighbors,print_complex_of_islands,print_complex_of_islands,print_per_complex_islands,plot_prefectures_clustering

st.set_page_config(
    page_title="Master Thesis", 
    page_icon=":rocket:",
    layout="wide")


shapefile_path = 'data/shapefiles/communities/TOP_DHM_KOIN.shp'
gdf = gpd.read_file(shapefile_path)

all_neighbors_df = pd.read_csv('data/all_neighbors_per_municipality.csv',dtype='str')  # Dataframe with all available neighbors per municipality

fuelType_to_number = {
    "Unleaded 95" : "1",
    "Unleaded 98/100" : "2",
    "Diesel" : "4"
}

def show_option_1():

    st.header("Clustering")

    selected_option = st.sidebar.radio("Select a Category", ["Individual Communities", "Prefectures", "Islands"])

    selected_fueltypeID = st.sidebar.selectbox("Select a Fuel Type", ["Unleaded 95", "Unleaded 98/100", "Diesel"])
    fuelTypeID = fuelType_to_number[selected_fueltypeID]

    active_neighbors_df = return_neighbors(gdf,fuelTypeID) # Dataframe with all active neighbors per municipality for the selected fuelTypeID

    if selected_option == "Individual Communities":

        print_main_map(gdf,active_neighbors_df)

        if selected_fueltypeID:

            selected_municipality = st.sidebar.selectbox('Select a Community', active_neighbors_df['LEKTIKO'])

            st.write("Selected Fuel Type: ", selected_fueltypeID)
            st.write("Selected Community: ", selected_municipality)

            selected_municipality_df = active_neighbors_df[active_neighbors_df["LEKTIKO"] == selected_municipality]
            dd_code = selected_municipality_df["KALCODE"].values[0]

            temp_df,dummy_df,clusters,neighbors = clustering(dd_code,gdf,active_neighbors_df,all_neighbors_df)

            print_target_dd_with_neighbors(temp_df,dummy_df,clusters,neighbors,dd_code)

            # selected_info = active_neighbors_df[active_neighbors_df['KALCODE'] == dd_code].to_dict(orient='records')[0]
            # st.write(f"**Municipality Information:**")
            # st.write(selected_info)

    elif selected_option == "Prefectures":

        clustering_df, average_prices_df, codes_2021 = return_prefecture_clustering_results(fuelTypeID)

        selected_prefecture = st.sidebar.selectbox('Select a Prefecture', clustering_df['ΝΟΜΟΣ'])

        plot_prefectures_clustering(clustering_df,average_prices_df,gdf,selected_prefecture,codes_2021)
    
    elif selected_option == "Islands":

        selected_option = st.sidebar.radio("Select a Sub-Category", ["Individual Islands", "Per Complex", "All Complexes"])

        if selected_option == "Individual Islands":

            islands_df = return_neighbors_x_islands(gdf,fuelTypeID)

            unique_islands = islands_df["ISLAND_NAME"].unique()

            selected_island = st.sidebar.selectbox('Select a Community', unique_islands)
            selected_island_df = islands_df[islands_df["ISLAND_NAME"] == selected_island]

            selected_island_municipality = st.sidebar.selectbox('Select a Community', selected_island_df['LEKTIKO'])
            selected_island_municipality_df = islands_df[islands_df["LEKTIKO"] == selected_island_municipality]
        
            dd_code = selected_island_municipality_df["KALCODE"].values[0]

            temp_df,dummy_df,clusters,neighbors = clustering(dd_code,gdf,active_neighbors_df,all_neighbors_df)

            print_target_dd_with_neighbors(temp_df,dummy_df,clusters,neighbors,dd_code)

        elif selected_option == "Per Complex":

            islands_df = return_islands()                   # All islands info
            results = return_complex_results(fuelTypeID)    # Clustering info per complex island

            selected_complex = st.sidebar.selectbox('Select an Island Complex', results['ISLAND_COMPLEX'])

            print_per_complex_islands(gdf,islands_df,results,selected_complex)

        elif selected_option == "All Complexes":

            island_gdf = return_islands()

            print_complex_of_islands(gdf,island_gdf,fuelTypeID)

def show_option_2():
    st.header("Option 3")
    st.write("This is the content for Option 3.")

def main():

    st.title("Geospatial Analysis on Fuel Prices in the Greek Market")

    # Add buttons on the left side
    selected_option = st.sidebar.radio("Select a Page", ["Clustering", "Conclusions"])

    # Display content based on the selected option
    if selected_option == "Clustering":
        show_option_1()
    elif selected_option == "Conclusions":
        show_option_2()

if __name__ == "__main__":
    main()