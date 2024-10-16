import pandas as pd
from prophet import Prophet
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error
from datetime import datetime
import numpy as np

# Load the dataset
file_path = r"C:\Users\DELL\Downloads\Dominos - Predictive Purchase Order System\Pizza_Sale_imp_fea.xlsx"
data = pd.read_excel(file_path)

# Ensure order_date is a datetime object
data['order_date'] = pd.to_datetime(data['order_date'])

# Check for missing values in regressor columns
regressor_cols = ['is_promotion', 'is_weekend', 'day_of_week', 'month', 'is_holiday']
missing_counts = data[regressor_cols].isnull().sum()
print("Missing values in regressor columns:\n", missing_counts)

# Fill missing values if any (just for safety)
data[regressor_cols] = data[regressor_cols].fillna(0)

# Prepare the forecast results DataFrame
forecast_results = []

# Define the specific dates for prediction
predict_dates = pd.date_range(start='2016-01-01', end='2016-01-07', freq='D')

# Get unique pizza IDs
pizza_ids = data['pizza_name_id'].unique()

# Create a list to store MAPE values for each pizza
mape_values = []

# Loop through each pizza_name_id and build Prophet and Random Forest models
for pizza_id in pizza_ids:
    # Filter the data for the current pizza
    pizza_data = data[data['pizza_name_id'] == pizza_id]

    # Split the data into training (before 2016) and future prediction
    train_data = pizza_data[pizza_data['order_date'] < '2016-01-01']

    # Prepare the data for Prophet
    train_df = train_data[['order_date', 'total_quantity', 'is_promotion', 
                            'is_weekend', 'day_of_week', 'month', 'is_holiday']].rename(
        columns={'order_date': 'ds', 'total_quantity': 'y'})

    # Create and fit the Prophet model
    model_prophet = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    
    # Add regressors
    model_prophet.add_regressor('is_promotion')
    model_prophet.add_regressor('is_weekend')
    model_prophet.add_regressor('day_of_week')
    model_prophet.add_regressor('month')
    model_prophet.add_regressor('is_holiday')

    model_prophet.fit(train_df)

    # Prepare features for Random Forest
    X_train_rf = train_data[['is_promotion', 'is_weekend', 'day_of_week', 'month', 'is_holiday']]
    y_train_rf = train_data['total_quantity']

    # Train Random Forest model
    model_rf = RandomForestRegressor(n_estimators=100, random_state=42)
    model_rf.fit(X_train_rf, y_train_rf)

    # Create a DataFrame for future dates using the specific date range
    future_dates = pd.DataFrame({'ds': predict_dates})

    # Merge with the original data to fill regressor values for future dates
    future_dates = future_dates.merge(pizza_data[['order_date', 'is_promotion', 'is_weekend', 
                                                   'day_of_week', 'month', 'is_holiday']],
                                       left_on='ds', right_on='order_date', how='left')

    # Fill NaNs in future_dates after the merge
    future_dates[regressor_cols] = future_dates[regressor_cols].fillna(0)

    # Prophet predictions
    forecast_prophet = model_prophet.predict(future_dates)

    # Random Forest predictions
    X_future_rf = future_dates[['is_promotion', 'is_weekend', 'day_of_week', 'month', 'is_holiday']]
    forecast_rf = model_rf.predict(X_future_rf)

    # Ensemble prediction (Averaging Prophet and Random Forest predictions)
    ensemble_prediction = (forecast_prophet['yhat'] + forecast_rf) / 2

    # Collect forecast results for the specific dates
    for i, row in future_dates.iterrows():
        forecast_results.append({
            'pizza_name_id': pizza_id,
            'order_date': row['ds'].strftime('%Y-%m-%d'),
            'predicted_quantity': ensemble_prediction[i]
        })

    # Calculate MAPE on the training data
    if not train_df.empty:
        # Prophet MAPE
        train_forecast_prophet = model_prophet.predict(train_df[['ds', 'is_promotion', 'is_weekend', 
                                                                 'day_of_week', 'month', 'is_holiday']])
        # Random Forest predictions on training data
        train_rf_predictions = model_rf.predict(X_train_rf)

        # Ensemble on training data
        ensemble_train_predictions = (train_forecast_prophet['yhat'] + train_rf_predictions) / 2

        # Calculate MAPE
        mape = mean_absolute_percentage_error(train_df['y'], ensemble_train_predictions)
        mape_values.append(mape)  # Store MAPE value
        print(f'MAPE for Pizza ID {pizza_id}: {mape:.2f}')

# Calculate the average MAPE
if mape_values:
    average_mape = sum(mape_values) / len(mape_values)
    print(f'Average MAPE across all pizza IDs: {average_mape:.2f}')

# Convert the results into a DataFrame
forecast_df = pd.DataFrame(forecast_results)

# Optionally print the forecast
print(forecast_df)

# Save to a text file
with open("prophet_sales_forecast_results.txt.txt", "w") as file:
    file.write("Sales Forecast from 2016-01-01 to 2016-01-07 (Ensemble of Prophet and Random Forest Models):\n")
    
    for pizza_id in pizza_ids:
        file.write(f"\nPredicted sales for Pizza ID {pizza_id}:\n")
        pizza_forecast = forecast_df[forecast_df['pizza_name_id'] == pizza_id]
        for _, row in pizza_forecast.iterrows():
            file.write(f"Date: {row['order_date']}, Predicted Quantity: {row['predicted_quantity']}\n")
