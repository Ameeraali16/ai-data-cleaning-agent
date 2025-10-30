import os
import pandas as pd
from sqlalchemy import create_engine
import requests

#this script help us in fetching and loading data from csv, excel, database and apis.

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

class DataIngestion:
    def __init__(self, db_url):
        self.engine = create_engine(db_url) if db_url else None

    def load_csv(self, file_name):
        file_path = os.path.join(DATA_DIR, file_name)
        try:
            data = pd.read_csv(file_path)
            print(f"Loaded data from {file_name} with shape {data.shape}")
            return data
        except Exception as e:
            print(f"Error loading CSV file {file_name}: {e}")
            return None
        
    def load_excel(self, file_name, sheet_name=0):
        file_path = os.path.join(DATA_DIR, file_name)
        try:
            data = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"Loaded data from {file_name} with shape {data.shape}")
            return data
        except Exception as e:
            print(f"Error loading Excel file {file_name}: {e}")
            return None 
    
    def connect_database(self, db_url):
        try:
            self.engine = create_engine(db_url)
            print(f"Connected to database at {db_url}")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            self.engine = None
    
    def load_from_database(self, query):
        if not self.engine:
            print("Database engine is not initialized.")
            return None
        try:
            data = pd.read_sql(query, self.engine)
            print(f"Loaded data from database with shape {data.shape}")
            return data
        except Exception as e:
            print(f"Error loading data from database: {e}")
            return None
    
    def fetch_from_api(self, api_url, params=None):
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data)
            print(f"Fetched data from API with shape {df.shape}")
            return df
        except Exception as e:
            print(f"Error fetching data from API: {e}")
            return None