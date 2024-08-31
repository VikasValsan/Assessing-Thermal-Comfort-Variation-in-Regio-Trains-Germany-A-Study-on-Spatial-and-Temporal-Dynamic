import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def plot_operative_temperature(file_path):
    # Load the dataset with the correct header row
    data = pd.read_excel(file_path, header=1)  # Adjust header as needed

    # Print out column names for debugging
    print("Column names in the dataset:", data.columns)

    # Identify the correct datetime column name
    datetime_col = None
    for col in data.columns:
        if 'datetime' in col.lower():  # This checks for variations like 'Datetime', 'DateTime', etc.
            datetime_col = col
            break

    if datetime_col is None:
        print("Error: No 'Datetime' column found.")
        return

    # Convert the identified datetime column to proper datetime format
    data['Time'] = pd.to_datetime(data[datetime_col], errors='coerce')

    # Handle any NaT values by dropping them or filling them
    data = data.dropna(subset=['Time'])  # Drop rows where 'Time' could not be parsed

    # Convert the time to string format for plotting
    data['Time'] = data['Time'].dt.strftime('%H:%M')

    # Ensure all relevant columns are numeric and handle any missing values
    data['Operative Temperature'] = pd.to_numeric(data['Operative Temperature'], errors='coerce')
    data['Operative Temperature @1.10m'] = pd.to_numeric(data['Operative Temperature @1.10m'], errors='coerce')
    data['Operative Temperature @0.10m'] = pd.to_numeric(data['Operative Temperature @0.10m'], errors='coerce')
    data['Operative Temperature @1.70m'] = pd.to_numeric(data['Operative Temperature @1.70m'], errors='coerce')

    # Plotting Operative Temperature at various heights on the same graph
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotting each series with distinctive colors and updated labels
    ax.plot(data['Time'], data['Operative Temperature'], label='$To_{ESK}$', color='blue')
    ax.plot(data['Time'], data['Operative Temperature @1.10m'], label='$To_{ST @1.10m}$', color='green')
    ax.plot(data['Time'], data['Operative Temperature @0.10m'], label='$To_{ST @0.10m}$', color='orange')
    ax.plot(data['Time'], data['Operative Temperature @1.70m'], label='$To_{ST @1.70m}$', color='purple')

    # Labels and no title
    ax.set_xlabel('Time (HH:MM)')
    ax.set_ylabel('Operative Temperature (°C)')

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
    plot_operative_temperature(file_path)
else:
    print("No file selected.")
