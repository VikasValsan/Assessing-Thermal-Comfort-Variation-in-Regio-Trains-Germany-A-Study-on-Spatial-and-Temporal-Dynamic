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
columns_to_clean = ['HVAC_OutsideTemp_value', 'Point1_Upperright.rh_value', 'Point1_Lowerright.rh_value',
                    'Point1_Upperleft.rh_value', 'Point2_Upperright.rh_value', 'Point2_Upperleft.rh_value',
                    'Point1_Lowerleft.rh_value', 'Point2_Lowerleft.rh_value', 'Point2_Lowerright.rh_value',
                    'Point2_Upperright.rh_value', 'Point2_Lowerright.rh_value', 'Point1_Upperright.t_db_value',
                    'Point1_Upperleft.t_db_value', 'Point1_Lowerright.t_db_value', 'Point1_Lowerleft.t_db_value',
                    'Point2_Upperright.t_db_value', 'Point2_Upperleft.t_db_value', 'Point2_Lowerleft.t_db_value',
                    'Point2_Lowerright.t_db_value']
data_cleaned = data.copy()
for column in columns_to_clean:
    data_cleaned = data_cleaned[(data_cleaned[column] != 0) & (data_cleaned[column].notna())]

# Apply humidity threshold function
def humidity_threshold(Tem):
    if Tem <= 22.5:
        return 75.0
    else:
        return 75.0 - 3 * (Tem - 22.5)

# Apply HumidityThreshold for each point based on its corresponding t_db_value
data_cleaned['Point1_Upperright_HumidityThreshold'] = data_cleaned['Point1_Upperright.t_db_value'].apply(humidity_threshold)
data_cleaned['Point1_Upperleft_HumidityThreshold'] = data_cleaned['Point1_Upperleft.t_db_value'].apply(humidity_threshold)
data_cleaned['Point2_Upperright_HumidityThreshold'] = data_cleaned['Point2_Upperright.t_db_value'].apply(humidity_threshold)
data_cleaned['Point2_Upperleft_HumidityThreshold'] = data_cleaned['Point2_Upperleft.t_db_value'].apply(humidity_threshold)

data_cleaned['Point1_Lowerleft_HumidityThreshold'] = data_cleaned['Point1_Lowerleft.t_db_value'].apply(humidity_threshold)
data_cleaned['Point1_Lowerright_HumidityThreshold'] = data_cleaned['Point1_Lowerright.t_db_value'].apply(humidity_threshold)
data_cleaned['Point2_Lowerleft_HumidityThreshold'] = data_cleaned['Point2_Lowerleft.t_db_value'].apply(humidity_threshold)
data_cleaned['Point2_Lowerright_HumidityThreshold'] = data_cleaned['Point2_Lowerright.t_db_value'].apply(humidity_threshold)

# Filter data for July 11, 2024
filtered_data = data_cleaned[data_cleaned['Datetime'].dt.date == pd.Timestamp('2024-07-11').date()]

# Create 2x2 grid for Upper Deck
fig_upper, axs_upper = plt.subplots(2, 2, figsize=(14, 10))
fig_upper.suptitle('Upper Deck - Relative Humidity (July 11, 2024)', fontsize=16)

# Upper Deck - Plot each point
# Point1_Upperright
axs_upper[0, 0].plot(filtered_data['Time_HHMM'], filtered_data['Point1_Upperright.rh_value'], label='RH (Point1 Upper Right)', color='orange')
axs_upper[0, 0].plot(filtered_data['Time_HHMM'], filtered_data['Point1_Upperright_HumidityThreshold'], label='Humidity Threshold', linestyle='--', color='green')
axs_upper[0, 0].set_title('Point1_Upperright')
axs_upper[0, 0].set_xlabel('Time (HH:MM)')
axs_upper[0, 0].set_ylabel('Relative Humidity (%)')
axs_upper[0, 0].set_ylim(30, 100)
axs_upper[0, 0].grid(True)
axs_upper[0, 0].legend(loc='upper right')
axs_upper[0, 0].set_xticks(np.arange(0, len(filtered_data['Time_HHMM']), step=60))
axs_upper[0, 0].set_xticklabels(filtered_data['Time_HHMM'][::60], rotation=45, fontsize=10)

