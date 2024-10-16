import pandas as pd
import numpy as np
from datetime import datetime

# Load the Excel file
file_path = r"C:\Users\DELL\Downloads\Dominos - Predictive Purchase Order System\Pizza_Sale_fimp.xlsx"
df = pd.read_excel(file_path)

#  Group by OrderID and count occurrences
order_counts = df['order_id'].value_counts()

# Ensure 'order_date' is in datetime format
df['order_date'] = pd.to_datetime(df['order_date'])

# Group by 'pizza_name_id' and 'order_date' to calculate 'total_quantity'
df['total_quantity'] = df.groupby(['pizza_name_id', 'order_date','pizza_size'])['quantity'].transform('sum')

# Drop duplicates to keep only one row per unique combination of pizza_name_id and order_date
df = df.drop_duplicates(subset=['pizza_name_id', 'order_date','pizza_size'])

# Create 'is_weekend' column
df['is_weekend'] = df['order_date'].dt.dayofweek.apply(lambda x: 1 if x >= 5 else 0)

# Create 'day_of_week' column (0 = Monday, 6 = Sunday)
df['day_of_week'] = df['order_date'].dt.dayofweek

# Create 'month' column
df['month'] = df['order_date'].dt.month

# Define official holidays
official_holidays = {
    "New Year's Day": '2015-01-01',
    "Thai Pongal": '2015-01-14',
    "Maatu Pongal": '2015-01-15',
    "Tamizh New Year": '2015-04-14',
    "May Day": '2015-05-01',
    "Independence Day": '2015-08-15',
    "Ganesh Chaturthi": '2015-09-17',
    "Mahatma Gandhi Jayanti": '2015-10-02',
    "Diwali": '2015-11-11',
    "Christmas": '2015-12-25',
    "Eid ul-Fitr": '2015-07-17',  # Date may vary based on the moon sighting
    "Eid ul-Adha": '2015-09-24',  # Date may vary based on the moon sighting
    "Id-E-Milad": '2015-01-04',    # Date may vary based on the moon sighting
    "The birthday of Dr. B.R. Ambedkar": '2015-04-14'
}

# Define unofficial holidays
unofficial_holidays = {
    "Pongal Festival": '2015-01-14',  # Observed for several days
    "Deepavali Celebrations": '2015-11-10',  # Observed for several days
    "Easter": '2015-04-20',
    "Holi": '2015-03-06',
    "Ramzan": '2015-07-16',  # Varies based on moon sighting
    "Good Friday": '2015-04-18'
}

# Combine official and unofficial holidays into a single dictionary
all_holidays = {**official_holidays, **unofficial_holidays}

# Create a new column for holidays
df['is_holiday'] = df['order_date'].dt.date.isin(pd.to_datetime(list(all_holidays.values())).date).astype(int)

# Function to create flags for promotional periods based on specific dates in India
def is_promotional(date):
    date_str = date.strftime('%Y-%m-%d')  # Format date as string
    promotional_dates = [
        '2015-01-01', '2015-01-14', '2015-01-26', '2015-02-14', '2015-02-09',
        '2015-03-06', '2015-04-03', '2015-04-05', '2015-04-14', '2015-04-15',
        '2015-05-01', '2015-05-10', '2015-06-21', '2015-07-17', '2015-08-15',
        '2015-08-29', '2015-09-17', '2015-10-02', '2015-10-22', '2015-11-11',
        '2015-11-14', '2015-12-25', '2015-12-31'
    ]
    return 1 if date_str in promotional_dates else 0

# Apply the function to create the 'is_promotion' column based on specific dates
df['is_promotion'] = df['order_date'].apply(is_promotional)

# Add promotion for all Tuesdays if pizza_size is 'M' or 'L'
tuesday_mask = (df['day_of_week'] == 1) & (df['pizza_size'].isin(['M', 'L']))
df.loc[tuesday_mask, 'is_promotion'] = 1
# Select only the relevant columns
output_df = df[['pizza_name_id', 'order_date', 'total_quantity', 'is_promotion', 'is_weekend', 'day_of_week', 'month', 'is_holiday']]

# Interpolate all numeric columns
output_df['total_quantity'] = output_df['total_quantity'].interpolate()

# Remove outliers from 'total_quantity' using IQR method
Q1 = output_df['total_quantity'].quantile(0.25)
Q3 = output_df['total_quantity'].quantile(0.75)
IQR = Q3 - Q1

# Define the upper and lower bounds for outlier removal
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Remove outliers
output_df = output_df[(output_df['total_quantity'] >= lower_bound) & (output_df['total_quantity'] <= upper_bound)]

# Save the processed data to a new Excel file
output_file_path = r"C:\Users\DELL\Downloads\Dominos - Predictive Purchase Order System\Pizza_Sale_imp_fea.xlsx"
output_df.to_excel(output_file_path, index=False)

print(f"File saved to {output_file_path}")
