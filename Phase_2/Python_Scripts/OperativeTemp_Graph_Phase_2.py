import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def plot_operative_temperature(file_path):
    # Load the dataset with the correct header row (A2 corresponds to header=1 in pandas)
    data = pd.read_excel(file_path, header=1)  # Header is in the second row (A2:W2)

    # Ensure the relevant columns are numeric and handle any missing values
    data['Operative Temp @0.10m'] = pd.to_numeric(data['Operative Temp @0.10m'], errors='coerce')
    data['Operative Temp @1.10m'] = pd.to_numeric(data['Operative Temp @1.10m'], errors='coerce')
    data['Operative Temp @1.70m'] = pd.to_numeric(data['Operative Temp @1.70m'], errors='coerce')
    data['Operative Temperature(Point1_Upperleft.OperativeTemp_value)'] = pd.to_numeric(data['Operative Temperature(Point1_Upperleft.OperativeTemp_value)'], errors='coerce')

    # Convert the Datetime column to proper datetime format and extract time
    data['Time'] = pd.to_datetime(data['Datetime']).dt.strftime('%H:%M')

    # Drop rows with NaN values or 0 values in any of the Operative Temperature columns
    cleaned_data = data.dropna(subset=['Time', 'Operative Temp @0.10m', 'Operative Temp @1.10m', 'Operative Temp @1.70m', 'Operative Temperature(Point1_Upperleft.OperativeTemp_value)'])
    cleaned_data = cleaned_data[(cleaned_data['Operative Temp @0.10m'] != 0) &
                                (cleaned_data['Operative Temp @1.10m'] != 0) &
                                (cleaned_data['Operative Temp @1.70m'] != 0) &
                                (cleaned_data['Operative Temperature(Point1_Upperleft.OperativeTemp_value)'] != 0)]

    # Plotting the data with cleaned time values
    plt.figure(figsize=(14, 7))  # Increase figure size for better readability

    plt.plot(cleaned_data['Time'], cleaned_data['Operative Temp @0.10m'], color='red', label='To_ST 0.10m')
    plt.plot(cleaned_data['Time'], cleaned_data['Operative Temp @1.10m'], color='blue', label='To_ST 1.10m')
    plt.plot(cleaned_data['Time'], cleaned_data['Operative Temp @1.70m'], color='green', label='To_ST 1.70m')
    plt.plot(cleaned_data['Time'], cleaned_data['Operative Temperature(Point1_Upperleft.OperativeTemp_value)'], color='purple', label='To_CDSK')

    # Labels and legend
    plt.xlabel('Time (HH:MM)')
    plt.ylabel('Operative Temperature (°C)')
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
    plot_operative_temperature(file_path)
else:
    print("No file selected.")
