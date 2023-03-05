# streamlit_app.py
import streamlit as st
from google.oauth2 import service_account
import gspread
import pandas as pd

st.title("SheetData")

scope = ["https://www.googleapis.com/auth/spreadsheets"]

# Create a credentials object using the service account info and scope values
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes = scope)
    
# Authorize the connection to Google Sheets using the credentials object
gc = gspread.authorize(credentials)
    
# Open the Google Sheets document with the specified name
sh = gc.open("reg_vendas")
    
# Access the worksheet within the document with the specified name
worksheet = sh.worksheet("rg_vendas") 
          
@st.cache(ttl=60)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows
        

col1, col2 = st.columns([1, 3])

sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

df = pd.DataFrame(rows)

with col1:
    st.header("Data Table")
    st.dataframe(df)
        
     
# If the "Send to Database" button is clicked, execute the send_to_database() function
# col2.write("Save in Shared Cloud?")
# if col2.button("Send to Database"):
#     send_to_database(res)
