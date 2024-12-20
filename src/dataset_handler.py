import pandas as pd
import matplotlib.pyplot as plt
# import folium

class DatasetHandler:

    def __init__(self, filename):
        """
        Reads the data into a dataframe and does initial processing
        """
        assert isinstance(filename, str)
        assert len(filename) > 0

        self._plot = False # controls whether plots should be displayed. Useful for debugging

        try:
            self._df = pd.read_csv(filename)
        except FileNotFoundError:
            print("The file could not be found!")

    def clean_dataset(self,printing=False):
        """
        Cleans the dataset i.e removes NaNs, errors, etc... and makes the dataset simpler to use.
        """
        # if we run the following, we see that Legislative District has the most number of NaN values
        if(printing):
            print(self._df.isna().sum().to_frame('NaN'))
        # we can fix this as follows:
        self._df['Legislative District'] = self._df['Legislative District'].map(lambda x: str(x).split('.')[0])
        # in a similar way for Vehicle Location
        # forward fill propigates the last observed values to fill the NaN slots
        self._df['Vehicle Location'] = self._df['Vehicle Location'].ffill()
        # Secondly, Legislative District is of dtype object, when it should be float so we can change it

        # We can rename the electric vehicle types for simplicity, i.e Plug-in Hybrid Electric Vehicle (PHEV) to PHEV
        ev_type = []
        for elem in self._df['Electric Vehicle Type']:
            if 'PHEV' in elem:
                ev_type.append('PHEV')
            elif 'BEV' in elem:
                ev_type.append('BEV')
            else:
                raise ValueError("Value has to be either PHEV or BEV!")
        self._df['Electric Vehicle Type'] = ev_type

        # We can do something similar for CAFV
        eligible = []
        for elem in self._df['Clean Alternative Fuel Vehicle (CAFV) Eligibility']:
            if 'Not eligible due to low battery range' == elem:
                eligible.append('Not Eligible')
            elif 'Eligibility unknown as battery range has not been researched' == elem:
                eligible.append('Unkown')
            elif 'Clean Alternative Fuel Vehicle Eligible' == elem:
                eligible.append('Eligible')
        self._df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'] = eligible
        self._df= self._df.ffill()#ffill any unfixed nan
        # print(self._df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'])

    def create_graph(self, data={}):
        """
        Abstracts away the core funcitonality of the visualization code.
        """
        assert isinstance(data, dict)
        assert len(data) > 0
        assert "x" in data
        assert "y" in data

        fig, ax = plt.subplots()
        
        ax.set_xlabel(data.get('xlabel', 'X'))
        ax.set_ylabel(data.get('ylabel', 'Y'))
        ax.set_title(data.get('title', 'Title'))

        return ax

    def create_boxplot(self, data={}, patch_artist=False):
        """
        Creates a boxplot
        """
        ax = self.create_graph(data)
        bxplot=ax.boxplot(data["x"], labels=data["y"], patch_artist=patch_artist)
        if(patch_artist):
            cmap = plt.get_cmap('hsv')
            colors = [cmap(x/len(bxplot['boxes']))for x in range(0,len(bxplot['boxes']))]
            for patch, color in zip(bxplot['boxes'], colors):
                patch.set_facecolor(color)
        ax.tick_params(axis='x', rotation=90)
        
        if self._plot: plt.show()

    def create_barplot(self, data={}, rotate=True, patch_artist=False):
        """
        Creates a barplot
        """
        ax = self.create_graph(data)

        if(patch_artist):
            cmap = plt.get_cmap('tab20')
            colors = [cmap(x/len(data['x']))for x in range(0,len(data['x']))]
            ax.bar(data['x'], data['y'], color=colors)
        else:
            ax.bar(data['x'], data['y'])
        if rotate: ax.tick_params(axis='x', rotation=90)
        
        if self._plot: plt.show()

    def create_piechart(self, data={}, patch_artist=False):
        """
        Creates a piechart
        """
        ax = self.create_graph(data)

        ax.set_xlabel('')
        ax.set_ylabel('')
        if(patch_artist):
            cmap = plt.get_cmap('tab20')
            colors = [cmap(x/len(data['x']))for x in range(0,len(data['x']))]
            ax.pie(data['x'], labels=data['y'], autopct='%1.1f%%', colors=colors)
        else:
            ax.pie(data['x'], labels=data['y'], autopct='%1.1f%%')
        if self._plot: plt.show()
