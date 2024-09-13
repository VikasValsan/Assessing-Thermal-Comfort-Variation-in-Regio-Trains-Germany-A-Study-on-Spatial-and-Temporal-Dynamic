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

# Function to remove outliers using IQR method
def remove_outliers(df, columns):
    for column in columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    return df

# Function to remove specific dips by time range
def remove_sharp_dips(df, column, start_time, end_time):
    df = df[~((df['Time_HHMM'] >= start_time) & (df['Time_HHMM'] <= end_time))]
    return df

# Load the dataset
file_path = select_file()
data = pd.read_csv(file_path, delimiter=';')

# Parse the Datetime column
data['Datetime'] = pd.to_datetime(data['Datetime'], format='%d.%m.%Y %H:%M')
data['Time_HHMM'] = data['Datetime'].dt.strftime('%H:%M')

# Remove NaN and 0 values
columns_to_clean = ['HVAC_OutsideTemp_value', 'Point1_Upperright.t_db_value', 'Point1_Upperleft.t_db_value',
                    'Point1_Lowerright.t_db_value', 'Point2_Lowerright.t_db_value', 'Point2_Lowerleft.t_db_value',
                    'Point2_Upperleft.t_db_value', 'Point2_Upperright.t_db_value']
data_cleaned = data.copy()
for column in columns_to_clean:
    data_cleaned = data_cleaned[(data_cleaned[column] != 0) & (data_cleaned[column].notna())]

# Remove outliers using IQR for temperature-related columns
data_cleaned = remove_outliers(data_cleaned, columns_to_clean)

# Remove sharp dips in Point2_Lowerleft between 11:41 and 16:26
data_cleaned = remove_sharp_dips(data_cleaned, 'Point2_Lowerleft.t_db_value', '11:41', '16:26')

# Apply temperature threshold function
def air_temp_threshold(Tem):
    if Tem <= 22.5:
        return 22.0
    elif 22.5 < Tem <= 35.0:
        return 22.0 + 0.4 * (Tem - 22.5)
    else:
        return 27.0

data_cleaned['AirTempThreshold'] = data_cleaned['HVAC_OutsideTemp_value'].apply(air_temp_threshold)

# Filter data for July 11, 2024
filtered_data = data_cleaned[data_cleaned['Datetime'].dt.date == pd.Timestamp('2024-07-11').date()]

# Separate columns for upper and lower deck
upper_deck_columns = ['Point1_Upperleft.t_db_value', 'Point1_Upperright.t_db_value',
                      'Point2_Upperleft.t_db_value', 'Point2_Upperright.t_db_value']
lower_deck_columns = ['Point1_Lowerright.t_db_value', 'Point1_Lowerleft.t_db_value', 'Point2_Lowerright.t_db_value',
                      'Point2_Lowerleft.t_db_value']

# Assign distinctive colors for each point
colors = ['orange', 'red', 'purple', 'brown', 'blue', 'green', 'cyan', 'magenta']

# Function to plot data in 2x2 grid with distinct colors
def plot_2x2_grid(temp_columns, deck_label, colors):
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'{deck_label} Deck - Air Temperature (July 11, 2024)', fontsize=16)

    for i, temp_col in enumerate(temp_columns):
        row, col = divmod(i, 2)  # Determine row and column for the 2x2 grid
        ax = axs[row, col]
        ax.plot(filtered_data['Time_HHMM'], filtered_data[temp_col], label=f'Air Temp ({temp_col.split(".")[0]})',
                color=colors[i])
        ax.plot(filtered_data['Time_HHMM'], filtered_data['AirTempThreshold'], label='Temp Threshold', linestyle='--',
                color='green')
        ax.plot(filtered_data['Time_HHMM'], filtered_data['HVAC_OutsideTemp_value'], label='Outside Temp',
                linestyle='--', color='black')

        ax.set_xlabel('Time (HH:MM)')
        ax.set_ylabel('Temperature (°C)')
        ax.set_ylim(16, 32)
        ax.grid(True)

        # Set x-axis ticks at 1-hour intervals, starting from 00:12
        ax.set_xticks(np.arange(0, len(filtered_data['Time_HHMM']), step=60))  # 60-minute intervals
        ax.set_xticklabels(filtered_data['Time_HHMM'][::60], rotation=45, fontsize=10)

        # Combine legends at the top right
        ax.legend(loc='upper right', fontsize=9)

        ax.set_title(f'{temp_col.split(".")[0]}')

    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()

# Plot upper deck temperatures (Point1 and Point2 Upper deck) with all 4 columns
plot_2x2_grid(upper_deck_columns, 'Upper', colors[:4])

# Plot lower deck temperatures (Point1 and Point2 Lower deck) with distinct colors
plot_2x2_grid(lower_deck_columns, 'Lower', colors[4:8])
