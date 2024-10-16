import pandas as pd

# Step 1: Load the Excel file
input_file = r"C:\Users\DELL\Downloads\Dominos - Predictive Purchase Order System\Pizza_ingredients.xlsx"
df = pd.read_excel(input_file)

# Step 2: Select relevant columns (pizza_ingredients and the date columns)
date_columns = ['1/1/2016', '1/2/2016', '1/3/2016', '1/4/2016', '1/5/2016', '1/6/2016', '1/7/2016']
columns = ['pizza_ingredients'] + date_columns

# Step 3: Group by 'pizza_ingredients' and sum the values for each unique ingredient
df_grouped = df[columns].groupby('pizza_ingredients').sum()

# Step 4: Save the result to a new Excel file
output_file = r"C:\Users\DELL\Downloads\Dominos - Predictive Purchase Order System\Pizza_ingredients_final_list.xlsx"
df_grouped.to_excel(output_file, index=True)

print(f"File saved to {output_file}")
