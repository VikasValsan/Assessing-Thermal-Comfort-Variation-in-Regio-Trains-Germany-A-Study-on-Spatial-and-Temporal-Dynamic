import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Function to select a file
def select_file():
    root = Tk()
    root.withdraw()
    filename = askopenfilename()
    root.destroy()  # Properly close the Tkinter root window
    return filename

# Load the dataset
file_path = select_file()
data = pd.read_csv(file_path, delimiter=';')

# Parse the Datetime column
data['Datetime'] = pd.to_datetime(data['Datetime'], format='%d.%m.%Y %H:%M')
data['Time_HHMM'] = data['Datetime'].dt.strftime('%H:%M')

# Function to remove outliers using IQR
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Remove NaN, 0 values, and outliers
columns_to_clean = ['HVAC_OutsideTemp_value', 'Point1_Upperright.to_value', 'Point1_Lowerright.to_value',
                    'Point1_Upperleft.to_value', 'Point1_Lowerleft.to_value', 'Point2_Upperright.to_value',
                    'Point2_Lowerright.to_value', 'Point2_Upperleft.to_value', 'Point2_Lowerleft.to_value']

data_cleaned = data.copy()
for column in columns_to_clean:
    # Remove NaN and 0 values
    data_cleaned = data_cleaned[(data_cleaned[column] != 0) & (data_cleaned[column].notna())]
    # Remove outliers
    data_cleaned = remove_outliers(data_cleaned, column)

# Filter data for July 11, 2024
filtered_data = data_cleaned[data_cleaned['Datetime'].dt.date == pd.Timestamp('2024-07-11').date()]

# Function to add the translucent yellow highlight for the ISO 7730 threshold
def add_iso7730_threshold():
    plt.fill_between(filtered_data['Time_HHMM'], 23, 26, color='yellow', alpha=0.3, label='Threshold ISO 7730')

# Create 2x2 plots for the upper deck
plt.figure(figsize=(14, 10))

plt.subplot(2, 2, 1)
plt.plot(filtered_data['Time_HHMM'], filtered_data['Point1_Upperright.to_value'], label='Point1_Upperright', color='orange')
plt.plot(filtered_data['Time_HHMM'], filtered_data['HVAC_OutsideTemp_value'], label='Outside Temp', linestyle='--', color='black')
add_iso7730_threshold()
plt.title('Upper Deck - Point1_Upperright.to_value')
plt.xlabel('Time (HH:MM)')
plt.ylabel('Operative Temperature (°C)')  # Ensure y-axis label is added
plt.xticks(np.linspace(0, len(filtered_data['Time_HHMM'])-1, num=12), rotation=45, fontsize=10)
plt.ylim(16, 30)
plt.grid(True)
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(filtered_data['Time_HHMM'], filtered_data['Point1_Upperleft.to_value'], label='Point1_Upperleft', color='red')
plt.plot(filtered_data['Time_HHMM'], filtered_data['HVAC_OutsideTemp_value'], label='Outside Temp', linestyle='--', color='black')
add_iso7730_threshold()
plt.title('Upper Deck - Point1_Upperleft.to_value')
plt.xlabel('Time (HH:MM)')
plt.ylabel('Operative Temperature (°C)')  # Ensure y-axis label is added
plt.xticks(np.linspace(0, len(filtered_data['Time_HHMM'])-1, num=12), rotation=45, fontsize=10)
plt.ylim(16, 30)
plt.grid(True)
plt.legend()

plt.subplot(2, 2, 3)
plt.plot(filtered_data['Time_HHMM'], filtered_data['Point2_Upperright.to_value'], label='Point2_Upperright', color='purple')
plt.plot(filtered_data['Time_HHMM'], filtered_data['HVAC_OutsideTemp_value'], label='Outside Temp', linestyle='--', color='black')
add_iso7730_threshold()
plt.title('Upper Deck - Point2_Upperright.to_value')
plt.xlabel('Time (HH:MM)')
plt.ylabel('Operative Temperature (°C)')  # Ensure y-axis label is added
plt.xticks(np.linspace(0, len(filtered_data['Time_HHMM'])-1, num=12), rotation=45, fontsize=10)
plt.ylim(16, 30)
plt.grid(True)
plt.legend()

