import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def plot_air_temperature(file_path):
    # Load the dataset with the correct header row
    data = pd.read_excel(file_path, header=1)  # Header is in the second row (A2:T2)

    # Convert the datetime column to proper datetime format
    data['Time'] = pd.to_datetime(data['Datetime'], errors='coerce').dt.strftime('%H:%M')

    # Ensure all relevant columns are numeric and handle any missing values
    data['Air Temp'] = pd.to_numeric(data['Air Temp'], errors='coerce')
    data['Air Temp @1.10m'] = pd.to_numeric(data['Air Temp @1.10m'], errors='coerce')
    data['Air Temp @0.10m'] = pd.to_numeric(data['Air Temp @0.10m'], errors='coerce')
    data['Air Temp @1.70m'] = pd.to_numeric(data['Air Temp @1.70m'], errors='coerce')

    # Plotting Air Temperature at various heights on the same graph
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotting each series with distinctive colors and updated labels
    ax.plot(data['Time'], data['Air Temp'], label='$ta_{ESK}$', color='blue')
    ax.plot(data['Time'], data['Air Temp @1.10m'], label='$ta_{ST @1.10m}$', color='green')
    ax.plot(data['Time'], data['Air Temp @0.10m'], label='$ta_{ST @0.10m}$', color='orange')
    ax.plot(data['Time'], data['Air Temp @1.70m'], label='$ta_{ST @1.70m}$', color='purple')

    # Labels and no title
    ax.set_xlabel('Time (HH:MM)')
    ax.set_ylabel('Air Temperature (°C)')

    # Legend with updated names
    ax.legend()

    # Adjust x-axis to prevent overlap
    plt.xticks(rotation=90)

    # Reduce the number of x-ticks for clarity
    ax.set_xticks(ax.get_xticks()[::10])

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
