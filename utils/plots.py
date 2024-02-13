import streamlit as st

import ast
import pandas as pd
from io import BytesIO
import geopandas as gpd
import matplotlib.pyplot as plt


def print_main_map(gdf,df):

    #width = st.sidebar.slider("Main Map Width", 1, 25, 20)
    #height = st.sidebar.slider("Main Map Height", 1, 25, 15)

    num_of_uniq_municipalities = len(df["KALCODE"].unique())
    num_of_all_municipalities = len(gdf["KALCODE"].unique())

    st.write("Number of All Communities:",num_of_all_municipalities)
    st.write("Number of Unique Communities:",num_of_uniq_municipalities)

    fig, ax = plt.subplots(figsize=(20, 15))
    ax.set_facecolor('#add8e6')  # Hex code for light blue color
    gdf['geometry'].plot(ax=ax, color='gray', edgecolor='gray')
    df['geometry'].plot(ax=ax, color='red', edgecolor='black')
    ax.set_title('Map of Communities in Greece')

    st.pyplot(fig)

def print_target_dd_with_neighbors(true_neighbors_df,dummy_neighbors_df,clusters,neighbors,selected_municipality):

    dd_name_fond_size = st.sidebar.slider("Community Name Size", 1, 25, 15)
    dd_name_rotation = st.sidebar.slider("Community Name Rotation", -95, 95, 8)

    fig, ax = plt.subplots(figsize=(24, 24))
    plt.title("Clustering")     # Plot title
    ax.set_facecolor('#add8e6') # Fill background with lightblue color

    dummy_neighbors_df['geometry'].plot(ax=ax, color='grey', edgecolor='black')  # Plot dummy neighbors

    ############################################
    ###           Applying Colors            ###
    ###    Depending of Average of Clusters  ###
    ############################################
    cluster_0 = cluster_1 = cluster_2 = 0
    flag_0 = flag_1 = flag_2 = 0
    for indexer, cluster in enumerate(clusters):
        target_polygon_index = true_neighbors_df[true_neighbors_df['KALCODE'] == neighbors[0][indexer]].index

        if cluster == "0":
            cluster_0+= float(true_neighbors_df.loc[target_polygon_index, 'Average_Fuel_Price'].values)
            flag_0+=1
        elif cluster == "1":
            cluster_1+= float(true_neighbors_df.loc[target_polygon_index, 'Average_Fuel_Price'].values)
            flag_1+=1
        elif cluster == "2":
            cluster_2+= float(true_neighbors_df.loc[target_polygon_index, 'Average_Fuel_Price'].values)
            flag_2+=1
    
    if flag_0 == 0:
        flag_0 = 0.5
    if flag_1 == 0:
        flag_1 = 0.5
    if flag_2 == 0:
        flag_2 = 0.5

    average_per_cluster = {
        "0":cluster_0/flag_0,
        "1":cluster_1/flag_1,
        "2":cluster_2/flag_2
    }

    communities_per_cluster = {
        "0":flag_0,
        "1":flag_1,
        "2":flag_2
    }

    cluster_to_color = dict(sorted(average_per_cluster.items(), key=lambda item: item[1], reverse=False))

    new_values = ['#fee0d2','#fc9272','#de2d26']
    
    for key, new_value in zip(cluster_to_color, new_values):
        cluster_to_color[key] = new_value


    ############################################
    ###           Applying Colors            ###
    ###    Depending of Average of Clusters  ###
    ############################################

    for indexer, cluster in enumerate(clusters):
        target_polygon_index = true_neighbors_df[true_neighbors_df['KALCODE'] == neighbors[0][indexer]].index

        true_neighbors_df.loc[target_polygon_index, 'geometry'].plot(ax=ax, color=cluster_to_color[cluster], edgecolor="black", label="Cluster 1")
        
    for indexer, cluster in enumerate(clusters):
        target_polygon_index = true_neighbors_df[true_neighbors_df['KALCODE'] == neighbors[0][indexer]].index

        code = true_neighbors_df.loc[target_polygon_index, 'KALCODE'].values
        if code == selected_municipality:
            edge_color = "yellow"
            line_width = 4

            true_neighbors_df.loc[target_polygon_index, 'geometry'].plot(ax=ax, color=cluster_to_color[cluster], linewidth=line_width, edgecolor=edge_color, label="Cluster 1")
            
    for idx, row in true_neighbors_df.iterrows():   # Plot true neighbors names
        plt.annotate(row['LEKTIKO'], (row['geometry'].centroid.x, row['geometry'].centroid.y),
                     ha='center', fontsize=dd_name_fond_size, color='black', rotation=dd_name_rotation)
        
    for idx, row in true_neighbors_df.iterrows():   # Plot a dot at the center of each true community
        plt.annotate(".", (row['geometry'].centroid.x, row['geometry'].centroid.y - 300),
                     ha='center', fontsize=20, color='black', rotation=0)
        
    for idx, row in dummy_neighbors_df.iterrows():   # Plot a dot at the center of each dummy community
        plt.annotate(".", (row['geometry'].centroid.x, row['geometry'].centroid.y - 300),
                     ha='center', fontsize=20, color='black', rotation=0)
        
    for idx, row in true_neighbors_df.iterrows():   # Plot true neighbors average fuel prices

        price_as_float = float(row['Average_Fuel_Price'])
        rounded_average_price = round(price_as_float, 3)
        final_average_price = str(rounded_average_price) + "€"

        plt.annotate(final_average_price, (row['geometry'].centroid.x, row['geometry'].centroid.y - 150),
                     ha='center', fontsize=dd_name_fond_size, color='black', rotation=dd_name_rotation)
        
    for idx, row in dummy_neighbors_df.iterrows():  # Plot dummy neighbors names
        plt.annotate(row['LEKTIKO'], (row['geometry'].centroid.x, row['geometry'].centroid.y),
                     ha='center', fontsize=dd_name_fond_size, color='black', rotation=dd_name_rotation)
        
    
    y_coord = st.sidebar.slider("Labeling Y-Coordinate", -0.5, 0.5, 0.1)
    
    flag = 0
    for key, value in cluster_to_color.items():
        flag+=1

        rounded_average_price = round(average_per_cluster[key], 3)

        if rounded_average_price <=0:
            continue

        plt.annotate("Cluster " + str(flag) + ":", xy=(0.1, y_coord), xycoords='axes fraction', 
                     ha='center', fontsize=30, color=value)
        
        plt.annotate("Average Price: " + str(rounded_average_price), xy=(0.36, y_coord), xycoords='axes fraction', 
                     ha='center', fontsize=30, color=value)
        
        plt.annotate("Number of Communities: " + str(communities_per_cluster[key]), xy=(0.77, y_coord), xycoords='axes fraction', 
                     ha='center', fontsize=30, color=value)
        
        y_coord -= 0.05

    buf = BytesIO()
    fig.savefig(buf, format="png")
    #image_width = st.number_input("Image Width", 1, 2000, 700)
    #use_column_width = st.checkbox("Use Column Width")
    st.image(buf)


