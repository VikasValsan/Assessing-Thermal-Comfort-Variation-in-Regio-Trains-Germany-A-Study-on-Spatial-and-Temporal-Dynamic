import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def load_dataset(prompt):
    """Function to load a dataset using a file dialog, with the second row as the header."""
    Tk().withdraw()  # Hide the main tkinter window
    print(prompt)
    file_path = askopenfilename()  # Open file dialog to select a file
    if file_path:
        # Load the data using the second row (index 1) as the header
        return pd.read_excel(file_path, header=1)
    else:
        print("No file selected.")
        return None


def perform_polynomial_analysis(data, independent_var, dependent_var, degree=2):
    """Function to perform polynomial regression analysis and generate plots."""
    # Clean the data
    data.columns = data.columns.str.strip()  # Strip any leading/trailing spaces from column names

    if independent_var not in data.columns or dependent_var not in data.columns:
        print(f"Column not found: {independent_var} or {dependent_var}")
        return None

    # Convert columns to numeric and inspect the first few rows
    data[independent_var] = pd.to_numeric(data[independent_var], errors='coerce')
    data[dependent_var] = pd.to_numeric(data[dependent_var], errors='coerce')

    # Drop rows with missing values in these columns
    clean_data = data.dropna(subset=[independent_var, dependent_var])
    if clean_data.empty:
        print(f"No valid data found for {independent_var} and {dependent_var} after cleaning.")
        return None

    # Prepare the independent and dependent variables
    X = clean_data[[independent_var]].values.reshape(-1, 1)
    y = clean_data[dependent_var].values

    # Polynomial Regression (degree 2)
    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)
    poly_reg = LinearRegression()
    poly_reg.fit(X_poly, y)
    y_poly_pred = poly_reg.predict(X_poly)
    r2_poly = r2_score(y, y_poly_pred)

    # Extract the polynomial coefficients for the regression equation
    coefs = poly_reg.coef_
    intercept = poly_reg.intercept_

    # Construct the polynomial equation as a string
    equation_terms = [f"{intercept:.4f}"]
    for i in range(1, len(coefs)):
        equation_terms.append(f"{coefs[i]:+.4f} * x^{i}")
    equation = " + ".join(equation_terms)

    # Print the regression equation
    print(f"Regression equation for {independent_var} vs {dependent_var}:")
    print(f"y = {equation}")

    # Plotting the polynomial regression result
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', label='Data points')
    plt.plot(X, y_poly_pred, color='green', label=f'Polynomial Regression (R² = {r2_poly:.2f})')
    plt.title(f'Polynomial Regression Analysis: {independent_var}')
    plt.xlabel(f'{independent_var} - Sensor Tree')
    plt.ylabel(f'{dependent_var} - Enclosed Sensor Kit')
    plt.legend()
    plt.grid(True)
    plt.show()

    return r2_poly


def main():
    # Load the Lab dataset
    lab_data = load_dataset("Select the Lab_Experiment dataset")

    # Ensure the dataset is loaded before proceeding
    if lab_data is not None:
        # Define the variable pairs
        variable_pairs_lab = [
            ("Air Temp @1.10m", "Air Temp"),
            ("Air Temp @1.70m", "Air Temp"),
            ("Air Temp @0.10m", "Air Temp"),
            ("CO2 Concentration @1.10m", "CO2 Concentartion"),
            ("Relative Humidity @1.10m", "Relative Humidity"),
            ("Operative Temperature @1.10m", "Operative Temperature"),
            ("Operative Temperature @0.10m", "Operative Temperature"),
            ("Operative Temperature @1.70m", "Operative Temperature")
        ]

        # Perform polynomial regression analysis for each variable pair
        for independent_var, dependent_var in variable_pairs_lab:
            print(f"\nAnalyzing {independent_var} vs {dependent_var} in Lab Environment...")
            r2_poly = perform_polynomial_analysis(lab_data, independent_var, dependent_var, degree=2)
            if r2_poly is not None:
                print(f"Polynomial R² value for {independent_var} vs {dependent_var}: {r2_poly:.4f}")
    else:
        print("Please make sure the dataset is selected and loaded correctly.")


if __name__ == "__main__":
    main()
