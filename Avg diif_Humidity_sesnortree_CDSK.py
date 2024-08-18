import pandas as pd

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
file1_filtered = file1_filtered.dropna(subset=['Humidity @1.10m (UID: TxR)'])
file2_filtered = file2_filtered.dropna(subset=['Point2_Upperleft.rh_value'])

# Calculate the average humidity for each source
average_humidity_1_10m = file1_filtered['Humidity @1.10m (UID: TxR)'].mean()
average_humidity_point2_upperleft = file2_filtered['Point2_Upperleft.rh_value'].mean()

# Calculate the difference
average_difference_humidity = average_humidity_1_10m - average_humidity_point2_upperleft

# Output the results
print(f"Average Humidity at 1.10m: {average_humidity_1_10m:.2f}%")
print(f"Average Humidity at Point2 Upperleft: {average_humidity_point2_upperleft:.2f}%")
print(f"Average Difference in Humidity: {average_difference_humidity:.2f}%")
