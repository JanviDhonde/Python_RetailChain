# -*- coding: utf-8 -*-
"""Project(Python Data cleaning).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1U-VG1sjvpLj_me_18kyuwwmN6hwyRRM7

***Import Libraries***
"""

# Import necesaary libraries
import pandas as pd

trxn = pd.read_csv(r'E:/Internship Studio/Project/Retail_data_Transactions.csv', header=0, encoding='utf-8')

trxn

response = pd.read_csv(r'E:/Internship Studio/Project/Retail_data_Response.csv', header=0, encoding='utf-8')

response

df = trxn.merge(response,on='customer_id',how='left')
df

# features
df.dtypes

df.shape

df.tail()

df.describe()

# Missing Values

df.isnull().sum()

df = df.dropna()

df

# change dtypes

df['trans_date']= pd.to_datetime(df['trans_date'])
df['response']= df['response'].astype('int64')

set(df['response'])

df.info()

# check outliers
# z-score

from scipy import stats
import numpy as np

#calc z score
z_scores = np.abs(stats.zscore(df['tran_amount']))

#set a threshold

threshold= 3

outliers= z_scores>threshold


print(df[outliers])

# check outliers
# z-score

from scipy import stats
import numpy as np

#calc z score
z_scores = np.abs(stats.zscore(df['response']))

#set a threshold

threshold= 3

outliers= z_scores>threshold


print(df[outliers])

import seaborn as sns
import matplotlib.pyplot as plt

sns.boxplot(x=df['tran_amount'])
plt.show()

sns.boxplot(x=df['response'])
plt.show()

# creating new columns

df['month']= df['trans_date'].dt.month

df

# Which 3 months have had the highest transaction amounts?

monthly_sales = df.groupby('month')['tran_amount'].sum()
monthly_sales = monthly_sales.sort_values(ascending=False).reset_index().head(3)
monthly_sales

# Customers having highest num of orders

customer_counts= df['customer_id'].value_counts().reset_index()
customer_counts.columns=['customer_id','count']

# sort

top_5_cus= customer_counts.sort_values(by='count', ascending=False).head(5)
top_5_cus

sns.set(style='darkgrid')

colors = ['yellow', 'blue', 'green', 'red', 'purple']

sns.barplot(x='customer_id',y='count',data=top_5_cus, palette=colors )
plt.title('Top 5 Customers')
plt.savefig('count_plot.png')

# Customers having highest value of orders

customer_sales = df.groupby('customer_id')['tran_amount'].sum().reset_index()

# sort

top_5_sal= customer_sales.sort_values(by='tran_amount', ascending=False).head(5)
top_5_sal

colors = ['yellow', 'blue', 'green', 'red', 'purple']

sns.barplot(x='customer_id',y='tran_amount',data=top_5_sal, palette=colors)
plt.title('Top 5 customers vs tran_amount')
plt.savefig('bar_plot.png')

"""***Advanced Analytics***

***Time Serires Analysis***
"""

df

import matplotlib.dates as mdates

df['month_year'] = df['trans_date'].dt.to_period('M')
df

# Convert the PeriodIndex to DateTimeIndex
monthly_sales = df.groupby('month_year')['tran_amount'].sum()

# Convert PeriodIndex to DateTimeIndex
monthly_sales.index = monthly_sales.index.to_timestamp()

plt.figure(figsize=(12,6))  # Increase the size of the figure
plt.plot(monthly_sales.index, monthly_sales.values)  # Plot the data
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Format the x-axis labels
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))  # Set the x-axis interval
plt.xlabel('Month-Year')
plt.ylabel('Sales')
plt.title('Monthly Sales')
plt.xticks(rotation=45)  # Rotate the x-axis labels
plt.tight_layout()  # Adjust the layout for better visibility
plt.savefig('line_plot.png')
plt.show()

"""***Cohort Segmentation***"""

# Recency will be the maximum of trans_date
recency = df.groupby('customer_id')['trans_date'].max()

# Frequency will be the count of transactions
frequency = df.groupby('customer_id')['trans_date'].count()

# Monetary will be the sum of tran_amount
monetary = df.groupby('customer_id')['tran_amount'].sum()

# Combine all three into a DataFrame
rfm = pd.DataFrame({'recency': recency, 'frequency': frequency, 'monetary': monetary})

rfm

# Customer segmentation

def segment_customer(row):
    if row['recency'].year >= 2012 and row['frequency'] >= 15 and row['monetary'] > 1000:
        return 'P0'
    elif (2011 <= row['recency'].year < 2012) and (10 < row['frequency'] <= 15) and (500 < row['monetary'] <= 1000):
        return 'P1'
    else:
        return 'P2'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

rfm

"""***Churn Analysis***"""

# Count the number of churned and active customers
churn_counts = df['response'].value_counts()

# Plot
churn_counts.plot(kind='bar')
plt.title('Churn counts')
plt.savefig('churn_plot.png')

"""***Analyzing top customers***"""

# Top 5 customers
top_5_customers = monetary.sort_values(ascending=False).head(5).index

# Filter transactions of top 5 customers
top_customers_df = df[df['customer_id'].isin(top_5_customers)]

# Plot their monthly sales
top_customers_sales = top_customers_df.groupby(['customer_id', 'month_year'])['tran_amount'].sum().unstack(level=0)
top_customers_sales.plot(kind='line')
plt.xlabel('Month-Year')
plt.ylabel('Sales')
plt.title('Top 5 customers')
plt.savefig('line_plot1.png')
plt.show()

df.to_csv('Main_data.csv')

rfm.to_csv('Additional_analysis.csv')

# This command will use to insert the graphs into excel workbook

from openpyxl import load_workbook
from openpyxl.drawing.image import Image

# Load Excel file
workbook = load_workbook('Data.xlsx')
sheet = workbook.active

# Insert image
img = Image('line_plot1.png')
sheet.add_image(img, 'A1')

# Save the workbook
workbook.save('your_excel_file_with_plot.xlsx')