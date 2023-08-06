"""
This module contains the web application to visualise the summary data
from the data pipeline
"""

# Authors: Joseph Moorhouse 
#
# License: BSD 3 clause

from flask import Flask
from datetime import datetime
import os
import pandas as pd

from sales_analysis.data_pipeline._pipeline import SalesPipeline
from sales_analysis.data_pipeline import BASEPATH

# --------------------------------------------------------------------------
# Load and check valid data

FILEPATH = os.path.join(BASEPATH, "data")
DATA_FILES = [f for f in os.listdir(FILEPATH) if f.endswith('.csv')]
REQUIRED_FILES = [
    'commissions.csv', 
    'orders.csv', 
    'order_lines.csv', 
    'products.csv', 
    'product_promotions.csv', 
    'promotions.csv'
]

for file in REQUIRED_FILES:
    if os.path.basename(file) not in DATA_FILES:
        raise FileNotFoundError(f"{os.path.basename(file)} was not found")

DATA = {f : pd.read_csv(os.path.join(FILEPATH, f)) for f in DATA_FILES}

# --------------------------------------------------------------------------
# Web application

sales_app = Flask('sales_analysis')

@sales_app.route('/<selected_date>', methods=['GET'])
def my_view(selected_date):
    date = datetime.strptime(selected_date, "%Y-%m-%d").date()

    sales = SalesPipeline(**DATA)
    sales_summary = sales.summary()

    try:
        daily_data = sales_summary.loc[date]
        return daily_data.to_dict()
    except (KeyError):
        return f"""No data for {date}. Please try 
        another date, such as 2019-08-01"