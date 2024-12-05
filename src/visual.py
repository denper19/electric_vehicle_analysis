import pandas as pd
import matplotlib.pyplot as plt
from dataset_handler import DatasetHandler
from geopy.geocoders import Nominatim
import folium
from folium import Marker
from folium.plugins import MarkerCluster
import json

handler = DatasetHandler("Electric_Vehicle_Population_Data.csv")
handler.clean_dataset(printing=True)

years=sorted(handler._df['Model Year'].unique())
yearly=[]
for year in years:
    byyear=handler._df.loc[handler._df['Model Year'] == year].values
    yearly.append([x[10] for x in byyear])

boxplot_data = {
    'xlabel': 'Model Year',
    'ylabel': 'Electric Range',
    'title' : 'Electric Range by Model Year',
    'x': yearly,
    'y': years
}
PHEV=handler._df[handler._df['Electric Vehicle Type']=='PHEV']
boxplot_data_PHEV = {
    'xlabel': 'Make',
    'ylabel': 'Electric Range',
    'title' : 'Electric Range by Manufacturer for PHEV',
    'x': [PHEV[PHEV['Make'] == make]['Electric Range'] for make in PHEV['Make'].unique()],
    'y': PHEV['Make'].unique()
}
BEV=handler._df[handler._df['Electric Vehicle Type']=='BEV']
boxplot_data_BEV = {
    'xlabel': 'Make',
    'ylabel': 'Electric Range',
    'title' : 'Electric Range by Manufacturer for BEV',
    'x': [BEV[BEV['Make'] == make]['Electric Range'] for make in BEV['Make'].unique()],
    'y': BEV['Make'].unique()
}

# displays the makes and the number of cars in each section
maker_data = {
    'xlabel': 'Make',
    'ylabel': 'No. of Vehicles',
    'title' : 'Top 10 Different Makers',
    'x': handler._df['Make'].value_counts().head(10).index.to_list(),
    'y': handler._df['Make'].value_counts().head(10).to_list()
}

# displays the Model and the number of cars in each section
model_data = {
    'xlabel': 'Make',
    'ylabel': 'No. of Vehicles',
    'title' : 'Top 10 Different Models',
    'x': handler._df['Model'].value_counts().head(10).index.to_list(),
    'y': handler._df['Model'].value_counts().head(10).to_list()
}

car_type = {
    'title' : 'Vehicle type distribution',
    'y': handler._df['Electric Vehicle Type'].value_counts().index.to_list(),
    'x': handler._df['Electric Vehicle Type'].value_counts().to_list()
}

eligibility = {
    'title' : 'Clean Alternative Fuel Vehicle (CAFV) Eligibility',
    'y': handler._df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].value_counts().index.to_list(),
    'x': handler._df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].value_counts().to_list()
}

yeartotal_barplot = {
    'xlabel': 'Year',
    'ylabel': 'No. of Vehicles',
    'title' : 'Yearly Total',
    'x': handler._df['Model Year'].value_counts().index.to_list(),
    'y': handler._df['Model Year'].value_counts().to_list()
}

print("Years:",min(years),":",max(years))
print("Geographical:")
print("*",len(handler._df['State'].unique()),'states')
print("*",len(handler._df['County'].unique()),'counties')
print("*",len(handler._df['City'].unique()),'cities')
print("*",len(handler._df['Electric Utility'].unique()),'electric utilities')
print("\nMakes and Models:")
print("*",len(handler._df['Make'].unique()),'makes')
print("*",len(handler._df['Model'].unique()),'models')

handler._df.describe(exclude='number').T

handler._plot = True
handler.create_boxplot(data=boxplot_data, patch_artist=True)
handler.create_boxplot(data=boxplot_data_PHEV, patch_artist=True)
handler.create_boxplot(data=boxplot_data_BEV, patch_artist=True)
handler.create_barplot(maker_data)
handler.create_barplot(model_data)
handler.create_piechart(car_type, patch_artist=True)
handler.create_barplot({
    'xlabel': 'Vehicle type',
    'ylabel': 'count',
    'title' : 'Vehicle type distribution',
    'y': handler._df['Electric Vehicle Type'].value_counts().to_list(),
    'x': handler._df['Electric Vehicle Type'].value_counts().index.to_list()
}, patch_artist=True)
handler.create_piechart(eligibility, patch_artist=True)
handler.create_barplot({
    'xlabel': 'Eligible',
    'ylabel': 'Count',
    'title' : 'Clean Alternative Fuel Vehicle (CAFV) Eligibility',
    'y': handler._df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].value_counts().to_list(),
    'x': handler._df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].value_counts().index.to_list()
}, patch_artist=True)
handler.create_barplot(yeartotal_barplot)

with open("locations_data.json", "r") as file:
    loaded_data = json.load(file)

map_usa = folium.Map(location=[39.5, -99.7], tiles='cartodbpositron', zoom_start=4.4)

mc = MarkerCluster()
for loc in handler._df['Postal Code'].dropna():
    key = str(int(loc))
    lat, lon = loaded_data[key]['latitude'], loaded_data[key]['longitude']
    mc.add_child(Marker([lat, lon]))
map_usa.add_child(mc)

# map_usa # only works in notebooks

EV_map_usa = folium.Map(location=[39.5, -99.7], tiles='cartodbpositron', zoom_start=4.4)

for loc in handler._df[handler._df['Electric Vehicle Type']=='BEV']['Postal Code'].dropna().unique():
    key = str(int(loc))
    lat, lon = loaded_data[key]['latitude'], loaded_data[key]['longitude']
    folium.CircleMarker(location=[lat, lon], radius=5, fill=True, fill_color="red", fill_opacity=1, stroke=False).add_to(EV_map_usa)

for loc in handler._df[handler._df['Electric Vehicle Type']=='PHEV']['Postal Code'].dropna().unique():
    key = str(int(loc))
    lat, lon = loaded_data[key]['latitude'], loaded_data[key]['longitude']
    folium.CircleMarker(location=[lat, lon], radius=5, fill=True, fill_color="green", fill_opacity=1, stroke=False).add_to(EV_map_usa)

# EV_map_usa # only works in notebooks