# Point1_Upperleft
axs_upper[0, 1].plot(filtered_data['Time_HHMM'], filtered_data['Point1_Upperleft.rh_value'], label='RH (Point1 Upper Left)', color='blue')
axs_upper[0, 1].plot(filtered_data['Time_HHMM'], filtered_data['Point1_Upperleft_HumidityThreshold'], label='Humidity Threshold', linestyle='--', color='green')
axs_upper[0, 1].set_title('Point1_Upperleft')
axs_upper[0, 1].set_xlabel('Time (HH:MM)')
axs_upper[0, 1].set_ylabel('Relative Humidity (%)')
axs_upper[0, 1].set_ylim(30, 100)
axs_upper[0, 1].grid(True)
axs_upper[0, 1].legend(loc='upper right')
axs_upper[0, 1].set_xticks(np.arange(0, len(filtered_data['Time_HHMM']), step=60))
axs_upper[0, 1].set_xticklabels(filtered_data['Time_HHMM'][::60], rotation=45, fontsize=10)

# Point2_Upperright
axs_upper[1, 0].plot(filtered_data['Time_HHMM'], filtered_data['Point2_Upperright.rh_value'], label='RH (Point2 Upper Right)', color='purple')
axs_upper[1, 0].plot(filtered_data['Time_HHMM'], filtered_data['Point2_Upperright_HumidityThreshold'], label='Humidity Threshold', linestyle='--', color='green')
axs_upper[1, 0].set_title('Point2_Upperright')
axs_upper[1, 0].set_xlabel('Time (HH:MM)')
axs_upper[1, 0].set_ylabel('Relative Humidity (%)')
axs_upper[1, 0].set_ylim(30, 100)
axs_upper[1, 0].grid(True)
axs_upper[1, 0].legend(loc='upper right')
axs_upper[1, 0].set_xticks(np.arange(0, len(filtered_data['Time_HHMM']), step=60))
axs_upper[1, 0].set_xticklabels(filtered_data['Time_HHMM'][::60], rotation=45, fontsize=10)

# Point2_Upperleft
axs_upper[1, 1].plot(filtered_data['Time_HHMM'], filtered_data['Point2_Upperleft.rh_value'], label='RH (Point2 Upper Left)', color='green')
axs_upper[1, 1].plot(filtered_data['Time_HHMM'], filtered_data['Point2_Upperleft_HumidityThreshold'], label='Humidity Threshold', linestyle='--', color='black')
axs_upper[1, 1].set_title('Point2_Upperleft')
axs_upper[1, 1].set_xlabel('Time (HH:MM)')
axs_upper[1, 1].set_ylabel('Relative Humidity (%)')
axs_upper[1, 1].set_ylim(30, 100)
axs_upper[1, 1].grid(True)
axs_upper[1, 1].legend(loc='upper right')
axs_upper[1, 1].set_xticks(np.arange(0, len(filtered_data['Time_HHMM']), step=60))
axs_upper[1, 1].set_xticklabels(filtered_data['Time_HHMM'][::60], rotation=45, fontsize=10)

# Adjust layout and show Upper Deck plot
plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.show()

# Create 2x2 grid for Lower Deck
fig_lower, axs_lower = plt.subplots(2, 2, figsize=(14, 10))
fig_lower.suptitle('Lower Deck - Relative Humidity (July 11, 2024)', fontsize=16)

