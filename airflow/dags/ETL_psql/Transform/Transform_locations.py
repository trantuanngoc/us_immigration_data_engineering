from ETL_psql.Transform.Transform import Transform_df
import pandas as pd
import os


class TransformLocationDf:
    def extra_var(self):
        filePath = os.path.join(self.root_dir, "Customers.csv")
        customer_df = pd.read_csv(filePath);

        filePath = os.path.join(self.root_dir, "Shipments.csv")
        shipment_df = pd.read_csv(filePath);

        self.customer_location = customer_df[['Postal code', 'City', 'State', 'Country']]
        self.shipment_destination = shipment_df['Destination']

    def transform(self):
        addr_arr = [address.split(",") for address in self.shipment_destination]

        location_dict = {};
        location_dict['Postal code'] = [int(address[4]) for address in addr_arr]
        location_dict['City'] = [address[1] for address in addr_arr]
        location_dict['State'] = [address[2] for address in addr_arr]
        location_dict['Country'] = [address[3] for address in addr_arr]

        self.df = pd.concat([self.customer_location, pd.DataFrame(location_dict)])

        self.df.drop_duplicates(subset=['Postal code'], keep='first', inplace=True)

