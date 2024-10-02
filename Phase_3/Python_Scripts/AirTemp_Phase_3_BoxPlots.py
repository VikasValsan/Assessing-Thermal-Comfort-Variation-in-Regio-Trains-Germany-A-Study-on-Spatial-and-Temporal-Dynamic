import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Function to calculate Interior Temperature threshold (Tic,0) based on outside temperature (Tem)
def calculate_tic_threshold(temp):
    if temp <= 22.5:
        return 22
    elif 22.5 < temp <= 35:
        return 22 + 0.4 * (temp - 22.5)
    else:
        return 27

# Create a file dialog to select the dataset
Tk().withdraw()  # Prevent the Tk window from appearing
file_path = askopenfilename(title="Select the Excel file with the sensor data",
                            filetypes=[("Excel files", "*.xlsx *.xls")])

# Load the dataset
df = pd.read_excel(file_path)

# Ensure proper datetime handling and filtering
df['Datetime'] = pd.to_datetime(df['Datetime'])
filtered_df = df[(df['Datetime'] >= '2024-06-27') & (df['Datetime'] <= '2024-07-19')]

# Extract necessary columns for the upper and lower decks (Temperature and Outside Temp)
upper_deck_columns_temp = ['Datetime', 'Point1_Upperleft.t_db_value', 'Point1_Upperright.t_db_value',
                           'Point2_Upperleft.t_db_value', 'Point2_Upperright.t_db_value',
                           'HVAC_OutsideTemp_value']

lower_deck_columns_temp = ['Datetime', 'Point1_Lowerleft.t_db_value', 'Point1_Lowerright.t_db_value',
                           'Point2_Lowerleft.t_db_value', 'Point2_Lowerright.t_db_value',
                           'HVAC_OutsideTemp_value']

upper_deck_temp_df = filtered_df[upper_deck_columns_temp].copy()
lower_deck_temp_df = filtered_df[lower_deck_columns_temp].copy()

# Apply the Interior Temperature threshold calculation to both decks
upper_deck_temp_df['Tic_Threshold'] = upper_deck_temp_df['HVAC_OutsideTemp_value'].apply(calculate_tic_threshold)
lower_deck_temp_df['Tic_Threshold'] = lower_deck_temp_df['HVAC_OutsideTemp_value'].apply(calculate_tic_threshold)

# Sensor columns for upper and lower decks
sensor_columns_upper_temp = ['Point1_Upperleft.t_db_value', 'Point1_Upperright.t_db_value']
sensor_columns_lower_temp = ['Point1_Lowerleft.t_db_value', 'Point1_Lowerright.t_db_value']
sensor_columns_upper_temp_2 = ['Point2_Upperleft.t_db_value', 'Point2_Upperright.t_db_value']
sensor_columns_lower_temp_2 = ['Point2_Lowerleft.t_db_value', 'Point2_Lowerright.t_db_value']

# Function to create the time-based box plots for Temperature data with customized styling and no outliers
def create_temp_boxplots(deck_df, sensor_columns, deck_name):
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # Adjusted figsize for side-by-side plots
    fig.suptitle(f'Temperature Variation for {deck_name} Sensors', fontsize=16,
                 y=0.98)  # Adjusted y to bring title within plot area

    for i, col in enumerate(sensor_columns):
        ax = axes[i]
        bp = ax.boxplot([deck_df[deck_df['Datetime'].dt.strftime('%d.%m.%y') == date][col].dropna()
                         for date in deck_df['Datetime'].dt.strftime('%d.%m.%y').unique()],
                        patch_artist=True, boxprops=dict(facecolor="lightblue", color="blue"),
                        capprops=dict(color="blue"),
                        whiskerprops=dict(color="blue"),
                        flierprops=dict(marker='o', color='blue', alpha=0.5),
                        medianprops=dict(color="red"), showfliers=False)  # Outliers removed by setting showfliers=False

        # Set the color for the box edges
        for box in bp['boxes']:
            box.set_edgecolor('blue')
            box.set_linewidth(1.5)

        # Plot the threshold line and outside temperature on top of the box plot
        ax.plot(deck_df['Datetime'].dt.strftime('%d.%m.%y').unique(),
                deck_df.groupby(deck_df['Datetime'].dt.date)['Tic_Threshold'].mean(),
                'g--', label='Tic threshold as per EN 14750-1', zorder=10)
        ax.plot(deck_df['Datetime'].dt.strftime('%d.%m.%y').unique(),
                deck_df.groupby(deck_df['Datetime'].dt.date)['HVAC_OutsideTemp_value'].mean(),
                'r--', label='Outside Temperature', zorder=5)

        ax.set_title(f'Temperature Variation CDSK - {col}', fontsize=12)
        ax.set_xlabel('Date (DD.MM.YY)', fontsize=10)
        ax.set_ylabel('Temperature (°C)', fontsize=10)
        ax.set_ylim(16, 35)
        ax.set_xticklabels(deck_df['Datetime'].dt.strftime('%d.%m.%y').unique(), rotation=45, ha='right')
        ax.grid(True)

    # Adjust layout with specified values
    plt.subplots_adjust(top=0.845, bottom=0.155, left=0.04, right=0.97, hspace=0.2, wspace=0.12)

    # Add the legend only once
    fig.legend([plt.Line2D([0], [0], color='r', lw=2, linestyle='--'),
                plt.Line2D([0], [0], color='g', lw=2, linestyle='--')],
               ['Outside Temperature', 'Tic threshold as per EN 14750-1'],
               loc='upper right', bbox_to_anchor=(1, 1), fontsize=12)  # Adjusted legend color and position

    plt.show()

# Create the time-based boxplots for Upper Deck (First Pair)
create_temp_boxplots(upper_deck_temp_df, sensor_columns_upper_temp, "Upper Deck")

# Create the time-based boxplots for Upper Deck (Second Pair)
create_temp_boxplots(upper_deck_temp_df, sensor_columns_upper_temp_2, "Upper Deck")

# Create the time-based boxplots for Lower Deck (First Pair)
create_temp_boxplots(lower_deck_temp_df, sensor_columns_lower_temp, "Lower Deck")

# Create the time-based boxplots for Lower Deck (Second Pair)
create_temp_boxplots(lower_deck_temp_df, sensor_columns_lower_temp_2, "Lower Deck")
