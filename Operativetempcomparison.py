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
file1_filtered = file1_filtered.dropna(subset=['Air Temp @0.10m ', 'Air Temp @1.10m', 'Air Temp @1.70m ',
                                               'Globe Temp @0.10m ', 'Globe Temp @1.10m', 'Globe Temp @1.70m '])
file2_filtered = file2_filtered.dropna(subset=['Point2_Upperleft.t_db_value', 'Point2_Upperleft.t_ir_value'])

# Calculate operative temperature for the first file
file2_filtered['Operative Temperature'] = (file2_filtered['Point2_Upperleft.t_db_value'] + file2_filtered['Point2_Upperleft.t_ir_value']) / 2

# Calculate operative temperature for the second file at different heights
file1_filtered['Operative Temp @0.10m'] = (file1_filtered['Air Temp @0.10m '] + file1_filtered['Globe Temp @0.10m ']) / 2
file1_filtered['Operative Temp @1.10m'] = (file1_filtered['Air Temp @1.10m'] + file1_filtered['Globe Temp @1.10m']) / 2
file1_filtered['Operative Temp @1.70m'] = (file1_filtered['Air Temp @1.70m '] + file1_filtered['Globe Temp @1.70m ']) / 2

# Combine the data into a single DataFrame using a merge to align timestamps
merged_data = pd.merge_asof(file2_filtered[['timestamp', 'Operative Temperature']],
                            file1_filtered[['Datetime', 'Operative Temp @0.10m', 'Operative Temp @1.10m', 'Operative Temp @1.70m']],
                            left_on='timestamp', right_on='Datetime', direction='nearest')

# Rename the columns for clarity
merged_data.rename(columns={
    'timestamp': 'Datetime',
    'Operative Temperature': 'Operative Temp (Point2_Upperleft)'
}, inplace=True)

# Plot the data
plt.figure(figsize=(12, 6))

# Plot each series with the correct colors and labels
plt.plot(merged_data['Datetime'], merged_data['Operative Temp (Point2_Upperleft)'], color='yellow', label='Operative Temp (Point2 Upperleft)')
plt.plot(merged_data['Datetime'], merged_data['Operative Temp @0.10m'], color='red', label='Operative Temp @0.10m')
plt.plot(merged_data['Datetime'], merged_data['Operative Temp @1.10m'], color='blue', label='Operative Temp @1.10m')
plt.plot(merged_data['Datetime'], merged_data['Operative Temp @1.70m'], color='green', label='Operative Temp @1.70m')

# Add the legend
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc='upper left', bbox_to_anchor=(1, 1))

# Formatting the plot
plt.title('Operative Temperature vs. Time')
plt.xlabel('Time')
plt.ylabel('Operative Temperature (°C)')
plt.xticks(rotation=45)
plt.xlim(pd.Timestamp('2024-08-01 13:50:00'), pd.Timestamp('2024-08-01 17:15:00'))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Correct x-axis format
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()
