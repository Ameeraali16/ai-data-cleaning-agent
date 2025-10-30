import sys
import os
import pandas as pd
import io
import aiohttp
from fastapi import FastAPI, UploadFile, File, HTTPException
from sqlalchemy import create_engine
from pydantic import BaseModel
import requests

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from scripts.ai_agent import AIAgent #AI agent 
from scripts.data_cleaning import DataCleaning #rule based data cleaning

app = FastAPI()

ai_agent = AIAgent()
cleaner = DataCleaning()

@app.post("/clean-data")
async def clean_data(file: UploadFile = File(...)):
    #Recieves file from UI, cleans it usig rule-based and AI-based methods, returns cleaned data in JSON format.
    try:
        contents = await file.read()
        file_extension = file.filename.split(".")[-1]

        if file_extension == "csv":
            df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        elif file_extension in ["xls", "xlsx"]:
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a CSV or Excel file.")

        df_cleaned = cleaner.clean_data(df)

        df_ai_cleaned = ai_agent.process_data(df_cleaned)

        if isinstance(df_ai_cleaned, str):
            from to import StringIO
            df_ai_cleaned = pd.read_csv(StringIO(df_ai_cleaned))
        
        return {"cleaned_data": df_ai_cleaned.to_dict(orient="records")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during data cleaning: {e}")
    
class DBQuery(BaseModel):
    db_url: str
    query: str

@app.post("/clean-db")
async def clean_db(data: DBQuery):
    try:
        engine = create_engine(data.db_url)
        df = pd.read_sql(data.query, engine)

        df_cleaned = cleaner.clean_data(df)

        df_ai_cleaned = ai_agent.process_data(df_cleaned)

        if isinstance(df_ai_cleaned, str):
            from io import StringIO
            df_ai_cleaned = pd.read_csv(StringIO(df_ai_cleaned))
        
        return {"cleaned_data": df_ai_cleaned.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during database data cleaning: {e}")

class APIRequest(BaseModel):
    api_url: str

@app.post("/clean-api")
async def clean_api(api_request: APIRquest):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_request.api_url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=400, detail="Failed to fetch data from API.")
                data = await response.json()
                df = pd.DataFrame(data)
                df_cleaned = cleaner.clean_data(df)
                df_ai_cleaned = ai_agent.process_data(df_cleaned)
                if isinstance(df_ai_cleaned, str):
                    from io import StringIO
                    df_ai_cleaned = pd.read_csv(StringIO(df_ai_cleaned))
                return {"cleaned_data": df_ai_cleaned.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during API data cleaning: {e}")
    
#run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)