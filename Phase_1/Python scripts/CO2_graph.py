import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def plot_co2_concentration(file_path):
    # Load the dataset with the correct header row
    data = pd.read_excel(file_path, header=1)  # Header is in the second row (A2:T2)

    # Convert the datetime column to proper datetime format
    data['Time'] = pd.to_datetime(data['Datetime'], errors='coerce').dt.strftime('%H:%M')

    # Plotting both CO2 Concentration and CO2 Concentration @1.10m on the same graph
    fig, ax = plt.subplots(figsize=(10, 6))

    try:
        # Plotting both series with updated labels
        ax.plot(data['Time'], data['CO2 Concentartion'], label='$CO2_{ESK}$', color='yellow')
        ax.plot(data['Time'], data['CO2 Concentration @1.10m'], label='$CO2_{ST}$', color='red')

        # Labels and no title
        ax.set_xlabel('Time (HH:MM)')
        ax.set_ylabel('CO2 Concentration (ppm)')

        # Legend with updated names
        ax.legend()

        # Adjust x-axis to prevent overlap
        plt.xticks(rotation=90)

        # Reduce the number of x-ticks for clarity
        ax.set_xticks(ax.get_xticks()[::10])

        plt.tight_layout()
        plt.show()
    except KeyError as e:
        print(f"Error: Could not find one of the expected columns: {e}")

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
