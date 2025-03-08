import pandas as pd
from matplotlib import pyplot as plt

class StocksifyVisualizer:
    def __init__(self, file_path=None):
        """
        Initializes the class and loads the dataframe if a file path is provided.
        """
        self.df = None
        if file_path:
            self.read_data(file_path)
        self.hiphop_group = ["Beton.Hofi","Pogány Induló","Krúbi","ekhoe","Co Lee", "Ótvar Pestis", "Franko", "Wavy"]
        self.folk_group = ["Дeva","Parno Graszt", "aurevoir.", "Bohemian Betyárs"]
        self.classic_alter_group = ["Kispál és a Borz", "Quimby", "30Y", "Heaven Street Seven", "Kaukázus", "Kiscsillag"]
        self.new_wave_alter_group = ["Elefánt", "Csaknekedkislány", "Esti Kornél", "Carson Coma", "Galaxisok", "Analog Balaton", "Blahalouisiana", "ajsa luna"]
        self.producer_group = ["Hundred Sins","Blaize","Beatrick","TEMBO","Dom Beats", "ANUBII$"]

    def read_data(self, file_path):
        """
        Reads the dataframe from a given file path and converts numeric columns.
        """
        self.df = pd.read_csv(file_path, index_col=0, parse_dates=True)
        self.df = self.df.iloc[2:,:]
        self.df = self.df.apply(pd.to_numeric, errors='coerce')  # Convert text numbers to numeric
    
    def calculate_percentage_change(self):
        """Calculates the percentage change relative to the first valid value for each artist."""
        df_perc = self.df.copy()
        for col in df_perc.columns:
            first_valid_index = df_perc[col].first_valid_index()
            if first_valid_index is not None:
                df_perc[col] = df_perc[col] / df_perc[col].loc[first_valid_index] * 100
        return df_perc

    def plot_top_gainers(self, num_artists=5):
        """Plots the top gainers in a line graph based on percentage change."""
        df_perc = self.calculate_percentage_change()
        last_day = df_perc.iloc[-1]  # Get last available data point

        gainers = last_day.nlargest(num_artists).index

        plt.figure(figsize=(12, 6))
        for artist in gainers:
            plt.plot(df_perc.index, df_perc[artist], label=f"▲ {artist}")

        plt.axhline(y=100, color="gray", linestyle="dotted")  # Reference line at 100%
        plt.xlabel("Date")
        plt.ylabel("Percentage of Initial Listeners")
        plt.title(f"Top {num_artists} Listener Gainers")
        plt.legend()
        plt.show()

    def plot_top_losers(self, num_artists=5):
        """Plots the top losers in a line graph based on percentage change."""
        df_perc = self.calculate_percentage_change()
        last_day = df_perc.iloc[-1]  # Get last available data point

        losers = last_day.nsmallest(num_artists).index

        plt.figure(figsize=(12, 6))
        for artist in losers:
            plt.plot(df_perc.index, df_perc[artist], linestyle="dashed", label=f"▼ {artist}")

        plt.axhline(y=100, color="gray", linestyle="dotted")  # Reference line at 100%
        plt.xlabel("Date")
        plt.ylabel("Percentage of Initial Listeners")
        plt.title(f"Top {num_artists} Listener Losers")
        plt.legend()
        plt.show()

    def plot_selected_artists(self, artist_list, as_percentage=True):
        """Plots selected artists over time, either as percentage or absolute numbers."""
        # Convert all artist names in selected_artists to lowercase for case-insensitive matching
        selected_artists_lower = [artist.lower() for artist in artist_list]
        print(selected_artists_lower)
        
        plt.figure(figsize=(12, 6))
        df_plot = self.calculate_percentage_change() if as_percentage else self.df

        # Convert the DataFrame columns (artist names) to lowercase for case-insensitive matching
        df_plot = df_plot.rename(columns=lambda x: x.lower())
        
        print(df_plot.columns)
        # Filter the DataFrame based on the lowercase artist names
        selected_artists_lower_case = [artist for artist in selected_artists_lower if artist in df_plot.columns]

        print(selected_artists_lower_case)

        for artist in selected_artists_lower_case:
            plt.plot(df_plot.index, df_plot[artist], label=artist)

        plt.xlabel("Date")
        plt.ylabel("Listeners (%)" if as_percentage else "Listeners")
        plt.title("Listener Trends Over Time")
        plt.legend()
        plt.show()
    
    def plot_average_for_artists(self, groups_of_artists):
        # Convert DataFrame columns (artist names) to lowercase for case-insensitive matching
        df_lower = self.df.rename(columns=lambda x: x.lower())
        
        plt.figure(figsize=(12, 6))
        
        # Iterate over each group of artists in the dictionary
        for group, artists in groups_of_artists.items():
            # Convert artist names in the group to lowercase for case-insensitive matching
            artists_lower = [artist.lower() for artist in artists]
            
            # Filter selected artists based on case-insensitive match
            artists_lower_case = [artist for artist in artists_lower if artist in df_lower.columns]
            
            # Calculate the average for each day for the selected artists in this group
            df_average = df_lower[artists_lower_case].mean(axis=1)
            
            # Plot the result for this group
            plt.plot(self.df.index, df_average, label=f"Average of {group}")
        
        # Customize the plot
        plt.title("Average of Selected Artists Over Time")
        plt.xlabel("Date")
        plt.ylabel("Average Value")
        plt.legend()
        plt.show()