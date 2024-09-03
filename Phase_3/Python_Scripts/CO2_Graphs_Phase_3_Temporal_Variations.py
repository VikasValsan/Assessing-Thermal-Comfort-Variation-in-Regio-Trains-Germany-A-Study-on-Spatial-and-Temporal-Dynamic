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
columns_to_clean = ['HVAC_OutsideTemp_value', 'Point1_Upperright.co2_value', 'Point1_Lowerright.co2_value']
data_cleaned = data.copy()
for column in columns_to_clean:
    data_cleaned = data_cleaned[(data_cleaned[column] != 0) & (data_cleaned[column].notna())]

# Apply CO2 threshold function
def co2_threshold_corrected(Tem):
    if -5 <= Tem <= 15:
        return 1600
    elif 15 < Tem <= 26:
        return 1275
    else:
        return 1600

data_cleaned['CO2Threshold'] = data_cleaned['HVAC_OutsideTemp_value'].apply(co2_threshold_corrected)

# Filter data for July 11, 2024
filtered_data = data_cleaned[data_cleaned['Datetime'].dt.date == pd.Timestamp('2024-07-11').date()]

# Plot CO2 Concentration
plt.figure(figsize=(14, 12))
# Upper Deck
plt.subplot(2, 1, 1)
plt.plot(filtered_data['Time_HHMM'], filtered_data['Point1_Upperright.co2_value'], label='CO2 (Upper)', color='orange')
plt.plot(filtered_data['Time_HHMM'], filtered_data['CO2Threshold'], label='CO2 Threshold', linestyle='--', color='green')
plt.title('Upper Deck - CO2 Concentration (July 11, 2024)')
plt.xlabel('Time (HH:MM)')
plt.ylabel('CO2 (ppm)')
plt.xticks(np.arange(0, len(filtered_data['Time_HHMM']), step=60), rotation=45, fontsize=10)
plt.ylim(400, 2500)
plt.grid(True)
plt.legend(loc='upper right')

# Continuation from where the previous snippet left off

# Lower Deck
plt.subplot(2, 1, 2)
plt.plot(filtered_data['Time_HHMM'], filtered_data['Point1_Lowerright.co2_value'], label='CO2 (Lower)', color='blue')
plt.plot(filtered_data['Time_HHMM'], filtered_data['CO2Threshold'], label='CO2 Threshold', linestyle='--', color='green')
plt.title('Lower Deck - CO2 Concentration (July 11, 2024)')
plt.xlabel('Time (HH:MM)')
plt.ylabel('CO2 (ppm)')
plt.xticks(np.arange(0, len(filtered_data['Time_HHMM']), step=60), rotation=45, fontsize=10)
plt.ylim(400, 2500)
plt.grid(True)
plt.legend(loc='upper right')

plt.tight_layout()
plt.show()
