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
columns_to_clean = ['HVAC_OutsideTemp_value', 'Point1_Upperright.rh_value', 'Point1_Lowerright.rh_value']
data_cleaned = data.copy()
for column in columns_to_clean:
    data_cleaned = data_cleaned[(data_cleaned[column] != 0) & (data_cleaned[column].notna())]

# Apply humidity threshold function
def humidity_threshold(Tim):
    if Tim <= 22.5:
        return 75.0
    else:
        return 75.0 - 3 * (Tim - 22.5)

data_cleaned['HumidityThreshold'] = data_cleaned['HVAC_Insidetemp_value'].apply(humidity_threshold)

# Filter data for July 11, 2024
filtered_data = data_cleaned[data_cleaned['Datetime'].dt.date == pd.Timestamp('2024-07-11').date()]

# Plot Relative Humidity
plt.figure(figsize=(14, 12))
# Upper Deck
plt.subplot(2, 1, 1)
plt.plot(filtered_data['Time_HHMM'], filtered_data['Point1_Upperright.rh_value'], label='RH (Upper)', color='orange')
plt.plot(filtered_data['Time_HHMM'], filtered_data['HumidityThreshold'], label='Humidity Threshold', linestyle='--', color='green')
plt.title('Upper Deck - Relative Humidity (July 11, 2024)')
plt.xlabel('Time (HH:MM)')
plt.ylabel('Relative Humidity (%)')
plt.xticks(np.arange(0, len(filtered_data['Time_HHMM']), step=60), rotation=45, fontsize=10)
plt.ylim(30, 80)
plt.grid(True)
plt.legend(loc='upper right')

# Lower Deck
plt.subplot(2, 1, 2)
plt.plot(filtered_data['Time_HHMM'], filtered_data['Point1_Lowerright.rh_value'], label='RH (Lower)', color='blue')
plt.plot(filtered_data['Time_HHMM'], filtered_data['HumidityThreshold'], label='Humidity Threshold', linestyle='--', color='green')
plt.title('Lower Deck - Relative Humidity (July 11, 2024)')
plt.xlabel('Time (HH:MM)')
plt.ylabel('Relative Humidity (%)')
plt.xticks(np.arange(0, len(filtered_data['Time_HHMM']), step=60), rotation=45, fontsize=10)
plt.ylim(30, 80)
plt.grid(True)
plt.legend(loc='upper right')

plt.tight_layout()
plt.show()
