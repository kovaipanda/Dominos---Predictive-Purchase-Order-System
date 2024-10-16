import pandas as pd

# Define the path to your text file
file_path = r"C:\Users\DELL\Downloads\Dominos - Predictive Purchase Order System\prophet_sales_forecast_results.txt"

# Initialize an empty list to hold the data
data = []

# Open and read the text file
with open(file_path, 'r') as file:
    lines = file.readlines()

# Initialize variables to store the current pizza ID and sales data
current_pizza_id = None

# Iterate over each line in the text file
for line in lines:
    # Check if the line indicates a new Pizza ID
    if "Predicted sales for Pizza ID" in line:
        current_pizza_id = int(line.split()[-1][:-1])  # Extract Pizza ID
    elif "Predicted Quantity" in line and current_pizza_id is not None:
        # Extract date and predicted quantity
        parts = line.split(", ")
        date = parts[0].split(": ")[1]  # Get date
        quantity = float(parts[1].split(": ")[1])  # Get predicted quantity
        data.append({"Pizza ID": current_pizza_id, "Date": date, "Predicted Quantity": quantity})

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)

# Define the mapping for pizza names
pizza_name_mapping = {
    'bbq_ckn_l': 0, 'bbq_ckn_m': 1, 'bbq_ckn_s': 2, 'big_meat_s': 3, 'brie_carre_s': 4,
    'calabrese_l': 5, 'calabrese_m': 6, 'calabrese_s': 7, 'cali_ckn_l': 8, 'cali_ckn_m': 9,
    'cali_ckn_s': 10, 'ckn_alfredo_l': 11, 'ckn_alfredo_m': 12, 'ckn_alfredo_s': 13,
    'ckn_pesto_l': 14, 'ckn_pesto_m': 15, 'ckn_pesto_s': 16, 'classic_dlx_l': 17,
    'classic_dlx_m': 18, 'classic_dlx_s': 19, 'five_cheese_l': 20, 'four_cheese_l': 21,
    'four_cheese_m': 22, 'green_garden_l': 23, 'green_garden_m': 24, 'green_garden_s': 25,
    'hawaiian_l': 26, 'hawaiian_m': 27, 'hawaiian_s': 28, 'ital_cpcllo_l': 29,
    'ital_cpcllo_m': 30, 'ital_cpcllo_s': 31, 'ital_supr_l': 32, 'ital_supr_m': 33,
    'ital_supr_s': 34, 'ital_veggie_l': 35, 'ital_veggie_m': 36, 'ital_veggie_s': 37,
    'mediterraneo_l': 38, 'mediterraneo_m': 39, 'mediterraneo_s': 40, 'mexicana_l': 41,
    'mexicana_m': 42, 'mexicana_s': 43, 'napolitana_l': 44, 'napolitana_m': 45,
    'napolitana_s': 46, 'pep_msh_pep_l': 47, 'pep_msh_pep_m': 48, 'pep_msh_pep_s': 49,
    'pepperoni_l': 50, 'pepperoni_m': 51, 'pepperoni_s': 52, 'peppr_salami_l': 53,
    'peppr_salami_m': 54, 'peppr_salami_s': 55, 'prsc_argla_l': 56, 'prsc_argla_m': 57,
    'prsc_argla_s': 58, 'sicilian_l': 59, 'sicilian_m': 60, 'sicilian_s': 61,
    'soppressata_l': 62, 'soppressata_m': 63, 'soppressata_s': 64, 'southw_ckn_l': 65,
    'southw_ckn_m': 66, 'southw_ckn_s': 67, 'spicy_ital_l': 68, 'spicy_ital_m': 69,
    'spicy_ital_s': 70, 'spin_pesto_l': 71, 'spin_pesto_m': 72, 'spin_pesto_s': 73,
    'spinach_fet_l': 74, 'spinach_fet_m': 75, 'spinach_fet_s': 76, 'spinach_supr_l': 77,
    'spinach_supr_m': 78, 'spinach_supr_s': 79, 'thai_ckn_l': 80, 'thai_ckn_m': 81,
    'thai_ckn_s': 82, 'the_greek_l': 83, 'the_greek_m': 84, 'the_greek_s': 85,
    'the_greek_xl': 86, 'the_greek_xxl': 87, 'veggie_veg_l': 88, 'veggie_veg_m': 89,
    'veggie_veg_s': 90
}

# Inverting the dictionary
inverted_mapping = {v: k for k, v in pizza_name_mapping.items()}

# Create the pizza_name_id column by mapping Pizza ID
df['pizza_name_id'] = df['Pizza ID'].map(inverted_mapping)

# Create the quantity column by rounding Predicted Quantity and changing negatives to 0
df['quantity'] = df['Predicted Quantity'].clip(lower=0).round().astype(int)

# Convert the Date column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

# Display the DataFrame
print(df)

# Save the DataFrame to a CSV file
output_path = r"C:\Users\DELL\Downloads\Dominos - Predictive Purchase Order System\predicted_prophet_sales.csv"
df.to_csv(output_path, index=False)
