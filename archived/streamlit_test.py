import geopandas as gpd
import streamlit as st
import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1 import make_axes_locatable


# Load the GeoDataFrame containing municipality borders
# Replace 'your_shapefile.shp' with the path to your shapefile

shapefile_path = 'C:/Users/mimar/Desktop/master/ΕΛΣΤΑΤ/dd/TOP_DHM_KOIN.shp'

gdf = gpd.read_file(shapefile_path)

# Create a Streamlit sidebar to select a municipality
selected_municipality = st.sidebar.selectbox('Select Municipality', gdf['KALCODE'])

# Filter the GeoDataFrame to display only the selected municipality
selected_gdf = gdf[gdf['KALCODE'] == selected_municipality]

# Plot the selected municipality borders using Matplotlib
fig, ax = plt.subplots(figsize=(30, 20))

ax.set_facecolor('#add8e6')  # Hex code for light blue color

gdf['geometry'].plot(ax=ax, color='lightgrey', edgecolor='black')
selected_gdf['geometry'].plot(ax=ax, color='blue', edgecolor='red')

# Set plot properties
ax.set_title(f'Municipality Borders - {selected_municipality}')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Display the plot using Streamlit
st.pyplot(fig)

# Display additional information in a popup when a municipality is selected
if st.button('Show Information'):
    # Retrieve and display information about the selected municipality
    selected_info = gdf[gdf['KALCODE'] == selected_municipality].to_dict(orient='records')[0]
    st.write(f"**Municipality Information:**")
    st.write(selected_info)