from dataset_handler import DatasetHandler
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
import folium
from folium import Marker
from folium.plugins import MarkerCluster
import json

handler = DatasetHandler("proj/electric_vehicle_analysis/Electric_Vehicle_Population_Data.csv")
handler.clean_dataset()
handler._plot = False

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
    'title' : 'EElectric Range by Manufacturer for BEV',
    'x': [BEV[BEV['Make'] == make]['Electric Range'] for make in BEV['Make'].unique()],
    'y': BEV['Make'].unique()
}
handler.create_boxplot(data=boxplot_data, patch_artist=True)
handler.create_boxplot(data=boxplot_data_PHEV, patch_artist=True)
handler.create_boxplot(data=boxplot_data_BEV, patch_artist=True)

handler._plot = True
# displays the makes and the number of cars in each section
maker_data = {
    'xlabel': 'Make',
    'ylabel': 'No. of Vehicles',
    'title' : 'Top 10 Different Makers',
    'x': handler._df['Make'].value_counts().head(10).index.to_list(),
    'y': handler._df['Make'].value_counts().head(10).to_list()
}
handler.create_barplot(maker_data)

# displays the Model and the number of cars in each section
model_data = {
    'xlabel': 'Make',
    'ylabel': 'No. of Vehicles',
    'title' : 'Top 10 Different Models',
    'x': handler._df['Model'].value_counts().head(10).index.to_list(),
    'y': handler._df['Model'].value_counts().head(10).to_list()
}
handler.create_barplot(model_data)

car_type = {
    'title' : 'Vehicle type distribution',
    'y': handler._df['Electric Vehicle Type'].value_counts().head(10).index.to_list(),
    'x': handler._df['Electric Vehicle Type'].value_counts().head(10).to_list()
}
handler._plot = True
handler.create_piechart(car_type)

eligibility = {
    'title' : 'Clean Alternative Fuel Vehicle (CAFV) Eligibility',
    'y': handler._df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].value_counts().head(10).index.to_list(),
    'x': handler._df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].value_counts().head(10).to_list()
}
handler._plot = True
handler.create_piechart(eligibility)

print("Geographical:")
print("*",len(handler._df['County'].unique()),'counties')
print("*",len(handler._df['City'].unique()),'cities')
print("*",len(handler._df['Electric Utility'].unique()),'electric utilities')
print("\nMakes and Models:")
print("*",len(handler._df['Make'].unique()),'makes')
print("*",len(handler._df['Model'].unique()),'models')

handler._df.describe(exclude='number').T
#### THIS CODE IS TO READ DATA INTO A JSON FILE, DO NOT COMMENT OUT UNLESS NEED TO CREATE JSON FILE #############

# locations = []
# count = 0
# zipcode_location_data = {}

# # Assuming 'handler._df' has 'Postal Code' column with zip codes
# for zipcode in handler._df['Postal Code'].dropna().unique():
#     geolocator = Nominatim(user_agent="myGeocodingApp")
#     location = geolocator.geocode(int(zipcode))
    
#     if location:
#         # Store the latitude and longitude as a tuple in the dictionary
#         zipcode_location_data[int(zipcode)] = {'latitude': location.latitude, 'longitude': location.longitude}
    
#     count += 1
#     print(count)

# # Write the data to a JSON file
# with open("locations_data.json", "w") as file:
#     json.dump(zipcode_location_data, file)

######################################################################################################################


#### THIS CODE ONLY RUNS IN JUPYTER NOTEBOOK, DO NOT COMMENT OUT######

# with open("locations_data.json", "r") as file:
#     loaded_data = json.load(file)
# # print(loaded_data)
# map_usa = folium.Map(location=[39.5, -99.7], tiles='cartodbpositron', zoom_start=4.4)

# # # # Add points to the map
# mc = MarkerCluster()
# for loc in handler._df['Postal Code'].dropna():
#     key = str(int(loc))
#     lat, lon = loaded_data[key]['latitude'], loaded_data[key]['longitude']
#     mc.add_child(Marker([lat, lon]))
# map_usa.add_child(mc)

# map_usa

##########################################################################