def plot_prefectures_clustering(clustering_df,average_prices_df,gdf,selected_prefecture,codes_2021):

    codes_2021 = codes_2021.rename(columns={"Γ.Κ. 2021":"KALCODE"})
    whole_prefecture = codes_2021[codes_2021["ΝΟΜΟΣ"] == selected_prefecture]
    whole_prefecture = pd.merge(gdf,whole_prefecture,on="KALCODE",how="left")
    whole_prefecture = whole_prefecture[whole_prefecture["ΝΟΜΟΣ"] == selected_prefecture]

    unique_prefecture_df = clustering_df[clustering_df["ΝΟΜΟΣ"] == selected_prefecture]

    individual_communities = unique_prefecture_df["Names"].values[0]
    communities = ast.literal_eval(individual_communities)

    individual_clusters = unique_prefecture_df["RESULT"].values[0]
    string_list = individual_clusters[1:-1].split()
    clusters = [int(num) for num in string_list]

    prefecture_capital = whole_prefecture[whole_prefecture["ΠΡΩΤΕΥΟΥΣΑ"] == "1"]
    prefecture_capital = prefecture_capital["KALCODE"].values[0]
    print(prefecture_capital)
    
    ############################################
    ###           Applying Colors            ###
    ###    Depending of Average of Clusters  ###
    ############################################
    cluster_0 = cluster_1 = cluster_2 = cluster_3 = cluster_4 = 0
    flag_0 = flag_1 = flag_2 = flag_3 = flag_4 = 0

    for index,community in enumerate(communities):
        temp_gdf = gdf[gdf["KALCODE"] == community]
        average_fuel_price = average_prices_df[average_prices_df["KALCODE"] == community]["AVERAGE_PRICE"].values[0]

        if clusters[index] == 0:
            cluster_0+= float(average_fuel_price)
            flag_0+=1
        elif clusters[index] == 1:
            cluster_1+= float(average_fuel_price)
            flag_1+=1
        elif clusters[index] == 2:
            cluster_2+= float(average_fuel_price)
            flag_2+=1
        elif clusters[index] == 3:
            cluster_3+= float(average_fuel_price)
            flag_3+=1
        elif clusters[index] == 4:
            cluster_4+= float(average_fuel_price)
            flag_4+=1

    average_per_cluster = {
        0:cluster_0/flag_0,
        1:cluster_1/flag_1,
        2:cluster_2/flag_2,
        3:cluster_3/flag_3,
        4:cluster_4/flag_4,
    }

    communities_per_cluster = {
        0:flag_0,
        1:flag_1,
        2:flag_2,
        3:flag_3,
        4:flag_4,
    }

    cluster_to_color = dict(sorted(average_per_cluster.items(), key=lambda item: item[1], reverse=False))

    new_values = ['#fee5d9','#fcae91','#fb6a4a','#de2d26','#a50f15']
    
    for key, new_value in zip(cluster_to_color, new_values):
        cluster_to_color[key] = new_value

    ############################################
    ###           Applying Colors            ###
    ###    Depending of Average of Clusters  ###
    ############################################

    fig, ax = plt.subplots(figsize=(24, 24))
    plt.title("Clustering for " + '"' + selected_prefecture + '"', fontsize = 28)     # Plot title
    ax.set_facecolor('#add8e6') # Fill background with lightblue color

    whole_prefecture["geometry"].plot(ax=ax, color="grey", edgecolor="grey")

    for index,community in enumerate(communities):

        if community == prefecture_capital:
            edge_color = "yellow"
            line_width = 5
        else:
            edge_color = "black"
            line_width = 0.5

        temp_gdf = gdf[gdf["KALCODE"] == community]
        temp_gdf["geometry"].plot(ax=ax, color=cluster_to_color[clusters[index]], linewidth=line_width, edgecolor=edge_color)
       
    
    for index,community in enumerate(communities):
        temp_gdf = gdf[gdf["KALCODE"] == community]

        if temp_gdf.empty:
            continue

        average_fuel_price = average_prices_df[average_prices_df["KALCODE"] == community]["AVERAGE_PRICE"].values[0]

        rounded_average_price = round(float(average_fuel_price), 3)
        final_average_price = str(rounded_average_price) + "€"

        plt.annotate(final_average_price, (temp_gdf["geometry"].centroid.x, temp_gdf["geometry"].centroid.y),
                    ha='center', fontsize=12, color='black', rotation=10)
        
    y_coord = st.sidebar.slider("Labeling Y-Coordinate", -0.5, 0.5, 0.1)

    flag = 0
    for key, value in cluster_to_color.items():
        flag+=1
        #plt.annotate("Cluster" + str(key), (50000, 50000), ha='center', fontsize=12, color=cluster_to_color[key], rotation=0)
        plt.annotate("Cluster " + str(flag) + ":", xy=(0.1, y_coord), xycoords='axes fraction', 
                     ha='center', fontsize=30, color=value)
        
        rounded_average_price = round(average_per_cluster[key], 3)

        plt.annotate("Average Price: " + str(rounded_average_price), xy=(0.30, y_coord), xycoords='axes fraction', 
                     ha='center', fontsize=30, color=value)
        
        plt.annotate("Number of Communities: " + str(communities_per_cluster[key]), xy=(0.62, y_coord), xycoords='axes fraction', 
                     ha='center', fontsize=30, color=value)
        
        y_coord -= 0.05

 
    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)

