Dominos---Predictive-Purchase-Order-System

Project Overview

This project focuses on building a predictive model for Domino's pizza orders based on historical sales data. 
The process includes data cleaning, feature engineering, and building machine learning models to forecast future sales. 
It utilizes time series forecasting models, such as Prophet and Random Forest, to predict pizza sales for specific dates.

The goal is to create a reliable system that assists in generating purchase orders for ingredients, reducing waste, and optimizing inventory levels.

Project Structure

📂 Dominos - Predictive Purchase Order System
│

├── 📁 Data

│   ├── Pizza_Sale.xlsx                 
# Raw sales data

│   ├── Pizza_Sale_cleaned.xlsx         
# Cleaned sales data after processing

│   ├── Pizza_Sale_fimp.xlsx          
# Data after feature engineering

│   ├── Pizza_Sale_imp_fea.xlsx        
# Data after interpolation and outlier removal

│   ├── Ingredients_Forecast.xlsx       
# Predicted ingredient requirements

├── data_cleaning.py                    
# Script for cleaning the sales data

├── sales_prediction.py                 
# Script for predicting sales

├── fimp.py                             
# Script for feature engineering

├── imp_fea.py                           
# Script for performing feature engineering and outlier removal

├── por.py                             
# Script for prediction using Prophet and Random Forest

├── pred_prop.py                       
# Script for extracting and formatting results from predictions

├── ing.py                             
# Script for predicting ingredient requirements based on sales forecast

└── ingredients_list_predicted.py       
# Script for predicting the ingredients list

Installation

Prerequisites

To run this project, ensure you have the following libraries installed:

Python 3.x

pandas

numpy

scikit-learn

prophet

openpyxl

You can install these packages using pip:

pip install pandas numpy scikit-learn prophet openpyxl

Files Description

Pizza_Sale.xlsx: The raw dataset containing historical pizza order information.

Pizza_Sale_cleaned.xlsx: The cleaned dataset after running the data_cleaning.py script.

Pizza_Sale_fimp.xlsx: The dataset after performing feature engineering (intermediate features).

Pizza_Sale_imp_fea.xlsx: The final dataset after interpolating missing values and removing outliers.

Ingredients_Forecast.xlsx: The final predicted output for ingredient orders based on the sales forecast.

prophet_sales_forecast_results.txt: Text output of sales predictions from the Prophet and Random Forest ensemble models.

Data Cleaning (data_cleaning.py)

This script loads the raw sales data and performs the following cleaning steps:

Handling missing values.

Correcting date formats.

Standardizing text fields.

Removing any duplicates or invalid entries.

The cleaned data is saved as Pizza_Sale_cleaned.xlsx.

Usage

python data_cleaning.py

sales_prediction.py

This script prepares the sales dataset for predictive modeling. 

It performs feature engineering by extracting time-based features and creating flags for promotional periods and holidays.

Key Features:

Converts order_date and order_time to appropriate datetime formats.

Creates new features such as:

Day of the week

Month

Hour of the order

Weekend flag

Promotional and holiday flags

Outputs an updated dataset with new features for sales prediction modeling.

Feature Engineering (fimp.py)

This script processes the cleaned data and generates new features:

Total Quantity: Aggregates the total quantity of pizzas ordered by pizza_name_id, order_date, and pizza_size.

Is Weekend: A binary flag indicating if the order was placed on a weekend.

Is Holiday: Marks holidays based on both official and unofficial holidays in India.

Is Promotion: Marks promotional periods (e.g., discounts or special events).

Day of Week: Numeric representation of the day of the week (0 for Monday to 6 for Sunday).

Month: The month of the order.

It also handles outlier detection and removal using the IQR method.

The final dataset is saved as Pizza_Sale_fimp.xlsx.

Usage

python fimp.py

Feature Engineering (imp_fea.py)

This script processes the cleaned data and generates new features:

Total Quantity: Aggregates the total quantity of pizzas ordered by pizza_name_id, order_date, and pizza_size.

Is Weekend: A binary flag indicating if the order was placed on a weekend.

Is Holiday: Marks holidays based on both official and unofficial holidays in India.

Is Promotion: Marks promotional periods (e.g., discounts or special events).

Day of Week: Numeric representation of the day of the week (0 for Monday to 6 for Sunday).

Month: The month of the order.

It also handles outlier detection and removal using the IQR method.

The final dataset is saved as Pizza_Sale_imp_fea.xlsx.

Usage

python imp_fea.py

Prediction (por.py)

This script builds predictive models using Prophet and Random Forest for each unique pizza and performs the following tasks:

Splits the data into training and test sets (pre-2016 and post-2016).

Trains the Prophet model with custom regressors (is_promotion, is_weekend, etc.).

Trains a Random Forest regressor using the same features.

Combines predictions from both models using an ensemble approach.

Outputs the predicted sales for specific dates (January 1-7, 2016).

The results are saved as prophet_sales_forecast_results.txt.

Usage

python por.py

Forecast Results Extraction (pred_prop.py)

This script reads the prophet_sales_forecast_results.txt file and processes the predicted data for better readability and future usage in the ingredients prediction process.

It extracts the results of predicted quantities for each pizza and formats the output.

Usage

python pred_prop.py

Ingredients Calculation (ing.py)

This script is responsible for calculating the quantity of each ingredient required for the predicted pizza orders. 

It works as follows:

It uses the predicted pizza sales generated by pred_prop.py.

It maps each pizza to its corresponding ingredients (e.g., dough, cheese, toppings).

The script aggregates the ingredient quantities needed for all pizzas in the forecast period (January 1-7, 2016).

The final list of required ingredients is saved as Ingredients_Forecast.xlsx.

Usage

python ing.py

Ingredients Prediction (ingredients_list_predicted.py)

This script calculates the required quantities of ingredients based on the predicted pizza sales.

Uses the predicted sales quantities from the Prophet and Random Forest ensemble.

Maps each pizza to its required ingredients.

Aggregates the total quantities of each ingredient required for the predicted date range (January 1-7, 2016).

Saves the final ingredient forecast to Ingredients_Forecast.xlsx.

Usage

python ingredients_list_predicted.py

Conclusion

This project provides an end-to-end system for predicting pizza sales and generating purchase orders for ingredients. 
By leveraging machine learning models such as Prophet and Random Forest, the project aims to optimize Domino's ingredient procurement process, reducing waste while ensuring sufficient stock levels.

