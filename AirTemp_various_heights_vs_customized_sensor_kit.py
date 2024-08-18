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
file1_filtered = file1_filtered.dropna(subset=['Air Temp @0.10m (UID: TB)', 'Air Temp @1.10m (UID: TA)', 'Air Temp @1.70m (UID: TK)'])
file2_filtered = file2_filtered.dropna(subset=['Point2_Upperleft.t_db_value'])

# Plot the data
plt.figure(figsize=(12, 6))

# Plot from file1 (multiple heights) with specified colors
plt.plot(file1_filtered['Datetime'], file1_filtered['Air Temp @0.10m (UID: TB)'], label='Air Temp @0.10m', color='yellow')
plt.plot(file1_filtered['Datetime'], file1_filtered['Air Temp @1.10m (UID: TA)'], label='Air Temp @1.10m', color='red')
plt.plot(file1_filtered['Datetime'], file1_filtered['Air Temp @1.70m (UID: TK)'], label='Air Temp @1.70m', color='blue')

# Plot from file2
plt.plot(file2_filtered['timestamp'], file2_filtered['Point2_Upperleft.t_db_value'], label='Point2 Upperleft.t_db_value', linestyle='--')

# Formatting the plot
plt.title('Air Temperature Comparison: Sensor Tree vs. Custom Developed Sensor Kit')
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')

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
