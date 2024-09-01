import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def plot_air_temperature(file_path):
    # Load the dataset with the correct header row (A2 corresponds to header=1 in pandas)
    data = pd.read_excel(file_path, header=1)  # Header is in the second row (A2:W2)

    # Ensure the relevant columns are numeric and handle any missing values
    data['Air Temp @0.10m '] = pd.to_numeric(data['Air Temp @0.10m '], errors='coerce')
    data['Air Temp @1.10m'] = pd.to_numeric(data['Air Temp @1.10m'], errors='coerce')
    data['Air Temp @1.70m '] = pd.to_numeric(data['Air Temp @1.70m '], errors='coerce')
    data['Point1_Upperleft.t_db_value'] = pd.to_numeric(data['Point1_Upperleft.t_db_value'], errors='coerce')

    # Convert the Datetime column to proper datetime format and extract time
    data['Time'] = data['Datetime'].dt.strftime('%H:%M')

    # Drop rows with NaN values or 0 values in any of the Air Temperature columns
    cleaned_data = data.dropna(subset=['Time', 'Air Temp @0.10m ', 'Air Temp @1.10m', 'Air Temp @1.70m ', 'Point1_Upperleft.t_db_value'])
    cleaned_data = cleaned_data[(cleaned_data['Air Temp @0.10m '] != 0) &
                                (cleaned_data['Air Temp @1.10m'] != 0) &
                                (cleaned_data['Air Temp @1.70m '] != 0) &
                                (cleaned_data['Point1_Upperleft.t_db_value'] != 0)]

    # Plotting the data with cleaned time values
    plt.figure(figsize=(14, 7))  # Increase figure size for better readability
    plt.plot(cleaned_data['Time'], cleaned_data['Air Temp @0.10m '], color='red', label='$ta_{0.10m}$')
    plt.plot(cleaned_data['Time'], cleaned_data['Air Temp @1.10m'], color='blue', label='$ta_{1.10m}$')
    plt.plot(cleaned_data['Time'], cleaned_data['Air Temp @1.70m '], color='green', label='$ta_{1.70m}$')
    plt.plot(cleaned_data['Time'], cleaned_data['Point1_Upperleft.t_db_value'], color='purple', label='$ta_{CDSK}$')

    # Labels and legend
    plt.xlabel('Time (HH:MM)')
    plt.ylabel('Air Temperature (°C)')
    plt.legend()

    # Adjust x-axis labels to prevent overlap
    plt.xticks(rotation=90)

    # Reduce the number of x-ticks for clarity
    plt.xticks(ticks=plt.xticks()[0][::10])  # Display every 10th label

    plt.tight_layout()
    plt.show()

def select_file():
    Tk().withdraw()  # We don't want a full GUI, so keep the root window from appearing
    file_path = askopenfilename(title="Select the dataset file", filetypes=[("Excel files", "*.xlsx *.xls")])
    return file_path

# Usage example
file_path = select_file()
if file_path:
    plot_air_temperature(file_path)
else:
    print("No file selected.")
