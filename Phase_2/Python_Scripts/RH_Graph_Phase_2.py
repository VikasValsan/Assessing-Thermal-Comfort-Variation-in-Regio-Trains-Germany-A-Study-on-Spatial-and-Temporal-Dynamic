import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def perform_regression_analysis(file_path):
    # Load the dataset with the correct header row (A1 corresponds to header=0 in pandas)
    data = pd.read_excel(file_path, header=0)

    # Print column names to verify they match what you expect
    print("Available columns:", data.columns)

    # Ensure the relevant columns are numeric and handle any missing values
    data['Relative Humidity @1.10m '] = pd.to_numeric(data['Relative Humidity @1.10m '], errors='coerce')
    data['Point1_Upperleft.rh_value'] = pd.to_numeric(data['Point1_Upperleft.rh_value'], errors='coerce')

    # Drop rows with NaN values
    cleaned_data = data.dropna(subset=['Relative Humidity @1.10m ', 'Point1_Upperleft.rh_value'])

    # Prepare data for regression
    X = cleaned_data['Relative Humidity @1.10m '].values.reshape(-1, 1)
    y = cleaned_data['Point1_Upperleft.rh_value'].values

    # Perform linear regression
    linear_model = LinearRegression()
    linear_model.fit(X, y)
    y_pred_linear = linear_model.predict(X)
    r_squared_linear = r2_score(y, y_pred_linear)

    # Perform polynomial regression (degree 2)
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)
    poly_model = LinearRegression()
    poly_model.fit(X_poly, y)
    y_pred_poly = poly_model.predict(X_poly)
    r_squared_poly = r2_score(y, y_pred_poly)

    # Plotting the linear regression line along with the data points
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', label='Data points')
    plt.plot(X, y_pred_linear, color='red', label=f'Linear Regression (R² = {r_squared_linear:.2f})')
    plt.xlabel('Relative Humidity @1.10m ')
    plt.ylabel('Point1_Upperleft.rh_value')
    plt.title('Linear Regression Analysis')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Plotting the polynomial regression line along with the data points
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', label='Data points')
    plt.plot(X, y_pred_poly, color='green', label=f'Polynomial Regression (R² = {r_squared_poly:.2f})')
    plt.xlabel('Relative Humidity @1.10m ')
    plt.ylabel('Point1_Upperleft.rh_value')
    plt.title('Polynomial Regression Analysis (Degree 2)')
    plt.legend()
    plt.tight_layout()
    plt.show()

def select_file():
    Tk().withdraw()  # Hide the root window
    file_path = askopenfilename(title="Select the dataset file", filetypes=[("Excel files", "*.xlsx *.xls")])
    return file_path

# Usage example
file_path = select_file()
if file_path:
    perform_regression_analysis(file_path)
else:
    print("No file selected.")
