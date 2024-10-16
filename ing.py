import pandas as pd

# Load the Excel and CSV files
ingredients_file = r"C:\Users\DELL\Downloads\Dominos - Predictive Purchase Order System\Pizza_ingredients.xlsx"
sales_file = r"C:\Users\DELL\Downloads\Dominos - Predictive Purchase Order System\predicted_prophet_sales.csv"

# Read the ingredients and sales data
ingredients_df = pd.read_excel(ingredients_file)
sales_df = pd.read_csv(sales_file)

# Ensure the 'pizza_name_id' and 'pizza_name_id' are of the same type
ingredients_df['pizza_name_id'] = ingredients_df['pizza_name_id'].astype(str)
sales_df['pizza_name_id'] = sales_df['pizza_name_id'].astype(str)

# Process each unique date in sales data
for unique_date in sales_df['Date'].unique():
    # Filter sales data for the current date
    date_sales = sales_df[sales_df['Date'] == unique_date]

    # Loop through each pizza in the sales data for the current date
    for index, row in date_sales.iterrows():
        pizza_id = row['pizza_name_id']
        quantity = row['quantity']

        # Find the corresponding ingredient entries (multiple rows for one pizza)
        ingredient_rows = ingredients_df[ingredients_df['pizza_name_id'] == pizza_id]

        # Loop through all ingredients for the current pizza
        for ing_index, ingredient_row in ingredient_rows.iterrows():
            # Get the Items_Qty_In_Grams value for the current ingredient
            items_qty_in_grams = ingredient_row['Items_Qty_In_Grams']

            # Calculate the total amount to fill in the appropriate column
            total_qty = items_qty_in_grams * quantity

            # Update the correct column (create the column if not already present)
            if unique_date not in ingredients_df.columns:
                ingredients_df[unique_date] = 0  # Initialize the column if not exists

            # Update the ingredient quantity for the current date and pizza
            ingredients_df.loc[ing_index, unique_date] += total_qty

# Save the updated Excel file
ingredients_df.to_excel(ingredients_file, index=False)
