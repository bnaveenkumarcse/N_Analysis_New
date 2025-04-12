import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = r'D:\coderviewsTech.Pvt.ltd\mynotebook\customer_shopping_data.csv'

def read():
    """
    This function is used to read the data for data analysis 
    """
    data = pd.read_csv(file_path)
    return data

def null_duplicates(data):
    """
    Displays null value info and count of duplicate rows.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        dict: Dictionary with null and duplicate info.
    """
    null_info = data.isnull().sum()
    duplicate_count = data.duplicated().sum()
    print("Null Values:\n", null_info)
    print("Duplicate Rows:", duplicate_count)
    return {
        'nulls': null_info,
        'duplicates': duplicate_count
    }

def calculate_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the sales by multiplying quantity and price.

    Args:
        df (pd.DataFrame): DataFrame with columns 'quantity' and 'price'.

    Returns:
        pd.DataFrame: The DataFrame with a new 'sales' column.
    """
    df['sales'] = df['quantity'] * df['price']
    return df

def calculate_average_basket_size(param: pd.DataFrame) -> float:
    """
    Calculates the average basket size (avg number of items per invoice).

    Args:
        df (pd.DataFrame): DataFrame with at least 'invoice_no' and 'quantity' columns.

    Returns:
        float: Average basket size.
    """
    basket_totals = param.groupby('invoice_no')['quantity'].sum()
    avg_size = basket_totals.mean()
    print(f"Average Basket Size: {avg_size:.2f}")
    return avg_size

def calculate_avg_basket_value(param: pd.DataFrame) -> float:
    """
    Calculates the average total value of each order.

    Args:
        param (pd.DataFrame): DataFrame containing 'invoice_no', 'quantity', and 'price' columns.

    Returns:
        float: Average value of orders.
    """
    param = calculate_sales(param) 

    avg_basket_value = param.groupby('invoice_no')['sales'].sum().mean()

    plt.figure(figsize=(8, 5))
    sns.histplot(param.groupby('invoice_no')['sales'].sum(), bins=30, kde=True)
    plt.title('Distribution of Basket Value')
    plt.xlabel('Order Value')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

    return avg_basket_value

def most_frequent_procust_by_gender(param: pd.DataFrame) -> pd.DataFrame:
    """
    Identifies and plots the most frequently purchased category by each gender.
    
    Args:
        df (pd.DataFrame): DataFrame with 'gender' and 'category' columns.

    Returns:
        pd.DataFrame: Top category per gender based on frequency.
    """
    gender_product_counts = param.groupby(['gender', 'category'])['quantity'].sum().reset_index()
    sorted_Data = gender_product_counts.sort_values(by='quantity', ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x='quantity', y='category', hue='gender', data=sorted_Data, palette='coolwarm')
    plt.xlabel('Quantity Sold')
    plt.ylabel('Category')
    plt.title('Top Categories by Quantity Sold')
    plt.legend(title='Gender')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()

    grouped = param.groupby(['gender', 'category']).size().reset_index(name='count')
    top_products = grouped.sort_values(['gender', 'count'], ascending=[True, False]).drop_duplicates('gender')

    print("Most Frequently Purchased Category by Gender:\n", top_products)

    plt.figure(figsize=(8, 5))
    sns.barplot(data=top_products, x='gender', y='count', hue='category', palette='Set2')
    plt.title('Most Frequently Purchased Category by Gender')
    plt.xlabel('Gender')
    plt.ylabel('Purchase Count')
    plt.tight_layout()
    plt.show()

    return top_products

def preprocess_dates(param: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the DataFrame by converting 'invoice_date' to datetime
    and adding separate columns for 'year', 'month', and 'year_month'.

    Parameters:
    ----------
    df : pd.DataFrame
        Input DataFrame with an 'invoice_date' column.

    Returns:
    -------
    pd.DataFrame
        Modified DataFrame with 'invoice_date' in datetime format,
        and new columns: 'year', 'month', and 'year_month'.
    """
    param['invoice_date'] = pd.to_datetime(param['invoice_date'], dayfirst=True, errors='coerce')
    param['year'] = param['invoice_date'].dt.year
    param['month'] = param['invoice_date'].dt.strftime('%B')
    param['year_month'] = param['invoice_date'].dt.to_period('M')
    return param

def get_peak_sales_period(param: pd.DataFrame) -> str:
    """
    Identifies the peak month and year based on the number of sales (invoices)
    and visualizes the monthly sales trend using a line chart.
    """
    param = preprocess_dates(param)

    sales_trend = param.groupby('year_month').size()
    peak_month = sales_trend.idxmax()

    plt.figure(figsize=(12, 6))
    sales_trend.plot(kind='line', marker='o', color='darkcyan', linewidth=2)
    plt.title('Sales Trend Over Time', fontsize=14)
    plt.xlabel('Month-Year')
    plt.ylabel('Number of Invoices')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    print(f"Peak Sales Period: {peak_month}")
    return str(peak_month)

