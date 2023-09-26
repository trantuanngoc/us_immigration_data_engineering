from ETL_psql.Transform.Transform import Transform_df


class TransformShipmentDf:
    def transform(self) :
        self.df['Shipping address'] = [address.split(",")[0] for address in self.df['Destination']]
        self.df['Shipping zipcode'] = [address.split(",")[4] for address in self.df['Destination']]
        self.df['Shipping status'] = self.df['Shipping status'].str.lower()
        self.df.drop_duplicates(subset = ['Order ID'], inplace = True)
        self.df.drop(columns = ['Destination'], inplace = True)

