## Notes
csv is downloaded from: 
https://data.wa.gov/Transportation/Electric-Vehicle-Population-Data/f6w7-q2d2/about_data

<b> It is recommended to use the notebooks to visualise data. </b>

## What the files do
The dataset_handler.py contains the dataset_handler class that is used to handle the data set, this includes plot generation, and cleaning the data.

The Jupiter notebook file named visual1.ipynb utilizes the dataset_handler to generate diagrams and gain insight from the data.

The Jupiter notebook file named visual2.ipynb is the map of EV distribution in Washington (including the cars that left Washington as well). 

The Jupiter notebook file named visual3.ipynb is the map of the electric vehicles by type.

The Jupiter notebook file named clustering.ipynb focus on the Washington state and shows the visualization about company adress selection based on clustering and distribution of vehicle types around each clustering centers.

visual.py = visual1.ipynb + visual2.ipynb + visual3.ipynb. Caveat: map visualisations only works in notebook

vehicle_clustering.py = clustering.ipynb

