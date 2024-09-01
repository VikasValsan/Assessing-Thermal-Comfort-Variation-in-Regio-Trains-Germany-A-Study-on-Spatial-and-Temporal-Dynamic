import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Function to select file and load the data with column names from the second row
def select_file():
    Tk().withdraw()  # Hide the root window
    file_path = askopenfilename(title="Select the Excel file with your data")
    # Load the data and specify that the actual column names are in the second row (index 1)
    data = pd.read_excel(file_path, header=1)
    # Strip any leading or trailing spaces from the column names
    data.columns = data.columns.str.strip()
    return data

# Step 1: Select and load the dataset
data = select_file()

# Print the column names to confirm they have been cleaned
print("Cleaned column names in the dataset:")
print(data.columns)

# Define polynomial equations for each dependent variable
def poly_air_temp_0_10m(x):
    return -0.165409 * (x ** 2) + 8.487383 * x - 78.733409

def poly_air_temp_1_10m(x):
    return -0.447091 * (x ** 2) + 24.494095 * x - 305.284296

def poly_air_temp_1_70m(x):
    return 0.073449 * (x ** 2) - 4.044155 * x + 85.430480

def poly_co2_1_10m(x):
    return 0.000172 * (x ** 2) + 0.108930 * x + 304.175562

def poly_rh_1_10m(x):
    return -0.040443 * (x ** 2) + 3.107169 * x - 22.031575

def poly_operative_temp_0_10m(x):
    return -0.897043 * (x ** 2) + 45.522555 * x - 551.249185

def poly_operative_temp_1_10m(x):
    return -0.663952 * (x ** 2) + 36.071465 * x - 463.671701

def poly_operative_temp_1_70m(x):
    return -0.756209 * (x ** 2) + 42.590733 * x - 573.295724

# Example usage after confirming column names
# Adjust the following lines based on the actual column names you inspect
data['Air Temp @0.10m'] = pd.to_numeric(data['Air Temp @0.10m'], errors='coerce')
data['Air Temp @1.10m'] = pd.to_numeric(data['Air Temp @1.10m'], errors='coerce')
data['Air Temp @1.70m'] = pd.to_numeric(data['Air Temp @1.70m'], errors='coerce')
data['CO2 Concentration @1.10m'] = pd.to_numeric(data['CO2 Concentration @1.10m'], errors='coerce')
data['Relative Humidity @1.10m'] = pd.to_numeric(data['Relative Humidity @1.10m'], errors='coerce')
data['Operative Temp @0.10m'] = pd.to_numeric(data['Operative Temp @0.10m'], errors='coerce')
data['Operative Temp @1.10m'] = pd.to_numeric(data['Operative Temp @1.10m'], errors='coerce')
data['Operative Temp @1.70m'] = pd.to_numeric(data['Operative Temp @1.70m'], errors='coerce')
data['Air Temp (Point1_Upperleft.t_db_value)'] = pd.to_numeric(data['Air Temp (Point1_Upperleft.t_db_value)'], errors='coerce')
data['Relative Humidity (Point1_Upperleft.rh_value)'] = pd.to_numeric(data['Relative Humidity (Point1_Upperleft.rh_value)'], errors='coerce')
data['CO2(Point1_Upperleft.co2_value)'] = pd.to_numeric(data['CO2(Point1_Upperleft.co2_value)'], errors='coerce')
data['Operative Temperature(Point1_Upperleft.OperativeTemp_value)'] = pd.to_numeric(data['Operative Temperature(Point1_Upperleft.OperativeTemp_value)'], errors='coerce')

# Apply polynomial equations and calculate corrections
data['Predicted_AirTemp_0.10m'] = data['Air Temp @0.10m'].apply(poly_air_temp_0_10m)
data['Predicted_AirTemp_1.10m'] = data['Air Temp @1.10m'].apply(poly_air_temp_1_10m)
data['Predicted_AirTemp_1.70m'] = data['Air Temp @1.70m'].apply(poly_air_temp_1_70m)
data['Predicted_CO2_1.10m'] = data['CO2 Concentration @1.10m'].apply(poly_co2_1_10m)
data['Predicted_RH_1.10m'] = data['Relative Humidity @1.10m'].apply(poly_rh_1_10m)
data['Predicted_OperativeTemp_0.10m'] = data['Operative Temp @0.10m'].apply(poly_operative_temp_0_10m)
data['Predicted_OperativeTemp_1.10m'] = data['Operative Temp @1.10m'].apply(poly_operative_temp_1_10m)
data['Predicted_OperativeTemp_1.70m'] = data['Operative Temp @1.70m'].apply(poly_operative_temp_1_70m)

# Calculate differences between predicted and actual values
data['AirTemp_Correction_0.10m'] = data['Predicted_AirTemp_0.10m'] - data['Air Temp (Point1_Upperleft.t_db_value)']
data['AirTemp_Correction_1.10m'] = data['Predicted_AirTemp_1.10m'] - data['Air Temp (Point1_Upperleft.t_db_value)']
data['AirTemp_Correction_1.70m'] = data['Predicted_AirTemp_1.70m'] - data['Air Temp (Point1_Upperleft.t_db_value)']
data['CO2_Correction_1.10m'] = data['Predicted_CO2_1.10m'] - data['CO2(Point1_Upperleft.co2_value)']
data['RH_Correction_1.10m'] = data['Predicted_RH_1.10m'] - data['Relative Humidity (Point1_Upperleft.rh_value)']
data['OperativeTemp_Correction_0.10m'] = data['Predicted_OperativeTemp_0.10m'] - data['Operative Temperature(Point1_Upperleft.OperativeTemp_value)']
data['OperativeTemp_Correction_1.10m'] = data['Predicted_OperativeTemp_1.10m'] - data['Operative Temperature(Point1_Upperleft.OperativeTemp_value)']
data['OperativeTemp_Correction_1.70m'] = data['Predicted_OperativeTemp_1.70m'] - data['Operative Temperature(Point1_Upperleft.OperativeTemp_value)']

# Calculate average corrections
average_corrections = {
    'AirTemp_0.10m': data['AirTemp_Correction_0.10m'].mean(),
    'AirTemp_1.10m': data['AirTemp_Correction_1.10m'].mean(),
    'AirTemp_1.70m': data['AirTemp_Correction_1.70m'].mean(),
    'CO2_1.10m': data['CO2_Correction_1.10m'].mean(),
    'RH_1.10m': data['RH_Correction_1.10m'].mean(),
    'OperativeTemp_0.10m': data['OperativeTemp_Correction_0.10m'].mean(),
    'OperativeTemp_1.10m': data['OperativeTemp_Correction_1.10m'].mean(),
    'OperativeTemp_1.70m': data['OperativeTemp_Correction_1.70m'].mean(),
}

# Output the average correction factors
for key, value in average_corrections.items():
    print(f'Average Correction Factor for {key}: {value:.4f}')

# Ask the user to choose a location to save the corrected file
save_path = askopenfilename(title="Select the save location for the corrected dataset")
if save_path:
    corrected_file_path = save_path if save_path.endswith('.xlsx') else save_path + '.xlsx'
    data.to_excel(corrected_file_path, index=False)
    print(f'Corrected data has been saved to {corrected_file_path}')
else:
    print("Save operation was cancelled.")
