# AI Agent Script for Data Cleaning and Preprocessing in structured format.
import openai
import pandas as pd
from dotenv import load_dotenv #to load environment variables
import os #system environment variables
from langchain_openai import OpenAI #langchain wrapper for openai
from langchain.graph import stategraph, END #to create state graphs
from pydantic import BaseModel #data validation and settings management

#load API key from env  
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

#define AI Model
llm = OpenAI(openai_api_key=openai.api_key, temperature=0)

class CleaningState(BaseModel):
    input_text: str
    Structured_response: str = ""

class AIAgent:
    def __init__(self):
        self.graph = self.create_graph()
    
    def create_graph(self):
        graph = stategraph.StateGraph(CleaningState)
    
        def agent_logic(state: CleaningState) -> CleaningState:
            response = llm.invoke(state.input_text)
            return CleaningState(input_text=state.input_text, Structured_response=response) 
    
        graph.add_node("cleaning_agent", agent_logic)
        graph.add_edge("cleaning_agent", END)
        graph.set_entry_point("cleaning_agent")
        return graph.complie()

    def process_data(self, df, batch_size=20):
        cleaned_responses = []
        for i in range(0, len(df), batch_size):
            df_batch = df.iloc[i:i+batch_size]

            prompt = f"""You are a data cleaning agent. Analyze the dataset:
            {df_batch.to_String()}

            Indentify the missing value, choose the best imputation strategy (mean, mode, median),
            remove duplicates, and correct data types. 

            Provide the cleaned dataset in a structured format.
            """

            state = CleaningState(input_text=prompt, Structured_response="")
            response = self.graph.invoke(state)

            if isinstance(respose, dict):
                response = cleaningState(**response)
            
            cleaned_responses.append(response.Structured_response)

        return "\n".join(cleaned_responses)