from ETL_psql.Transform.Transform import Transform_df


class TransformProductDf:
    def extra_var(self):
        self.sell_price = self.df['SELL PRICE']
        self.comm_rate  = self.df['COMMISION RATE']
    
    def transform(self) :
        self.df['BRAND'].fillna("Unknown", inplace = True)

        self.df['PRODUCT_SIZE'] = [0 for i in range(len(self.df))]

        self.df['COMMISION'] = self.sell_price * self.comm_rate / 100

