#Entry point for the application
import streamlit as st
st.markdown("""
    <style>
        /* Import font */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-right: 1px solid #E0E0E0;
        }

        /* Sidebar header text */
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] label {
            color: #2E2E2E;
        }

        /* Main header */
        h1 {
            color: #5B8DEF;
            font-weight: 700;
            text-align: center;
            font-size: 2.2rem;
        }

        /* Subheader */
        h2, h3 {
            text-align: center;
            color: #2E2E2E;
        }

        /* Upload area styling */
        .stFileUploader {
            border-radius: 12px;
            border: 2px dashed #5B8DEF !important;
            padding: 1.2em;
            background-color: #F4F6FB;
        }

        /* Buttons */
        .stButton>button {
            background: linear-gradient(90deg, #5B8DEF 0%, #7BA6F7 100%);
            color: white;
            border: none;
            padding: 0.6em 1.5em;
            border-radius: 8px;
            font-weight: 600;
            transition: 0.3s;
        }

        .stButton>button:hover {
            background: linear-gradient(90deg, #4a78d3 0%, #678ce8 100%);
            transform: translateY(-2px);
        }

        /* Footer text */
        .stMarkdown p {
            text-align: center;
            color: #666;
        }

        /* Divider line */
        hr {
            border: 0;
            height: 1px;
            background: #E0E0E0;
        }

        /* Dataframe section */
        .stDataFrame {
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

import requests
import pandas as pd
import json
from io import StringIO

FASTAPI_URL ="http://127.0.0.1:8000"

st.set_page_config(page_title="AI Data Cleaning Agent", layout="wide")

# Add this right after st.set_page_config(...)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("## 🧹 AI Data Cleaning Agent")
    st.markdown("*Clean your data effortlessly using AI!*")


st.sidebar.header("Data Source Selection")
data_source = st.sidebar.radio(
    "Choose a data source to clean:",
    ["CSV/Excel File", "Database", "API Endpoint"],
    index=0
)

if data_source == "CSV/Excel File":
    st.subheader("Upload your CSV or Excel file")
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xls", "xlsx"])

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1]
        if file_extension == "csv":
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.write("### Original Data")
        st.dataframe(df)

        if st.button("Clean Data"):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            response = requests.post(f"{FASTAPI_URL}/clean-data", files=files)

            if response.status_code == 200:
                st.subheader("Raw API Response (Debugging)")

                try:
                    cleaned_data_raw = response.json()["cleaned_data"]
                    if isinstance(cleaned_data_raw, str):
                        cleaned_data = pd.DataFrame(json.loads(cleaned_data_raw))
                    else:
                        cleaned_data = pd.DataFrame(cleaned_data_raw)

                    st.subheader("Cleaned Data")
                    st.dataframe(cleaned_data)
                except Exception as e:
                    st.error(f"Error parsing cleaned data: {e}")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
elif data_source == "Database":
    st.subheader("Enter Database Query")
    db_url = st.text_input("Database URL", value="postgresql://user:password@localhost:5432/db")
    query = st.text_area("SQL Query", value="SELECT * FROM my_table;")

    if st.button("Clean Data"):
        response = requests.post(f"{FASTAPI_URL}/clean-db", json={"db_url": db_url, "query": query})

        if response.status_code == 200:
            st.subheader("Raw API Response (Debugging)")
            st.json(response.json())

            try:
                cleaned_data_raw = response.json()["cleaned_data"]
                if isinstance(cleaned_data_raw, str):
                    cleaned_data = pd.DataFrame(json.loads(cleaned_data_raw))
                else:
                    cleaned_data = pd.DataFrame(cleaned_data_raw)

                st.subheader("Cleaned Data")
                st.dataframe(cleaned_data)
            except Exception as e:
                st.error(f"Error parsing cleaned data: {e}")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

elif data_source == "API Endpoint":
    st.subheader("Enter API Endpoint")
    api_url = st.text_input("API URL", value="https://jsonplaceholder.typicode.com/posts")

    if st.button("Clean Data"):
        response = requests.post(f"{FASTAPI_URL}/clean-api", json={"api_url": api_url})

        if response.status_code == 200:
            st.subheader("Raw API Response (Debugging)")
            st.json(response.json())

            try:
                cleaned_data_raw = response.json()["cleaned_data"]
                if isinstance(cleaned_data_raw, str):
                    cleaned_data = pd.DataFrame(json.loads(cleaned_data_raw))
                else:
                    cleaned_data = pd.DataFrame(cleaned_data_raw)

                st.subheader("Cleaned Data")
                st.dataframe(cleaned_data)
            except Exception as e:
                st.error(f"Error parsing cleaned data: {e}")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

st.markdown("""
    ---
            Built with Streamlit + FastAPI + OpenAI
    """)

           