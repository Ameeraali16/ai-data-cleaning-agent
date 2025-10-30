#we clean data such as handling missing values, removing duplicates, and correcting data types.
import pandas as pd
import numpy as np

class DataCleaning:
    #handles missing values by filling with mean, median, mode or dropping them
    def handle_missing_values(self, df, strategy='mean'): #default argument is mean
        if strategy == 'mean':
            return df.fillna(df.mean())
        elif strategy == 'median':
            return df.fillna(df.median())
        elif strategy == 'mode':
            return df.fillna(df.mode().iloc[0])
        elif strategy == 'drop':
            return df.dropna()
        else:
            raise ValueError("Unsupported strategy. Use 'mean', 'median', 'mode', or 'drop'.")
    
    def remove_duplicates(self, df):
        return df.drop_duplicates()

    def fix_data_types(self, df):
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except ValueError:
                pass
        return df
    
    def clean_data(self, df):
        #this function applies all cleaning steps
        df = self.handle_missing_values(df)
        df = self.remove_duplicates(df)
        df = self.fix_data_types(df)
        return df

        