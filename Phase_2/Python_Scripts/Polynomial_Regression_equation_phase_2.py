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

    # Extracting the coefficients to form the polynomial equation
    coeffs = poly_reg.coef_
    intercept = poly_reg.intercept_
    equation = f"{coeffs[2]:.6f} * X^2 + {coeffs[1]:.6f} * X + {intercept:.6f}"

    # Display the polynomial equation
    print(f"\nPolynomial equation for {dependent_var} as a function of {independent_var}:")
    print(f"y = {equation}")

    # Plotting the polynomial regression result
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', label='Data points')
    plt.plot(X, y_poly_pred, color='green', label=f'Polynomial Regression (R² = {r2_poly:.2f})')
    plt.title(f'Polynomial Regression Analysis: {independent_var}')
    plt.xlabel(f'{independent_var} - Sensor Tree')
    plt.ylabel(f'{dependent_var} - CDSK')
    plt.legend()
    plt.grid(True)
    plt.show()

    return r2_poly, equation


def main():
    # Load the Train dataset
    train_data = load_dataset("Select the Train_Experiment dataset")

    # Ensure the dataset is loaded before proceeding
    if train_data is not None:
        # Define the variable pairs
        variable_pairs_train = [
            ("Air Temp @0.10m", "Air Temp (Point1_Upperleft.t_db_value)"),
            ("Air Temp @1.10m", "Air Temp (Point1_Upperleft.t_db_value)"),
            ("Air Temp @1.70m", "Air Temp (Point1_Upperleft.t_db_value)"),
            ("CO2 Concentration @1.10m", "CO2(Point1_Upperleft.co2_value)"),
            ("Relative Humidity @1.10m", "Relative Humidity (Point1_Upperleft.rh_value)"),
            ("Operative Temp @0.10m", "Operative Temperature(Point1_Upperleft.OperativeTemp_value)"),
            ("Operative Temp @1.10m", "Operative Temperature(Point1_Upperleft.OperativeTemp_value)"),
            ("Operative Temp @1.70m", "Operative Temperature(Point1_Upperleft.OperativeTemp_value)")
        ]

        # Perform polynomial regression analysis for each variable pair
        for independent_var, dependent_var in variable_pairs_train:
            print(f"\nAnalyzing {independent_var} vs {dependent_var} in Train Environment...")
            r2_poly, equation = perform_polynomial_analysis(train_data, independent_var, dependent_var, degree=2)
            if r2_poly is not None:
                print(f"Polynomial R² value for {independent_var} vs {dependent_var}: {r2_poly:.4f}")
                print(f"Derived Polynomial Equation: {equation}")
    else:
        print("Please make sure the dataset is selected and loaded correctly.")


if __name__ == "__main__":
    main()
