import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load the dataset
file_path = r"C:\Users\DELL\Downloads\Dominos - Predictive Purchase Order System\Pizza_Sale_data_cleaned.xlsx"
df = pd.read_excel(file_path)

# Step 1: Convert 'order_date' and 'order_time' to datetime format
# Adjust the format based on the actual date format in your dataset
df['order_date'] = pd.to_datetime(df['order_date'], format='%d-%m-%Y', errors='coerce')  # Use appropriate format
df['order_time'] = pd.to_datetime(df['order_time'], format='%H:%M:%S', errors='coerce').dt.time  # Keep only the time part

# Check for any conversion issues
if df['order_date'].isnull().any():
    print("Warning: Some dates could not be converted. Please check the data.")

# Step 2: Create time-based features
# Day of the week (0=Monday, 6=Sunday)
df['day_of_week'] = df['order_date'].dt.dayofweek

# Day name (e.g., Monday, Tuesday, etc.)
df['day_name'] = df['order_date'].dt.day_name()

# Month of the order
df['month'] = df['order_date'].dt.month

# Hour of the day (Extract hour from 'order_time')
df['order_hour'] = pd.to_datetime(df['order_time'].astype(str), format='%H:%M:%S', errors='coerce').dt.hour

# Is Weekend (Create a flag for weekend orders)
df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

# Function to create flags for promotional periods based on specific dates in India
def is_promotional(date):
    if date == '2015-01-01':  # New Year’s Day
        return 1
    elif date == '2015-01-14':  # Makar Sankranti
        return 1
    elif date == '2015-01-26':  # Republic Day
        return 1
    elif date == '2015-02-14':  # Valentine’s Day
        return 1
    elif date == '2015-02-09':  # National Pizza Day
        return 1
    elif date == '2015-03-06':  # Holi
        return 1
    elif date == '2015-04-03':  # Good Friday
        return 1
    elif date == '2015-04-05':  # Easter
        return 1
    elif date == '2015-04-14':  # Baisakhi
        return 1
    elif date == '2015-04-15':  # Ram Navami
        return 1
    elif date == '2015-05-01':  # Labour Day
        return 1
    elif date == '2015-05-10':  # Mother’s Day
        return 1
    elif date == '2015-06-21':  # Father’s Day
        return 1
    elif date == '2015-07-17':  # Eid ul-Fitr
        return 1
    elif date == '2015-08-15':  # Independence Day
        return 1
    elif date == '2015-08-29':  # Raksha Bandhan
        return 1
    elif date == '2015-09-17':  # Ganesh Chaturthi
        return 1
    elif date == '2015-10-02':  # Mahatma Gandhi Jayanti
        return 1
    elif date == '2015-10-22':  # Dussehra
        return 1
    elif date == '2015-11-11':  # Diwali
        return 1
    elif date == '2015-11-14':  # Children’s Day
        return 1
    elif date == '2015-12-25':  # Christmas
        return 1
    elif date == '2015-12-31':  # New Year’s Eve
        return 1
    else:
        return 0

# Apply the function to create the 'is_promotion' column based on specific dates
df['is_promotion'] = df['order_date'].apply(is_promotional)


# Step 4: Create flags for holidays using the holidays dictionary
# Create 'is_holiday' column (example: if 'holiday' column exists and is True, set it to 1, else 0)
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



# Step 5: Preview the updated dataset with new features
print(df.describe())

# Save the updated DataFrame to a new Excel file (optional)
output_file_path = r"C:\Users\DELL\Downloads\Dominos - Predictive Purchase Order System\Pizza_Sale_prediction.xlsx"
df.to_excel(output_file_path, index=False)
