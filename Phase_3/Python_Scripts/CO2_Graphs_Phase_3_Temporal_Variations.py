import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename


# Function to select a file
def select_file():
    Tk().withdraw()
    filename = askopenfilename()
    return filename


# Load the dataset
file_path = select_file()
data = pd.read_csv(file_path, delimiter=';')

# Parse the Datetime column
data['Datetime'] = pd.to_datetime(data['Datetime'], format='%d.%m.%Y %H:%M')
data['Time_HHMM'] = data['Datetime'].dt.strftime('%H:%M')

# Remove NaN and 0 values
columns_to_clean = ['HVAC_OutsideTemp_value']
co2_columns = [col for col in data.columns if col.endswith('.co2_value')]
columns_to_clean.extend(co2_columns)

data_cleaned = data.copy()
for column in columns_to_clean:
    data_cleaned = data_cleaned[(data_cleaned[column] != 0) & (data_cleaned[column].notna())]


# Apply CO2 threshold function
def co2_threshold_corrected(Tem):
    if -15 <= Tem <= -5:
        return 1600
    elif -5 < Tem <= 26:
        return 1275
    else:
        return 1600


data_cleaned['CO2Threshold'] = data_cleaned['HVAC_OutsideTemp_value'].apply(co2_threshold_corrected)

# Filter data for July 11, 2024
filtered_data = data_cleaned[data_cleaned['Datetime'].dt.date == pd.Timestamp('2024-07-11').date()]

# Separate columns for upper and lower deck
upper_deck_columns = ['Point1_Upperright.co2_value', 'Point1_Upperleft.co2_value', 'Point2_Upperright.co2_value',
                      'Point2_Upperleft.co2_value']
lower_deck_columns = ['Point1_Lowerright.co2_value', 'Point1_Lowerleft.co2_value', 'Point2_Lowerright.co2_value',
                      'Point2_Lowerleft.co2_value']

# Define distinct colors for CO2 values
upper_deck_colors = ['orange', 'blue', 'green', 'purple']  # Colors for the upper deck
lower_deck_colors = ['cyan', 'magenta', 'yellow', 'brown']  # Distinct colors for the lower deck


# Function to plot data in 2x2 grid with distinctive colors for each CO2 sensor
def plot_2x2_grid(co2_columns, deck_label, co2_colors):
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'{deck_label} Deck - CO2 Concentration & Outdoor Temperature (July 11, 2024)', fontsize=16)

    for i, co2_col in enumerate(co2_columns):
        row, col = divmod(i, 2)  # Determine row and column for the 2x2 grid
        ax1 = axs[row, col]
        co2_color = co2_colors[i % len(co2_colors)]  # Use distinct colors for CO2 plots

        ax1.plot(filtered_data['Time_HHMM'], filtered_data[co2_col], label=f'CO2 ({co2_col.split(".")[0]})',
                 color=co2_color)
        ax1.plot(filtered_data['Time_HHMM'], filtered_data['CO2Threshold'], label='CO2 Threshold', linestyle='--',
                 color='green')
        ax1.set_xlabel('Time (HH:MM)')
        ax1.set_ylabel('CO2 (ppm)')
        ax1.set_ylim(400, 2500)
        ax1.grid(True)

        # Create a second y-axis for outdoor temperature
        ax2 = ax1.twinx()
        ax2.plot(filtered_data['Time_HHMM'], filtered_data['HVAC_OutsideTemp_value'], label='Outdoor Temp', color='red')
        ax2.set_ylabel('Outdoor Temperature (°C)')
        ax2.set_ylim(-10, 40)

        # Add a black horizontal line at 26°C
        ax2.axhline(y=26, color='black', linestyle='-', linewidth=1)

        # Set the x-axis starting from 00:12 with 1-hour intervals
        ax1.set_xticks(np.arange(0, len(filtered_data['Time_HHMM']), step=60))  # 60-minute intervals
        ax1.set_xticklabels(filtered_data['Time_HHMM'][::60], rotation=45, fontsize=10)

        # Combine all three legends together at the top left
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)

        ax1.set_title(f'{co2_col.split(".")[0]}')

    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()


# Plot upper deck with distinct colors for upper deck
plot_2x2_grid(upper_deck_columns, 'Upper', upper_deck_colors)

# Plot lower deck with distinct colors for lower deck
plot_2x2_grid(lower_deck_columns, 'Lower', lower_deck_colors)
