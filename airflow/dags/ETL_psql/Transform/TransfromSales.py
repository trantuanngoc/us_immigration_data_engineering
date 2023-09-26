from ETL_psql.Transform.Transform import Transform_df
from datetime import datetime
import pandas as pd
import os


class TransformSaleDf:
    def extra_var(self):
        filePath = os.path.join(self.root_dir, "Products.csv")
        prod_arr = pd.read_csv(filePath)

        prod_arr = [(prod_arr['PRODUCT_ID'][i],
                     prod_arr['SELL PRICE'][i],
                     prod_arr['COMMISION RATE'][i]) for i in range(len(prod_arr))]

        self.prod_arr = sorted(prod_arr, key=lambda x: x[0])
        self.n = len(self.df)
        self.product = list(self.df['Product ID'])
        self.quantity = list(self.df['Quantity'])

    def search_product(self, sale_prod_id):
        l = 0
        r = len(self.prod_arr) - 1

        while (l <= r):
            mid = int((l + r) / 2)
            prod_id, prod_price, prod_comm_rate = self.prod_arr[mid]

            if (prod_id > sale_prod_id):
                r = mid - 1
            elif (prod_id < sale_prod_id):
                l = mid + 1
            else:
                return prod_price, prod_comm_rate

    def transform(self):
        self.df['Date'] = [datetime.strptime(date, "%m-%d-%y").date()
                           for date in self.df['Date']]

        revenue_arr = [self.search_product(self.product[i]) for i in range(self.n)]

        self.df['Total cost'] = [val[0] * self.quantity[i]
                                 for i, val in enumerate(revenue_arr)]
        self.df['Profit'] = [(val[0] * val[1] / 100) * self.quantity[i]
                             for i, val in enumerate(revenue_arr)]
