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
file1_filtered = file1_filtered.dropna(subset=['Air Temp @0.10m (UID: TB)', 'Air Temp @1.10m (UID: TA)', 'Air Temp @1.70m (UID: TK)'])
file2_filtered = file2_filtered.dropna(subset=['Point2_Upperleft.t_db_value'])

# Calculate the average temperature for each height in file1 and for Point2 Upperleft in file2
average_temp_0_10m = file1_filtered['Air Temp @0.10m (UID: TB)'].mean()
average_temp_1_10m = file1_filtered['Air Temp @1.10m (UID: TA)'].mean()
average_temp_1_70m = file1_filtered['Air Temp @1.70m (UID: TK)'].mean()
average_temp_point2_upperleft = file2_filtered['Point2_Upperleft.t_db_value'].mean()

# Calculate the differences
difference_0_10m = average_temp_0_10m - average_temp_point2_upperleft
difference_1_10m = average_temp_1_10m - average_temp_point2_upperleft
difference_1_70m = average_temp_1_70m - average_temp_point2_upperleft

# Output the results
print(f"Average Temperature at 0.10m: {average_temp_0_10m:.2f}°C")
print(f"Average Temperature at 1.10m: {average_temp_1_10m:.2f}°C")
print(f"Average Temperature at 1.70m: {average_temp_1_70m:.2f}°C")
print(f"Average Temperature at Point2 Upperleft: {average_temp_point2_upperleft:.2f}°C")
print()
print(f"Difference at 0.10m: {difference_0_10m:.2f}°C")
print(f"Difference at 1.10m: {difference_1_10m:.2f}°C")
print(f"Difference at 1.70m: {difference_1_70m:.2f}°C")
