# Customer Shopping Data Analysis

This project performs data analysis on customer shopping data, including operations such as calculating sales, analyzing shopping patterns, identifying trends, and visualizing results. It uses Python with libraries like Pandas, Matplotlib, and Seaborn to perform various tasks.

## Features

### 1. Data Reading and Preprocessing
- `read()`: Reads the customer shopping data from a CSV file.
- `preprocess_dates()`: Converts the 'invoice_date' column to datetime and adds 'year', 'month', and 'year_month' columns for easier analysis.

### 2. Null and Duplicate Handling
- `null_duplicates()`: Checks and displays null values and duplicate rows in the dataset.

### 3. Sales Calculation
- `calculate_sales()`: Calculates sales by multiplying 'quantity' and 'price' columns, adding a 'sales' column to the DataFrame.

### 4. Basket Size and Value Analysis
- `calculate_average_basket_size()`: Calculates the average number of items per invoice.
- `calculate_avg_basket_value()`: Calculates the average value of each order and visualizes the distribution of basket values.

### 5. Gender-Based Analysis
- `most_frequent_procust_by_gender()`: Identifies the most frequently purchased product categories by gender and visualizes the data.

### 6. Sales Trend Analysis
- `get_peak_sales_period()`: Identifies the peak sales period based on the number of invoices and visualizes the monthly sales trend.
- `sales_breakdown_by_year_and_month()`: Provides a breakdown of total sales by year and month, including visualizations of sales trends.

### 7. Category-Specific Analysis
- `highest_sales_month_per_category()`: Identifies the month with the highest sales for each product category and visualizes the trend.

### 8. Payment Method Distribution
- `payment_method_distribution_by_gender()`: Analyzes the distribution of payment methods by gender and visualizes the data.

## Requirements

- Python 3.x
- Pandas
- Matplotlib
- Seaborn

You can install the required libraries using the following command:

```bash
pip install pandas matplotlib seaborn
