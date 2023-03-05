# streamlit_app.py



import streamlit as st
from google.oauth2 import service_account
import gspread
import pandas as pd

st.title("SheetData")

def read_from_database(res):
    # Create a list of scope values to pass to the credentials object
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    # Create a credentials object using the service account info and scope values
    credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
    
    # Authorize the connection to Google Sheets using the credentials object
    gc = gspread.authorize(credentials)
    
    # Open the Google Sheets document with the specified name
    sh = gc.open("reg_vendas")
    
    # Access the worksheet within the document with the specified name
    worksheet = sh.worksheet("rg_vendas") 
    
    # Set up a progress bar
    my_bar = st.progress(0)
    
    # Iterate through the rows of the data frame
    for ind in res.index:
        # Calculate the percentage complete
        percent_complete = (ind+1)/len(res) 
        # Update the progress bar
        my_bar.progress(percent_complete)
        
        # Get the values in the first column of the worksheet
        values_list = worksheet.col_values(1)
        # Calculate the next empty row in the worksheet
        length_row = len(values_list)
        
        # Update the cells in the worksheet with the data from the data frame
#         worksheet.update_cell(length_row+1, 1, res['Type'][ind])
#         worksheet.update_cell(length_row+1, 2, str(res['Quantity'][ind]))
#         worksheet.update_cell(length_row+1, 3, str(res['Price'][ind]))
        rows = worksheet.get_all_records()
       
       
    # Return a success message
    return df = pd.DataFrame(rows)
    print(df.head())
    st.success("Updated to Database ", icon="✅")\

# If the "Send to Database" button is clicked, execute the send_to_database() function
# col2.write("Save in Shared Cloud?")
# if col2.button("Send to Database"):
#     send_to_database(res)
