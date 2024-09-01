import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename


# Function to calculate Relative Humidity threshold based on interior temperature
def calculate_rh_threshold(temp):
    if temp <= 22.5:
        return 75
    else:
        return 75 - 3 * (temp - 22.5)


# Create a file dialog to select the dataset
Tk().withdraw()  # Prevent the Tk window from appearing
file_path = askopenfilename(title="Select the Excel file with the sensor data",
                            filetypes=[("Excel files", "*.xlsx *.xls")])

# Load the dataset
df = pd.read_excel(file_path)

# Ensure proper datetime handling and filtering
df['Datetime'] = pd.to_datetime(df['Datetime'])
filtered_df = df[(df['Datetime'] >= '2024-06-27') & (df['Datetime'] <= '2024-07-19')]

# Extract necessary columns for the upper and lower decks (Relative Humidity and Interior Temp)
upper_deck_columns_rh = ['Datetime', 'Point1_Upperleft.rh_value', 'Point1_Upperright.rh_value',
                         'Point2_Upperleft.rh_value', 'Point2_Upperright.rh_value',
                         'Point1_Upperleft.t_db_value', 'Point1_Upperright.t_db_value',
                         'Point2_Upperleft.t_db_value', 'Point2_Upperright.t_db_value']

lower_deck_columns_rh = ['Datetime', 'Point1_Lowerleft.rh_value', 'Point1_Lowerright.rh_value',
                         'Point2_Lowerleft.rh_value', 'Point2_Lowerright.rh_value',
                         'Point1_Lowerleft.t_db_value', 'Point1_Lowerright.t_db_value',
                         'Point2_Lowerleft.t_db_value', 'Point2_Lowerright.t_db_value']

upper_deck_rh_df = filtered_df[upper_deck_columns_rh].copy()
lower_deck_rh_df = filtered_df[lower_deck_columns_rh].copy()

# Calculate the mean interior temperature for each deck
upper_deck_rh_df['Mean_Interior_Temperature'] = upper_deck_rh_df[['Point1_Upperleft.t_db_value',
                                                                  'Point1_Upperright.t_db_value',
                                                                  'Point2_Upperleft.t_db_value',
                                                                  'Point2_Upperright.t_db_value']].mean(axis=1)

lower_deck_rh_df['Mean_Interior_Temperature'] = lower_deck_rh_df[['Point1_Lowerleft.t_db_value',
                                                                  'Point1_Lowerright.t_db_value',
                                                                  'Point2_Lowerleft.t_db_value',
                                                                  'Point2_Lowerright.t_db_value']].mean(axis=1)

# Apply the RH threshold calculation to both decks
upper_deck_rh_df['RH_Threshold'] = upper_deck_rh_df['Mean_Interior_Temperature'].apply(calculate_rh_threshold)
lower_deck_rh_df['RH_Threshold'] = lower_deck_rh_df['Mean_Interior_Temperature'].apply(calculate_rh_threshold)

# Sensor columns for upper and lower decks
sensor_columns_upper_rh = ['Point1_Upperleft.rh_value', 'Point1_Upperright.rh_value',
                           'Point2_Upperleft.rh_value', 'Point2_Upperright.rh_value']

sensor_columns_lower_rh = ['Point1_Lowerleft.rh_value', 'Point1_Lowerright.rh_value',
                           'Point2_Lowerleft.rh_value', 'Point2_Lowerright.rh_value']


# Function to create the time-based box plots for Relative Humidity data with customized styling
def create_rh_boxplots(deck_df, sensor_columns, deck_name):
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))  # Adjusted layout to 1x2 and figsize
    fig.suptitle(f'Relative Humidity Variation for {deck_name} Sensors', fontsize=16,
                 y=0.98)  # Adjusted y to bring title within plot area

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

        # Plot the RH threshold line on top of the box plot
        ax.plot(deck_df['Datetime'].dt.strftime('%d.%m.%y').unique(),
                deck_df.groupby(deck_df['Datetime'].dt.strftime('%d.%m.%y'))['RH_Threshold'].mean(),
                'g--', label='RH threshold as per EN 14750-1', zorder=10)

        ax.set_title(f'RH Variation CDSK - {col}', fontsize=12)
        ax.set_xlabel('Date (DD.MM.YY)', fontsize=10)
        ax.set_ylabel('Relative Humidity (%)', fontsize=10)
        ax.set_ylim(20, 100)
        ax.set_xticklabels(deck_df['Datetime'].dt.strftime('%d.%m.%y').unique(), rotation=45, ha='right')
        ax.grid(True)

    # Adjust layout to match specified layout parameters
    plt.subplots_adjust(top=0.88, bottom=0.11, left=0.05, right=0.98, hspace=0.3, wspace=0.3)

    # Add a single legend for the entire figure
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right', fontsize=12, bbox_to_anchor=(1, 1))

    plt.tight_layout(rect=[0, 0, 1, 0.95], pad=2.0)  # Additional layout adjustment
    plt.show()


# Create the time-based boxplots for Upper Deck with the new 1x2 layout
create_rh_boxplots(upper_deck_rh_df, sensor_columns_upper_rh[:2], "Upper Deck - Point 1")
create_rh_boxplots(upper_deck_rh_df, sensor_columns_upper_rh[2:], "Upper Deck - Point 2")

# Create the time-based boxplots for Lower Deck with the new 1x2 layout
create_rh_boxplots(lower_deck_rh_df, sensor_columns_lower_rh[:2], "Lower Deck - Point 1")
create_rh_boxplots(lower_deck_rh_df, sensor_columns_lower_rh[2:], "Lower Deck - Point 2")
