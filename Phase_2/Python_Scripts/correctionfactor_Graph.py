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
    file_path = askopenfilename(title=prompt,
                                filetypes=[("Excel files", "*.xlsx *.xls")])  # Open file dialog to select a file
    if file_path:
        print(f"File selected: {file_path}")
        # Load the data using the second row (index 1) as the header
        return pd.read_excel(file_path, header=1)
    else:
        print("No file selected.")
        return None


def perform_polynomial_analysis_and_correction(data, independent_var, dependent_var, degree=2):
    """Function to perform polynomial regression analysis and calculate correction factors."""
    print(f"Starting analysis for {independent_var} vs {dependent_var}...")

    # Clean the data
    data.columns = data.columns.str.strip()  # Strip any leading/trailing spaces from column names

    if independent_var not in data.columns or dependent_var not in data.columns:
        print(f"Column not found: {independent_var} or {dependent_var}")
        return None

    print(f"Columns found. Proceeding with regression...")

    # Convert columns to numeric and inspect the first few rows
    data[independent_var] = pd.to_numeric(data[independent_var], errors='coerce')
    data[dependent_var] = pd.to_numeric(data[dependent_var], errors='coerce')

    # Drop rows with missing values in these columns
    clean_data = data.dropna(subset=[independent_var, dependent_var])
    if clean_data.empty:
        print(f"No valid data found for {independent_var} and {dependent_var} after cleaning.")
        return None

    print(f"Data cleaned. Proceeding with polynomial regression...")

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

    # Generate the polynomial regression equation
    intercept = poly_reg.intercept_
    coef = poly_reg.coef_
    equation = f"y = {coef[2]:.6f} * X^2 + {coef[1]:.6f} * X + {intercept:.6f}"

    print(f"Polynomial regression completed with R² = {r2_poly:.2f}")
    print(f"Derived Polynomial Equation: {equation}")

    # Calculate the dynamic correction factor
    correction_factor = y - y_poly_pred
    corrected_predictions = y_poly_pred + correction_factor.mean()  # Apply mean correction factor for adjustment
    r2_corrected = r2_score(y, corrected_predictions)

    clean_data['Correction Factor'] = correction_factor

    # Plotting the polynomial regression result with correction factor and actual data points
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', label='Actual Data Points')
    plt.plot(X, y_poly_pred, color='green', label=f'Polynomial Regression (R² = {r2_poly:.2f})')
    plt.plot(X, corrected_predictions, color='orange', label=f'Corrected Predictions (R² = {r2_corrected:.2f})')
    plt.scatter(X, correction_factor, color='red', label='Correction Factor')
    plt.title(f'Polynomial Regression & Correction Factor: {independent_var}')
    plt.xlabel(f'{independent_var} - Sensor Tree')
    plt.ylabel(f'{dependent_var} - CDSK / CF')

    plt.legend()
    plt.grid(True)
    plt.show()

    print(f"Plot displayed.")

    # Return the dataset with correction factors, polynomial equation, and the corrected R² value
    return clean_data, equation, r2_corrected


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

        # Perform polynomial regression analysis and calculate correction factors for each variable pair
        correction_factors = {}
        polynomial_equations = {}
        r2_corrected_values = {}
        for independent_var, dependent_var in variable_pairs_train:
            print(f"\nAnalyzing {independent_var} vs {dependent_var} in Train Environment...")
            corrected_data, equation, r2_corrected = perform_polynomial_analysis_and_correction(train_data,
                                                                                                independent_var,
                                                                                                dependent_var,
                                                                                                degree=2)
            if corrected_data is not None:
                correction_factors[independent_var] = corrected_data['Correction Factor'].mean()
                polynomial_equations[independent_var] = equation
                r2_corrected_values[independent_var] = r2_corrected
                print(f"Average Correction Factor for {independent_var}: {correction_factors[independent_var]:.4f}°C")
                print(f"Polynomial Equation for {independent_var}: {equation}")
                print(f"R² after correction for {independent_var}: {r2_corrected:.2f}")

        # Display all polynomial equations and R² after correction
        print("\nPolynomial Equations derived for each parameter:")
        for param, eq in polynomial_equations.items():
            print(f"{param}: {eq}")

        print("\nR² after applying correction factor for each parameter:")
        for param, r2_value in r2_corrected_values.items():
            print(f"{param}: {r2_value:.2f}")

    else:
        print("Please make sure the dataset is selected and loaded correctly.")


if __name__ == "__main__":
    main()
