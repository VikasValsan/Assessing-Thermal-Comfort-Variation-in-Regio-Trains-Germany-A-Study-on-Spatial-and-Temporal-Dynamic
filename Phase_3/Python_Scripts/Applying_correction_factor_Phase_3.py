import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Correction factors provided
correction_factors = {
    'AirTemp_1.10m': 0.000,
    'CO2_1.10m': -0.5045,
    'OperativeTemp_1.10m': 0.0000,
    'RH_1.10m': -0.000
}

# Suffixes corresponding to the data columns
suffixes = {
    'AirTemp': '.t_db_value',
    'CO2': '.co2_value',
    'OperativeTemp': '.to_value',
    'RH': '.rh_value'
}

# Function to select file and load the data
def select_file():
    Tk().withdraw()  # Hide the root window
    file_path = askopenfilename(title="Select the Excel file with your data")
    return pd.read_excel(file_path)

# Step 1: Select and load the dataset
data = select_file()

# Step 2: Apply the correction factors to the relevant columns
for key, suffix in suffixes.items():
    # Find columns that match the suffix
    matching_columns = [col for col in data.columns if col.endswith(suffix)]
    if matching_columns:
        for col in matching_columns:
            # Apply the correction factor
            if key in correction_factors:
                correction_factor = correction_factors[key]
                data[col] = data[col] + correction_factor
                print(f"Applied correction factor {correction_factor} to column {col}")

# Step 3: Save the corrected dataset
save_path = asksaveasfilename(title="Save the corrected dataset as", defaultextension=".xlsx")
if save_path:
    data.to_excel(save_path, index=False)
    print(f"Corrected data has been saved to {save_path}")
else:
    print("Save operation was cancelled.")
