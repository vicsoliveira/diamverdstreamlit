# streamlit_app.py
import streamlit as st
from google.oauth2 import service_account
import gspread
import pandas as pd

from pandas import DataFrame

from gspread_pandas import Spread,Client

st.title("SheetData")

# from pysmiles import read_smiles
# # 
# import networkx as nx
# import matplotlib.pyplot as plt

# from datetime import datetime

# Create a Google Authentication connection object
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope,creds=credentials)
spreadsheetname = "reg_vendas"
spread = Spread(spreadsheetname,client = client)

# Check the connection
# st.write(spread.url)
    
sh = client.open(spreadsheetname)


@st.cache()         
def load_the_spreadsheet(sheetname):
    worksheet = sh.worksheet(sheetname)
    df = DataFrame(worksheet.get_all_records())
    return df
vendas_sheet = load_the_spreadsheet('rg_vendas')
st.dataframe(vendas_sheet)

# Update to Sheet
def update_the_spreadsheet(sheetname,dataframe):
    col = ['nome','idade', 'data_ult']
    spread.df_to_sheet(dataframe[col],sheet = sheetname,index = False)
    st.sidebar.info('Updated to GoogleSheet')

nome_vendas_sheet = vendas_sheet['nome'].values.tolist()
idade_vendas_sheet = vendas_sheet['idade'].values.tolist()
data_ult_vendas_sheet = vendas_sheet['data ped'].values.tolist()

opt = {'nome': [nome_vendas_sheet], 'idade': [idade_vendas_sheet], 'data_ult': [data_ult_vendas_sheet]} 
opt_df = DataFrame(opt)
df = load_the_spreadsheet('client_fre')
new_df = df.append(opt_df,ignore_index=True)
update_the_spreadsheet('client_fre',new_df)

# st.info(comp_dict[show_me])
# name = comp_dict['iupac_name']
# st.markdown(name)
# plot = st.checkbox('Canonical Smiles Plot')

# if plot:
#     sm = comp_dict['canonical_smiles']
#     mol = read_smiles(comp_dict['canonical_smiles']) 
#     elements = nx.get_node_attributes(mol, name = "element")
#     nx.draw(mol, with_labels=True, labels = elements, pos=nx.spring_layout(mol))
#     fig , ax = plt.subplots()
#     nx.draw(mol, with_labels=True, labels = elements, pos = nx.spring_layout(mol))
#     st.pyplot(fig)

# add = st.sidebar.checkbox('Add CID')
# if add :  
#     cid_entry = st.sidebar.text_input('New CID')
#     confirm_input = st.sidebar.button('Confirm')
    
#     if confirm_input:
#         now = datetime.now()
#         opt = {'Compound CID': [cid_entry],
#               'Time_stamp' :  [now]} 
#         opt_df = DataFrame(opt)
#         df = load_the_spreadsheet('Pending CID')
#         new_df = df.append(opt_df,ignore_index=True)
#         update_the_spreadsheet('Pending CID',new_df)
