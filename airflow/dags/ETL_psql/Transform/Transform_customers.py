from ETL_psql.Transform.Transform import Transform_df

class Transform_customer_df:
    def transform(self):
        self.df.drop(columns=['City', 'State', 'Country'], inplace=True);



