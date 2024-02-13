import geopandas as gpd
import streamlit as st
import pydeck as pdk

# Load the GeoDataFrame containing municipality borders
# Replace 'your_shapefile.shp' with the path to your shapefile

shapefile_path = 'C:/Users/mimar/Desktop/master/ΕΛΣΤΑΤ/dd/TOP_DHM_KOIN.shp'

gdf = gpd.read_file(shapefile_path)

# Create a Streamlit sidebar to select a municipality
selected_municipality = st.sidebar.selectbox('Select Municipality', gdf['KALCODE'])

# Filter the GeoDataFrame to display only the selected municipality
selected_gdf = gdf[gdf['KALCODE'] == selected_municipality]

# Plot the selected municipality borders using pydeck
layer = pdk.Layer(
    "PolygonLayer",
    data=selected_gdf['geometry'],
    get_polygon="-",
    get_fill_color=[0, 0, 255, 100],  # Blue color with some transparency
    get_line_color=[255, 0, 0],  # Red border color
)

view_state = pdk.ViewState(
    latitude=gdf.geometry.centroid.y.mean(),
    longitude=gdf.geometry.centroid.x.mean(),
    zoom=8,
)

tooltip = {"html": f"<b>{selected_municipality}</b>", "style": {"color": "white"}}

# Create the pydeck chart
chart = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip,
)

# Display the chart using Streamlit
st.pydeck_chart(chart)

# Display additional information in a popup when a municipality is selected
if st.button('Show Information'):
    # Retrieve and display information about the selected municipality
    selected_info = gdf[gdf['KALCODE'] == selected_municipality].to_dict(orient='records')[0]
    st.write(f"**Municipality Information:**")
    st.write(selected_info)