plt.subplot(2, 2, 4)
plt.plot(filtered_data['Time_HHMM'], filtered_data['Point2_Upperleft.to_value'], label='Point2_Upperleft', color='brown')
plt.plot(filtered_data['Time_HHMM'], filtered_data['HVAC_OutsideTemp_value'], label='Outside Temp', linestyle='--', color='black')
add_iso7730_threshold()
plt.title('Upper Deck - Point2_Upperleft.to_value')
plt.xlabel('Time (HH:MM)')
plt.ylabel('Operative Temperature (°C)')  # Ensure y-axis label is added
plt.xticks(np.linspace(0, len(filtered_data['Time_HHMM'])-1, num=12), rotation=45, fontsize=10)
plt.ylim(16, 30)
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# Create 2x2 plots for the lower deck
plt.figure(figsize=(14, 10))

plt.subplot(2, 2, 1)
plt.plot(filtered_data['Time_HHMM'], filtered_data['Point1_Lowerright.to_value'], label='Point1_Lowerright', color='blue')
plt.plot(filtered_data['Time_HHMM'], filtered_data['HVAC_OutsideTemp_value'], label='Outside Temp', linestyle='--', color='black')
add_iso7730_threshold()
plt.title('Lower Deck - Point1_Lowerright.to_value')
plt.xlabel('Time (HH:MM)')
plt.ylabel('Operative Temperature (°C)')  # Ensure y-axis label is added
plt.xticks(np.linspace(0, len(filtered_data['Time_HHMM'])-1, num=12), rotation=45, fontsize=10)
plt.ylim(16, 30)
plt.grid(True)
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(filtered_data['Time_HHMM'], filtered_data['Point1_Lowerleft.to_value'], label='Point1_Lowerleft', color='green')
plt.plot(filtered_data['Time_HHMM'], filtered_data['HVAC_OutsideTemp_value'], label='Outside Temp', linestyle='--', color='black')
add_iso7730_threshold()
plt.title('Lower Deck - Point1_Lowerleft.to_value')
plt.xlabel('Time (HH:MM)')
plt.ylabel('Operative Temperature (°C)')  # Ensure y-axis label is added
plt.xticks(np.linspace(0, len(filtered_data['Time_HHMM'])-1, num=12), rotation=45, fontsize=10)
plt.ylim(16, 30)
plt.grid(True)
plt.legend()

plt.subplot(2, 2, 3)
plt.plot(filtered_data['Time_HHMM'], filtered_data['Point2_Lowerright.to_value'], label='Point2_Lowerright', color='cyan')
plt.plot(filtered_data['Time_HHMM'], filtered_data['HVAC_OutsideTemp_value'], label='Outside Temp', linestyle='--', color='black')
add_iso7730_threshold()
plt.title('Lower Deck - Point2_Lowerright.to_value')
plt.xlabel('Time (HH:MM)')
plt.ylabel('Operative Temperature (°C)')  # Ensure y-axis label is added
plt.xticks(np.linspace(0, len(filtered_data['Time_HHMM'])-1, num=12), rotation=45, fontsize=10)
plt.ylim(16, 30)
plt.grid(True)
plt.legend()

plt.subplot(2, 2, 4)
plt.plot(filtered_data['Time_HHMM'], filtered_data['Point2_Lowerleft.to_value'], label='Point2_Lowerleft', color='magenta')
plt.plot(filtered_data['Time_HHMM'], filtered_data['HVAC_OutsideTemp_value'], label='Outside Temp', linestyle='--', color='black')
add_iso7730_threshold()
plt.title('Lower Deck - Point2_Lowerleft.to_value')
plt.xlabel('Time (HH:MM)')
plt.ylabel('Operative Temperature (°C)')  # Ensure y-axis label is added
plt.xticks(np.linspace(0, len(filtered_data['Time_HHMM'])-1, num=12), rotation=45, fontsize=10)
plt.ylim(16, 30)
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