# Lower Deck - Plot each point
# Point1_Lowerleft
axs_lower[0, 0].plot(filtered_data['Time_HHMM'], filtered_data['Point1_Lowerleft.rh_value'], label='RH (Point1 Lower Left)', color='red')
axs_lower[0, 0].plot(filtered_data['Time_HHMM'], filtered_data['Point1_Lowerleft_HumidityThreshold'], label='Humidity Threshold', linestyle='--', color='green')
axs_lower[0, 0].set_title('Point1_Lowerleft')
axs_lower[0, 0].set_xlabel('Time (HH:MM)')
axs_lower[0, 0].set_ylabel('Relative Humidity (%)')
axs_lower[0, 0].set_ylim(30, 100)
axs_lower[0, 0].grid(True)
axs_lower[0, 0].legend(loc='upper right')
axs_lower[0, 0].set_xticks(np.arange(0, len(filtered_data['Time_HHMM']), step=60))
axs_lower[0, 0].set_xticklabels(filtered_data['Time_HHMM'][::60], rotation=45, fontsize=10)

# Point1_Lowerright
axs_lower[0, 1].plot(filtered_data['Time_HHMM'], filtered_data['Point1_Lowerright.rh_value'], label='RH (Point1 Lower Right)', color='brown')
axs_lower[0, 1].plot(filtered_data['Time_HHMM'], filtered_data['Point1_Lowerright_HumidityThreshold'], label='Humidity Threshold', linestyle='--', color='green')
axs_lower[0, 1].set_title('Point1_Lowerright')
axs_lower[0, 1].set_xlabel('Time (HH:MM)')
axs_lower[0, 1].set_ylabel('Relative Humidity (%)')
axs_lower[0, 1].set_ylim(30, 100)
axs_lower[0, 1].grid(True)
axs_lower[0, 1].legend(loc='upper right')
axs_lower[0, 1].set_xticks(np.arange(0, len(filtered_data['Time_HHMM']), step=60))
axs_lower[0, 1].set_xticklabels(filtered_data['Time_HHMM'][::60], rotation=45, fontsize=10)

# Point2_Lowerleft
axs_lower[1, 0].plot(filtered_data['Time_HHMM'], filtered_data['Point2_Lowerleft.rh_value'], label='RH (Point2 Lower Left)', color='darkred')
axs_lower[1, 0].plot(filtered_data['Time_HHMM'], filtered_data['Point2_Lowerleft_HumidityThreshold'], label='Humidity Threshold', linestyle='--', color='green')
axs_lower[1, 0].set_title('Point2_Lowerleft')
axs_lower[1, 0].set_xlabel('Time (HH:MM)')
axs_lower[1, 0].set_ylabel('Relative Humidity (%)')
axs_lower[1, 0].set_ylim(30, 100)
axs_lower[1, 0].grid(True)
axs_lower[1, 0].legend(loc='upper right')
axs_lower[1, 0].set_xticks(np.arange(0, len(filtered_data['Time_HHMM']), step=60))
axs_lower[1, 0].set_xticklabels(filtered_data['Time_HHMM'][::60], rotation=45, fontsize=10)

# Point2_Lowerright
axs_lower[1, 1].plot(filtered_data['Time_HHMM'], filtered_data['Point2_Lowerright.rh_value'], label='RH (Point2 Lower Right)', color='darkblue')
axs_lower[1, 1].plot(filtered_data['Time_HHMM'], filtered_data['Point2_Lowerright_HumidityThreshold'], label='Humidity Threshold', linestyle='--', color='green')
axs_lower[1, 1].set_title('Point2_Lowerright')
axs_lower[1, 1].set_xlabel('Time (HH:MM)')
axs_lower[1, 1].set_ylabel('Relative Humidity (%)')
axs_lower[1, 1].set_ylim(30, 100)
axs_lower[1, 1].grid(True)
axs_lower[1, 1].legend(loc='upper right')
axs_lower[1, 1].set_xticks(np.arange(0, len(filtered_data['Time_HHMM']), step=60))
axs_lower[1, 1].set_xticklabels(filtered_data['Time_HHMM'][::60], rotation=45, fontsize=10)

# Adjust layout and show Lower Deck plot
plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.show()