def print_per_complex_islands(gdf,islands_df,results,selected_complex):

    unique_complex_df = results[results["ISLAND_COMPLEX"] == selected_complex]

    unique_islands = unique_complex_df["NAMES"].values[0]
    unique_average_values = unique_complex_df["PRICES"].values[0]
    unique_clusters = unique_complex_df["RESULT"].values[0]

    unique_islands = unique_islands[1:-1].split()
    unique_islands = [string.strip("'") for string in unique_islands]

    unique_average_values = unique_average_values[1:-1].split()
    unique_clusters = unique_clusters[1:-1].split()

    complex_to_color = {
        "0":'blue',
        "1":'green',
        "2":'yellow',
        "3":'red'
    }

    ############################################
    ###           Applying Colours           ###
    ###    Depending of Average of Clusters  ###
    ############################################
    cluster_0 = cluster_1 = cluster_2 = cluster_3 = 0
    flag_0 = flag_1 = flag_2 = flag_3 = 0

    for index,island_name in enumerate(unique_islands):
        #temp_island_df = islands_df[islands_df["ISLAND_NAME"] == island_name]

        price_as_float = float(unique_average_values[index])

        if unique_clusters[index] == "0":
            cluster_0+= float(price_as_float)
            flag_0+=1
        elif unique_clusters[index] == "1":
            cluster_1+= float(price_as_float)
            flag_1+=1
        elif unique_clusters[index] == "2":
            cluster_2+= float(price_as_float)
            flag_2+=1
        elif unique_clusters[index] == "3":
            cluster_3+= float(price_as_float)
            flag_3+=1

    print(flag_0,flag_1,flag_2,flag_3)
    print(cluster_0,cluster_1,cluster_2,cluster_3)

    average_per_cluster = {
        "0":cluster_0/flag_0,
        "1":cluster_1/flag_1,
        "2":cluster_2/flag_2,
        "3":cluster_3/flag_3
    }

    communities_per_cluster = {
        "0":flag_0,
        "1":flag_1,
        "2":flag_2,
        "3":flag_3
    }

    complex_to_color = dict(sorted(average_per_cluster.items(), key=lambda item: item[1], reverse=False))

    new_values = ['#fee5d9','#fcae91','#fb6a4a','#cb181d']
    
    for key, new_value in zip(complex_to_color, new_values):
        complex_to_color[key] = new_value

    ############################################
    ###           Applying Colours           ###
    ###    Depending of Average of Clusters  ###
    ############################################

    fig, ax = plt.subplots(figsize=(20, 20))
    ax.set_facecolor('#add8e6')  # Hex code for light blue color

    name_font_size = st.sidebar.slider("Island Name Size", 5, 35, 14)
    
    for index,island_name in enumerate(unique_islands):
        temp_island_df = islands_df[islands_df["ISLAND_NAME"] == island_name]

        temp_gdf_island = pd.merge(gdf,temp_island_df,on="KALCODE",how="left")

        temp_gdf_island = temp_gdf_island[temp_gdf_island["ISLAND_NAME"] == island_name]

        multi_polygon = temp_gdf_island['geometry'].unary_union
        multi_polygon_gdf = gpd.GeoDataFrame(geometry=[multi_polygon])

        multi_polygon_gdf["geometry"].plot(ax=ax, color=complex_to_color[unique_clusters[index]], edgecolor=complex_to_color[unique_clusters[index]])

        plt.annotate(island_name, (multi_polygon_gdf['geometry'].centroid.x, multi_polygon_gdf['geometry'].centroid.y),
                     ha='center', fontsize=name_font_size, color='black', rotation=0)
        
        price_as_float = float(unique_average_values[index])
        rounded_average_price = round(price_as_float, 3)
        final_average_price = str(rounded_average_price) + "€"
        
        plt.annotate(final_average_price, (multi_polygon_gdf['geometry'].centroid.x, multi_polygon_gdf['geometry'].centroid.y - 5000),
                     ha='center', fontsize=name_font_size, color='black', rotation=0)

    y_coord = st.sidebar.slider("Labeling Y-Coordinate", -0.5, 0.5, 0.1)

    flag = 0
    for key, value in complex_to_color.items():
        flag+=1
        #plt.annotate("Cluster" + str(key), (50000, 50000), ha='center', fontsize=12, color=cluster_to_color[key], rotation=0)
        plt.annotate("Cluster " + str(flag) + ":", xy=(0.1, y_coord), xycoords='axes fraction', 
                     ha='center', fontsize=30, color=value)
        
        rounded_average_price = round(average_per_cluster[key], 3)

        plt.annotate("Average Price: " + str(rounded_average_price), xy=(0.31, y_coord), xycoords='axes fraction', 
                     ha='center', fontsize=30, color=value)
        
        plt.annotate("Number of Communities: " + str(communities_per_cluster[key]), xy=(0.66, y_coord), xycoords='axes fraction', 
                     ha='center', fontsize=30, color=value)
         
        y_coord -= 0.05

        
    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)


