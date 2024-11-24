from dataset_handler import DatasetHandler
import matplotlib.pyplot as plt

handler = DatasetHandler(r"C:\Users\denve\ece143proj\Electric_Vehicle_Population_Data.csv")
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

handler.create_boxplot(boxplot_data)

for e, battery_type in enumerate(['PHEV', 'BEV'], start=1):

    # Filter the DataFrame for the current battery_type
    filtered_data = handler._df[handler._df['Electric Vehicle Type'] == battery_type]

    # Get unique makes and prepare data for box plot
    makes = sorted(filtered_data['Make'].unique())
    electric_ranges = [filtered_data[filtered_data['Make'] == make]['Electric Range'] for make in makes]

    # Create the box plot
    ev_data = {
        'xlabel': 'Make',
        'ylabel': 'Electric Range',
        'title' : f'Electric Range by Model Year for {battery_type}',
        'x': electric_ranges,
        'y': makes
    }
    handler.create_boxplot(ev_data, patch_artist=True)

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