def sales_breakdown_by_year_and_month(param5: pd.DataFrame) -> pd.DataFrame:
    """
    Provides a breakdown of total sales (quantity * price) by year and month.
    Visualizes:
    1. Total Sales by Year (bar chart)
    2. Monthly Sales Trends for Each Year (line chart)

    Parameters:
    ----------
    param5 : pd.DataFrame
        The input DataFrame containing at least the columns 'invoice_date', 
        'quantity', and 'price'.

    Returns:
    -------
    pd.DataFrame
        A pivot table showing the total sales by year and month.
    
    Example:
    -------
    >>> data = read()  # Replace with actual DataFrame loading
    >>> sales_breakdown_by_year_and_month(data)
    """
    param5 = preprocess_dates(param5)
    param5 = calculate_sales(param5) 

    yearly_sales = param5.groupby('year')['sales'].sum().reset_index(name='total_sales')
    monthly_sales = param5.groupby(['year', 'month'])['sales'].sum().reset_index(name='total_sales')
    monthly_sales = monthly_sales.sort_values(by='month')

    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    plt.bar(yearly_sales['year'].astype(str), yearly_sales['total_sales'], color='skyblue')
    plt.xlabel('Year')
    plt.ylabel('Total Sales (₹)')
    plt.title('Total Sales by Year')

    plt.subplot(1, 2, 2)
    for year in monthly_sales['year'].unique():
        subset = monthly_sales[monthly_sales['year'] == year]
        plt.plot(subset['month'], subset['total_sales'], marker='o', label=f'Year {year}')
    
    plt.xlabel('Month')
    plt.ylabel('Total Sales (₹)')
    plt.title('Monthly Sales Trend')
    plt.xticks(range(1, 13))
    plt.legend(title='Year')
    plt.tight_layout()
    plt.show()

    pivot = pd.pivot_table(param5, index='year', columns='month', values='sales', aggfunc='sum').fillna(0)
    return pivot

def highest_sales_month_per_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifies the month(s) with the highest sales for each product category.

    Args:
        df (pd.DataFrame): DataFrame with columns 'invoice_date', 'category', 'quantity', 'price'.

    Returns:
        pd.DataFrame: Top sales months per category.
    """
    df = preprocess_dates(df)
    df = calculate_sales(df) 
    
    monthly_category_sales = df.groupby(['category', 'year_month'])['sales'].sum().reset_index()
    monthly_category_sales['year_month'] = monthly_category_sales['year_month'].astype(str)

    top_months = monthly_category_sales.loc[
        monthly_category_sales.groupby('category')['sales'].idxmax()
    ].sort_values(by='sales', ascending=False)

    plt.figure(figsize=(14, 6))
    sns.lineplot(data=monthly_category_sales, x='year_month', y='sales', hue='category', marker='o')
    plt.title('Monthly Sales Trend by Product Category')
    plt.xlabel('Year-Month')
    plt.ylabel('Sales (₹)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

    return top_months

def payment_method_distribution_by_gender(param7: pd.DataFrame) -> pd.DataFrame:
    """
    Analyzes the distribution of payment methods based on gender.

    Args:
        param7 (pd.DataFrame): DataFrame with columns 'payment_method' and 'gender'.

    Returns:
        pd.DataFrame: Distribution of payment methods by gender.
    """
    payment_gender_distribution = param7.groupby(['payment_method', 'gender']).size().reset_index(name='transaction_count')

    plt.figure(figsize=(10, 6))
    sns.barplot(data=payment_gender_distribution, x='payment_method', y='transaction_count', hue='gender', palette='Set2')
    plt.title('Payment Method Distribution by Gender')
    plt.xlabel('Payment Method')
    plt.ylabel('Transaction Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    return payment_gender_distribution
def total_and_highest_revenue_by_mall(param8: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the total revenue and highest revenue collected by each shopping mall.

    Args:
        param8 (pd.DataFrame): DataFrame containing columns 'shopping_mall', 'quantity', and 'price'.

    Returns:
        pd.DataFrame: DataFrame with total revenue and highest revenue for each shopping mall.
    """
    param8 = calculate_sales(param8)  # Using the calculate_sales function
    
    total_revenue_by_mall = param8.groupby('shopping_mall')['sales'].sum().reset_index(name='total_revenue')
    highest_revenue_by_mall = param8.groupby('shopping_mall')['sales'].max().reset_index(name='highest_revenue')
    
    revenue_data = pd.merge(total_revenue_by_mall, highest_revenue_by_mall, on='shopping_mall')

    plt.figure(figsize=(12, 6))
    sns.barplot(data=revenue_data, x='shopping_mall', y='total_revenue', color='skyblue', label='Total Revenue')
    sns.barplot(data=revenue_data, x='shopping_mall', y='highest_revenue', color='orange', label='Highest Revenue')
    plt.title('Total and Highest Revenue by Shopping Mall')
    plt.xlabel('Shopping Mall')
    plt.ylabel('Revenue (₹)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return revenue_data