def print_complex_of_islands(gdf,island_gdf,fuelTypeID):

    gdf = gdf.loc[:,["KALCODE","geometry"]]

    final_df = pd.merge(gdf,island_gdf,on="KALCODE",how='left')
    final_df = final_df.dropna()

    unique_complex_islands = final_df["ISLAND_COMPLEX"].unique()

    if fuelTypeID == "1":

        complex_to_color = {
            "ΕΥΒΟΙΑ":'blue',
            "ΚΡΗΤΗ":'green',
            "ΣΠΟΡΑΔΕΣ":'#fc9272',
            "ΑΝΑΤΟΛΙΚΟ ΑΙΓΑΙΟ":'#fee0d2',
            "ΔΩΔΕΚΑΝΗΣΑ":'#fee0d2',
            "ΚΥΚΛΑΔΕΣ":'#fee0d2',
            "ΑΡΓΟΣΑΡΩΝΙΚΟΣ":'#fee0d2',
            "ΕΠΤΑΝΗΣΑ":'#de2d26'
        }

        complex_to_price = {
            "ΕΥΒΟΙΑ":'1.6205819041341607',
            "ΚΡΗΤΗ":'1.7076318098872656',
            "ΣΠΟΡΑΔΕΣ":'1.8508587309858913',
            "ΑΝΑΤΟΛΙΚΟ ΑΙΓΑΙΟ":'1.698040504897597',
            "ΔΩΔΕΚΑΝΗΣΑ":'1.7449215875629953',
            "ΚΥΚΛΑΔΕΣ":'1.826177367873738',
            "ΑΡΓΟΣΑΡΩΝΙΚΟΣ":'1.6367695413353376',
            "ΕΠΤΑΝΗΣΑ":'2.1012666945333374'
        }
    elif fuelTypeID == "2":
        complex_to_color = {
            "ΕΥΒΟΙΑ":'blue',
            "ΚΡΗΤΗ":'green',
            "ΣΠΟΡΑΔΕΣ":'#fc9272',
            "ΑΝΑΤΟΛΙΚΟ ΑΙΓΑΙΟ":'#fc9272',
            "ΔΩΔΕΚΑΝΗΣΑ":'#de2d26',
            "ΚΥΚΛΑΔΕΣ":'#de2d26',
            "ΑΡΓΟΣΑΡΩΝΙΚΟΣ":'#fc9272',
            "ΕΠΤΑΝΗΣΑ":'#fc9272'
        }

        complex_to_price = {
            "ΕΥΒΟΙΑ":'1.7965187853746551',
            "ΚΡΗΤΗ":'1.8361161855278938',
            "ΣΠΟΡΑΔΕΣ":'1.996305520309713',
            "ΑΝΑΤΟΛΙΚΟ ΑΙΓΑΙΟ":'1.8794562997061008',
            "ΔΩΔΕΚΑΝΗΣΑ":'1.9272714570203562',
            "ΚΥΚΛΑΔΕΣ":'2.0009932883619745',
            "ΑΡΓΟΣΑΡΩΝΙΚΟΣ":'1.8402990428877009',
            "ΕΠΤΑΝΗΣΑ":'1.8212965981846818'
        }
    else:
        complex_to_color = {
            "ΕΥΒΟΙΑ":'blue',
            "ΚΡΗΤΗ":'green',
            "ΣΠΟΡΑΔΕΣ":'#fc9272',
            "ΑΝΑΤΟΛΙΚΟ ΑΙΓΑΙΟ":'#fc9272',
            "ΔΩΔΕΚΑΝΗΣΑ":'#fee0d2',
            "ΚΥΚΛΑΔΕΣ":'#de2d26',
            "ΑΡΓΟΣΑΡΩΝΙΚΟΣ":'#fee0d2',
            "ΕΠΤΑΝΗΣΑ":'#fee0d2'
        }

        complex_to_price = {
            "ΕΥΒΟΙΑ":'1.36624347376721',
            "ΚΡΗΤΗ":'1.424577231131483',
            "ΣΠΟΡΑΔΕΣ":'1.5603947603826216',
            "ΑΝΑΤΟΛΙΚΟ ΑΙΓΑΙΟ":'1.429371664933791',
            "ΔΩΔΕΚΑΝΗΣΑ":'1.4496203790706264',
            "ΚΥΚΛΑΔΕΣ":'1.5416102770607822',
            "ΑΡΓΟΣΑΡΩΝΙΚΟΣ":'1.3711693874169868',
            "ΕΠΤΑΝΗΣΑ":'1.399004703972634'
        }
    


    #width = st.sidebar.slider("Neighbors Map Width", 0.1, 20., 12.)
    #height = st.sidebar.slider("Neighbors Map Height", 0.1, 20., 13.)

    fig, ax = plt.subplots(figsize=(20, 20))
    ax.set_facecolor('#add8e6')  # Hex code for light blue color
    
    gdf["geometry"].plot(ax=ax, color="grey", linewidth=2, edgecolor='grey')

    for complex_name in unique_complex_islands:
            if complex_name == "ΕΥΒΟΙΑ" or complex_name == "ΚΡΗΤΗ":
                continue
            complex_df = final_df[final_df["ISLAND_COMPLEX"] == complex_name]
            multi_polygon = complex_df['geometry'].unary_union
            multi_polygon_gdf = gpd.GeoDataFrame(geometry=[multi_polygon])
            multi_polygon_gdf['ISLAND_COMPLEX'] = complex_name

            multi_polygon_gdf["geometry"].plot(ax=ax, color=complex_to_color[complex_name], linewidth=2, edgecolor=complex_to_color[complex_name])

            plt.annotate(multi_polygon_gdf["ISLAND_COMPLEX"].values[0], (multi_polygon_gdf['geometry'].centroid.x, multi_polygon_gdf['geometry'].centroid.y),
                     ha='center', fontsize=25, color='black', rotation=15)
            
            price_as_float = float(complex_to_price[complex_name])
            rounded_average_price = round(price_as_float, 3)
            final_average_price = str(rounded_average_price) + "€" 

            plt.annotate(final_average_price, (multi_polygon_gdf['geometry'].centroid.x, multi_polygon_gdf['geometry'].centroid.y - 14000),
                     ha='center', fontsize=17, color='black', rotation=15)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)





        
    

