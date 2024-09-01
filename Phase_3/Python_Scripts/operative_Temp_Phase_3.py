import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Create a file dialog to select the dataset
Tk().withdraw()  # Prevent the Tk window from appearing
file_path = askopenfilename(title="Select the Excel file with the sensor data",
                            filetypes=[("Excel files", "*.xlsx *.xls")])

# Load the dataset
df = pd.read_excel(file_path)

# Ensure proper datetime handling and filtering
df['Datetime'] = pd.to_datetime(df['Datetime'])
filtered_df = df[(df['Datetime'] >= '2024-06-27') & (df['Datetime'] <= '2024-07-19')]

# Extract necessary columns for the upper and lower decks (Operative Temperature)
upper_deck_columns_t_o = ['Datetime', 'Point1_Upperleft.to_value', 'Point1_Upperright.to_value',
                          'Point2_Upperleft.to_value', 'Point2_Upperright.to_value']

lower_deck_columns_t_o = ['Datetime', 'Point1_Lowerleft.to_value', 'Point1_Lowerright.to_value',
                          'Point2_Lowerleft.to_value', 'Point2_Lowerright.to_value']

upper_deck_t_o_df = filtered_df[upper_deck_columns_t_o].copy()
lower_deck_t_o_df = filtered_df[lower_deck_columns_t_o].copy()

# Sensor columns for upper and lower decks
sensor_columns_upper_t_o = ['Point1_Upperleft.to_value', 'Point1_Upperright.to_value',
                            'Point2_Upperleft.to_value', 'Point2_Upperright.to_value']

sensor_columns_lower_t_o = ['Point1_Lowerleft.to_value', 'Point1_Lowerright.to_value',
                            'Point2_Lowerleft.to_value', 'Point2_Lowerright.to_value']

# Function to create the time-based box plots for Operative Temperature data with customization options
def create_t_o_boxplots(deck_df, sensor_columns, deck_name, y_axis_range=(18, 30)):
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))  # Adjusted figsize and layout to 1x2
    fig.suptitle(f'Operative Temperature Variation for {deck_name} Sensors', fontsize=16, y=0.98)

    for i, col in enumerate(sensor_columns):
        ax = axes[i % 2]  # Adjusted index to fit 1x2 layout
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

        ax.set_title(f'Operative Temperature Variation - {col}', fontsize=12)
        ax.set_xlabel('Date (DD.MM.YY)', fontsize=10)
        ax.set_ylabel('Temperature (°C)', fontsize=10)
        ax.set_ylim(y_axis_range)  # Adjust the y-axis range
        ax.set_xticklabels(deck_df['Datetime'].dt.strftime('%d.%m.%y').unique(), rotation=45, ha='right')
        ax.grid(True)

    # Adjust layout to match specified layout parameters
    plt.subplots_adjust(top=0.88, bottom=0.11, left=0.05, right=0.98, hspace=0.3, wspace=0.3)
    plt.tight_layout(rect=[0, 0, 1, 0.95], pad=2.0)  # Additional layout adjustment
    plt.show()

# Create the time-based boxplots for Upper Deck with the new 1x2 layout
create_t_o_boxplots(upper_deck_t_o_df, sensor_columns_upper_t_o[:2], "Upper Deck - Point 1", y_axis_range=(18, 30))
create_t_o_boxplots(upper_deck_t_o_df, sensor_columns_upper_t_o[2:], "Upper Deck - Point 2", y_axis_range=(18, 30))

# Create the time-based boxplots for Lower Deck with the new 1x2 layout
create_t_o_boxplots(lower_deck_t_o_df, sensor_columns_lower_t_o[:2], "Lower Deck - Point 1", y_axis_range=(18, 30))
create_t_o_boxplots(lower_deck_t_o_df, sensor_columns_lower_t_o[2:], "Lower Deck - Point 2", y_axis_range=(18, 30))
