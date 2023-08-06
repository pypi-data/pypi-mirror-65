"""
This module contains the data pipeline container for organising and 
calcuating the required summary statistics
"""

# Authors: Joseph Moorhouse 
#
# License: BSD 3 clause

import pandas as pd 

# --------------------------------------------------------------------------
# Data pipeline

class SalesPipeline:
    """Backend pipeline for data in sales_analysis/data_pipeline/data
    
    Parameters
    ----------
    data : dict of pd.DataFrame
        dict should contain sales data from 
        sales_analysis/data_pipeline/data. Must include 'commissions.csv', 
        'orders.csv', 'order_lines.csv', 'products.csv', 
        'product_promotions.csv' and 'promotions.csv'

    Attributes
    ----------
    merged_order_data : pd.DataFrame
        Formatted order/orderlines data
    """
    # ----------------------------------------------------------------------
    # Constructors

    def __init__(self, **data):
        for k, v in data.items():
            setattr(self, k.split('.')[0], v)
            
        self.merged_order_data = self._merge_order_data()

    # ----------------------------------------------------------------------
    # formatting methods 
            
    def _format_orders(self, orders):
        "date formatting method for orders.csv"

        orders["created_at"] = pd.to_datetime(orders["created_at"]).dt.date
        return orders
    
    def _merge_order_data(self):
        "Method to combine orders.csv and order_lines.csv"

        orders = self._format_orders(self.orders)
        order_lines = self.order_lines
        
        return order_lines.merge(
            orders, 
            how="left", 
            left_on="order_id", 
            right_on="id",
        )

    # ----------------------------------------------------------------------
    # statistics/calculation methods

    def _customer_count(self):
        "Method to count the total number of unique customers per day"

        orders = self._format_orders(self.orders)
        customer_count = orders.groupby("created_at")["customer_id"].nunique()
        customer_count.name = "customers"
        
        return customer_count
    
    def _total_discount(self):
        "Method to calculate the total discount given per day"

        merged = self.merged_order_data  
        merged["total_discount"] = (
            merged["full_price_amount"] - merged["discounted_amount"])
        
        total_discount = merged.groupby("created_at")["total_discount"].sum()
        total_discount.name = "total_discount_amount"
        
        return total_discount
        
    def _item_count(self):
        "Method to calculate the total number of items sold per day"

        sales_quantity = (self.merged_order_data
                 .groupby("created_at")["quantity"].sum())
        sales_quantity.name = "items"
        
        return sales_quantity
    
    def _mean_order_total(self):
        "Method to calculate the average order amount per day"

        average_daily_order = (self.merged_order_data
                .groupby("created_at")['total_amount'].mean())
        average_daily_order.name = "order_total_avg"
        
        return average_daily_order
    
    def _mean_discount_rate(self):
        "Method to calculate the average discount rate offered per day"

        average_discount_rate = (self.merged_order_data
                .groupby("created_at")["discount_rate"].mean())
        average_discount_rate.name = "discount_rate_avg"
        
        return average_discount_rate

    # ----------------------------------------------------------------------
    # Public methods
    
    def summary(self):  
        """Summary sales statistics per day.
        
        Returns
        -------
        summary: pd.DataFrame
            Summary of the total number of customers, total discount offered,
            total number of items sold, average order amount and the average 
            discount rate offered each day
        """

        summary_df = pd.concat([
            self._customer_count(),
            self._total_discount(),
            self._item_count(),
            self._mean_order_total(),
            self._mean_discount_rate(),
        ], axis=1)
        
        summary_df.index = pd.to_datetime(summary_df.index)
        return summary_df