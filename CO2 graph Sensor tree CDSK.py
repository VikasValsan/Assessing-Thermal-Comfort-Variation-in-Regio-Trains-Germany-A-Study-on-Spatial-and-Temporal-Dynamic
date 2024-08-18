import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Paths to the CSV files (update these paths to your local file paths)
file1_path = 'path/to/your/Adjusted_SLBox_DB_mobiletestunit_240801-Magdeburg-Schönenbeck.csv'
file2_path = 'path/to/your/Train_data_clean_channel_data_cet_v2.csv'

# Load the CSV files
file1_df = pd.read_csv(file1_path, delimiter=';', parse_dates=['Datetime'], dayfirst=True)
file2_df = pd.read_csv(file2_path, delimiter=';', parse_dates=['timestamp'], dayfirst=True)

# Define the time range
start_time = '2024-08-01 13:52'
end_time = '2024-08-01 17:12'

# Filter data based on the time range
file1_filtered = file1_df[(file1_df['Datetime'] >= start_time) & (file1_df['Datetime'] <= end_time)]
file2_filtered = file2_df[(file2_df['timestamp'] >= start_time) & (file2_df['timestamp'] <= end_time)]

# Drop rows with NaN values for the relevant columns
file1_filtered = file1_filtered.dropna(subset=['CO2 Concentration @1.10m (UID: 29r5)'])
file2_filtered = file2_filtered.dropna(subset=['Point2_Upperleft.co2_value'])

# Plot the data for CO2 Concentration
plt.figure(figsize=(12, 6))

# Plot from file1 (CO2 Concentration @1.10m)
plt.plot(file1_filtered['Datetime'], file1_filtered['CO2 Concentration @1.10m (UID: 29r5)'], label='CO2 Concentration @1.10m', color='green')

# Plot from file2 (Point2 Upperleft)
plt.plot(file2_filtered['timestamp'], file2_filtered['Point2_Upperleft.co2_value'], label='Point2 Upperleft.co2_value', linestyle='--', color='orange')

# Formatting the plot
plt.title('CO2 Concentration Comparison: Sensor Tree vs. Custom Developed Sensor Kit')
plt.xlabel('Time')
plt.ylabel('CO2 Concentration (ppm)')

# Set the x-axis major formatter to display time in HH:MM format
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45)
plt.xlim(pd.Timestamp('2024-08-01 13:50:00'), pd.Timestamp('2024-08-01 17:15:00'))

# Move legend outside the plot area to the top right
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()
