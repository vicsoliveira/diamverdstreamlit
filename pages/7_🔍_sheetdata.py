# streamlit_app.py
import streamlit as st
from google.oauth2 import service_account
import gspread
import pandas as pd

from pandas import DataFrame

from gspread_pandas import Spread,Client

st.title("SheetData")
# # Application Related Module
# import pubchempy as pcp
# from pysmiles import read_smiles
# # 
# import networkx as nx
# import matplotlib.pyplot as plt

# from datetime import datetime

# # Disable certificate verification (Not necessary always)
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

# Create a Google Authentication connection object
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope,creds=credentials)
spreadsheetname = "reg_vendas"
spread = Spread(spreadsheetname,client = client)

# Check the connection
st.write(spread.url)

# st.title("SheetData")

# scope = ['https://spreadsheets.google.com/feeds',
#          'https://www.googleapis.com/auth/drive']

# # Create a credentials object using the service account info and scope values
# credentials = service_account.Credentials.from_service_account_info(
#     st.secrets["gcp_service_account"], scopes = scope)
    
# # Authorize the connection to Google Sheets using the credentials object
# gc = gspread.authorize(credentials)
    
# # Open the Google Sheets document with the specified name
# sh = gc.open("reg_vendas")
    
# # Access the worksheet within the document with the specified name
# worksheet = sh.worksheet("rg_vendas")

# conn = connect()
          
# @st.cache(ttl=60)
# def run_query(query):
#     rows = conn.execute(query, headers=1)
#     rows = rows.fetchall()
#     return rows
        

# col1, col2 = st.columns([1, 3])

# sheet_url = st.secrets["private_gsheets_url"]
# rows = run_query(f'SELECT * FROM "{sheet_url}"')

# df = pd.DataFrame(rows)

# with col1:
#     st.header("Data Table")
#     st.dataframe(df)
        
     
# # If the "Send to Database" button is clicked, execute the send_to_database() function
# # col2.write("Save in Shared Cloud?")
# # if col2.button("Send to Database"):
# #     send_to_database(res)
