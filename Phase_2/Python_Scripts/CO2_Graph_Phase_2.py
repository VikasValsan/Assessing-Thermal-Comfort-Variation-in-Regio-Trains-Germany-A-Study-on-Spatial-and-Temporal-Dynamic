import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def plot_co2_concentration(file_path):
    # Load the dataset with the correct header row (A2 corresponds to header=1 in pandas)
    data = pd.read_excel(file_path, header=1)  # Header is in the second row (A2:W2)

    # Ensure the relevant columns are numeric and handle any missing values
    data['CO2 Concentration @1.10m '] = pd.to_numeric(data['CO2 Concentration @1.10m '], errors='coerce')
    data['Point1_Upperleft.co2_value'] = pd.to_numeric(data['Point1_Upperleft.co2_value'], errors='coerce')

    # Convert the Datetime column to proper datetime format and extract time
    data['Time'] = pd.to_datetime(data['Datetime'], format='%d:%m:%Y:%H:%M', errors='coerce').dt.strftime('%H:%M')

    # Drop rows with NaN values in 'Time', 'CO2 Concentration @1.10m ', or 'Point1_Upperleft.co2_value' columns
    cleaned_data = data.dropna(subset=['Time', 'CO2 Concentration @1.10m ', 'Point1_Upperleft.co2_value'])

    # Plotting the data with cleaned time values
    plt.figure(figsize=(14, 7))  # Increase figure size for better readability
    plt.plot(cleaned_data['Time'], cleaned_data['CO2 Concentration @1.10m '], color='blue', label='$CO2_{ST}$')
    plt.plot(cleaned_data['Time'], cleaned_data['Point1_Upperleft.co2_value'], color='green', label='$CO2_{CDSK}$')

    # Labels and legend
    plt.xlabel('Time (HH:MM)')
    plt.ylabel('CO2 Concentration (ppm)')
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
    plot_co2_concentration(file_path)
else:
    print("No file selected.")
