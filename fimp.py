import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# Step 1: Load the dataset
file_path = r"C:\Users\DELL\Downloads\Dominos - Predictive Purchase Order System\Pizza_Sale_prediction.xlsx"
df = pd.read_excel(file_path)

# Step 2: Data Preparation
# Check the data types
print(df.dtypes)

# Convert order_date and order_time to datetime if necessary
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df['order_time'] = pd.to_datetime(df['order_time'], format='%H:%M:%S', errors='coerce')

# Extract additional date features
df['year'] = df['order_date'].dt.year
df['day'] = df['order_date'].dt.day
df['quarter'] = df['order_date'].dt.quarter
df['order_hour'] = df['order_time'].dt.hour

# Convert 'pizza_name_id' to numerical using Label Encoding
label_encoder = LabelEncoder()
df['pizza_name_id'] = label_encoder.fit_transform(df['pizza_name_id'])

# Create a mapping of pizza names to their corresponding encoded values
pizza_mapping = dict(zip(label_encoder.classes_, range(len(label_encoder.classes_))))
print("Pizza Name to ID Mapping:", pizza_mapping)

# Drop other categorical columns if necessary (list them here)
# If you have other categorical columns to drop, add their names to the list
columns_to_drop = ['other_categorical_column1', 'other_categorical_column2']  # Replace with actual column names
df = df.drop(columns=columns_to_drop, errors='ignore')  # Use errors='ignore' to avoid errors if columns don't exist

# Step 3: Group by date to get daily pizza quantity
daily_quantity = df.groupby('order_date').agg({'quantity': 'sum'}).reset_index()

# Merge daily_quantity back with original dataframe if needed (to keep all features)
df = df.merge(daily_quantity, on='order_date', suffixes=('', '_daily'), how='left')

# Prepare the features and target variable
X = df[['pizza_name_id', 'day_of_week', 'month', 'order_hour', 'is_weekend', 'is_promotion', 'is_holiday', "pizza_id"]]
y = df['quantity_daily']  # use aggregated quantity per day

# Step 4: Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the XGBoost model
model = XGBRegressor()
model.fit(X_train, y_train)

# Step 5: Get feature importances
importances = model.feature_importances_

# Create a DataFrame for visualization
feature_importance_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

# Step 6: Plotting feature importances
plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'], color='skyblue')
plt.xlabel('Importance Score')
plt.title('Feature Importance for Pizza Quantity Forecasting')
plt.show()

# Step 7: Print feature importance data
print(feature_importance_df)

# Save the updated DataFrame to a new Excel file 
output_file_path = r"C:\Users\DELL\Downloads\Dominos - Predictive Purchase Order System\Pizza_Sale_fimp.xlsx"
df.to_excel(output_file_path, index=False)
