from data_ingestion import DataIngestion
from data_cleaning import DataCleaning
from ai_agent import AIAgent

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "demodb"
DB_USER = "postgres"
DB_PASSWORD = "1234"

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

ingestion = DataIngestion(DB_URL)
cleaner = DataCleaning()
ai_agent = AIAgent()

df_csv = ingestion.load_from_csv("data/sample_data.csv")
if df_csv is not None:
    print("\n Cleaning CSV Data...")
    df_csv = cleaner.clean_data(df_csv)
    df_csv_ai_cleaned = ai_agent.process_data(df_csv)
    print("\ AI-cleaned Excel Data:\n", df_excel)

df_db = ingestion.load_from_database("SELECT * FROM my_table;")
if df_db is not None:
    print("\n Cleaning Database Data...")
    df_db = cleaner.clean_data(df_db)
    df_db_ai_cleaned = ai_agent.process_data(df_db)
    print("\n AI-cleaned Database Data:\n", df_db_ai_cleaned)

API_URL = "https://jsonplaceholder.typicode.com/posts"
df_api = ingestion.fetch_from_api(API_URL)
if df_api is not None:
    print("\n Cleaning API Data...")
    df_api = df_api.head(30)
    if "body" in df_api.columns:
        df_api["body"] = df_api["body"].apply(lambda x: x[:100]+"..." if instance(x,str) else x)
        
    df_api = cleaner.clean_data(df_api)
    df_api_ai_cleaned = ai_agent.process_data(df_api)
    print("\n AI-cleaned API Data:\n", df_api_ai_cleaned)