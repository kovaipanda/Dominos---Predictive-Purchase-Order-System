import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file
file_path = r"C:\Users\DELL\Downloads\Dominos - Predictive Purchase Order System\Pizza_Sale.xlsx"
df = pd.read_excel(file_path)

# Fill missing values in 'total_price' as 'quantity' * 'unit_price'
df['total_price'] = df['total_price'].fillna(df['quantity'] * df['unit_price'])

# Step 1: Create a map of 'pizza_ingredients' to 'pizza_category' where 'pizza_category' is not missing
ingredient_category_map = df.dropna(subset=['pizza_category']).set_index('pizza_ingredients')['pizza_category'].to_dict()

# Step 2: Fill missing values in 'pizza_category' using the map from 'pizza_ingredients'
df['pizza_category'] = df.apply(
    lambda row: ingredient_category_map.get(row['pizza_ingredients'], row['pizza_category']) if pd.isna(row['pizza_category']) else row['pizza_category'],
    axis=1
)

# Step 1: Create a map of 'pizza_name_id' to 'pizza_name' where 'pizza_name' is not missing
name_id_map = df.dropna(subset=['pizza_name']).set_index('pizza_name_id')['pizza_name'].to_dict()

# Step 2: Fill missing values in 'pizza_name' using the map from 'pizza_name_id'
df['pizza_name'] = df.apply(
    lambda row: name_id_map.get(row['pizza_name_id'], row['pizza_name']) if pd.isna(row['pizza_name']) else row['pizza_name'],
    axis=1
)

# Step 1: Create a map of 'pizza_name' to 'pizza_ingredients' where 'pizza_ingredients' is not missing
name_ingredients_map = df.dropna(subset=['pizza_ingredients']).set_index('pizza_name')['pizza_ingredients'].to_dict()

# Step 2: Fill missing values in 'pizza_ingredients' using the map from 'pizza_name'
df['pizza_ingredients'] = df.apply(
    lambda row: name_ingredients_map.get(row['pizza_name'], row['pizza_ingredients']) if pd.isna(row['pizza_ingredients']) else row['pizza_ingredients'],
    axis=1
)

# Step 1: Create a map of ('pizza_size', 'pizza_name') to 'pizza_name_id' where 'pizza_name_id' is not missing
size_name_id_map = df.dropna(subset=['pizza_name_id']).set_index(['pizza_size', 'pizza_name'])['pizza_name_id'].to_dict()

# Step 2: Fill missing values in 'pizza_name_id' using the map from 'pizza_size' and 'pizza_name'
df['pizza_name_id'] = df.apply(
    lambda row: size_name_id_map.get((row['pizza_size'], row['pizza_name']), row['pizza_name_id']) if pd.isna(row['pizza_name_id']) else row['pizza_name_id'],
    axis=1
)

# Get the number of missing values in each column
missing_values = df.isnull().sum()

# Display the result
print(missing_values)

# Step 1: Select the relevant columns for numerical analysis
numerical_columns = ['pizza_id', 'order_id', 'quantity', 'unit_price', 'total_price']

# Step 2: Convert the selected columns to numeric, forcing errors to NaN (in case of invalid data)
df[numerical_columns] = df[numerical_columns].apply(pd.to_numeric, errors='coerce')

# Step 3: Create box plots for each numerical column to identify outliers
plt.figure(figsize=(15, 10))  # Adjust figure size for better visualization

# Create individual box plots
for i, col in enumerate(numerical_columns, 1):
    plt.subplot(2, 3, i)  # Create subplots (2 rows, 3 columns)
    plt.boxplot(df[col].dropna())  # Drop missing values and plot
    plt.title(col)

plt.tight_layout()  # Adjust subplots to fit into figure area
plt.show()

# Save the updated DataFrame to a new Excel file (optional)
df.to_excel("Pizza_Sale_data_cleaned.xlsx", index=False)


# Step 1: Check for missing data and preview dataset
print(df.info())  # To check for missing values and data types
print(df.describe())  # Statistical summary of numerical columns

# Convert 'order_date' to datetime for time series analysis
df['order_date'] = pd.to_datetime(df['order_date'])

# Step 2: Analyze Sales Trends Over Time
# Aggregate total sales per day
daily_sales = df.groupby('order_date')['total_price'].sum()

# Plot sales trend over time
plt.figure(figsize=(10, 6))
plt.plot(daily_sales.index, daily_sales.values, color='blue')
plt.title('Sales Trend Over Time')
plt.xlabel('Order Date')
plt.ylabel('Total Sales')
plt.grid(True)
plt.show()

# Step 3: Analyze Seasonality (Monthly Sales Trends)
df['order_month'] = df['order_date'].dt.to_period('M')
monthly_sales = df.groupby('order_month')['total_price'].sum()

# Plot monthly sales trends
plt.figure(figsize=(10, 6))
plt.plot(monthly_sales.index.astype(str), monthly_sales.values, color='green')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Step 4: Analyze Weekly Sales Patterns
df['order_weekday'] = df['order_date'].dt.day_name()

# Calculate average sales by day of the week
weekly_sales = df.groupby('order_weekday')['total_price'].mean()

# Plot weekly sales patterns
plt.figure(figsize=(10, 6))
sns.barplot(x=weekly_sales.index, y=weekly_sales.values, palette="viridis")
plt.title('Average Sales by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Average Sales')
plt.xticks(rotation=45)
plt.show()

# Step 5: Product Sales Analysis
# Aggregate total sales per pizza category
pizza_category_sales = df.groupby('pizza_category')['total_price'].sum()

# Plot total sales by pizza category
plt.figure(figsize=(10, 6))
sns.barplot(x=pizza_category_sales.index, y=pizza_category_sales.values, palette="coolwarm")
plt.title('Total Sales by Pizza Category')
plt.xlabel('Pizza Category')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.show()

# Step 6: Customer Insights - Repeat Orders
# Calculate the number of orders per customer (if customer_id is available)
if 'customer_id' in df.columns:
    customer_order_count = df['customer_id'].value_counts()

    # Plot number of orders by customers
    plt.figure(figsize=(10, 6))
    sns.histplot(customer_order_count, kde=False, bins=20, color='orange')
    plt.title('Number of Orders per Customer')
    plt.xlabel('Number of Orders')
    plt.ylabel('Count of Customers')
    plt.grid(True)
    plt.show()

# Step 7: Correlation Heatmap (Identify Significant Features)
# Only numerical columns will be included in the correlation matrix
numerical_columns = ['pizza_id', 'order_id', 'quantity', 'unit_price', 'total_price']
corr_matrix = df[numerical_columns].corr()

# Plot correlation heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Heatmap of Numerical Features')
plt.show()
