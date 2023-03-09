# # streamlit_app.py
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

       
def load_the_spreadsheet(sheetname):
    worksheet = sh.worksheet(sheetname)
    df = DataFrame(worksheet.get_all_records())
    return df
vendas_sheet = load_the_spreadsheet('rg_vendas')
st.dataframe(vendas_sheet)

# Update to Sheet
def update_the_spreadsheet(sheetname,dataframe):
    col = ['nome_i','idade_i', 'data_ult_i']
    spread.df_to_sheet(dataframe[col],sheet = sheetname,index = False)
    st.sidebar.info('Updated to GoogleSheet')

vendas_sheet_u = vendas_sheet.drop_duplicates(subset=['nome'], keep= 'last')


nome_vendas_sheet = vendas_sheet_u['nome'].tolist()
idade_vendas_sheet = vendas_sheet_u['idade'].tolist()
data_ult_vendas_sheet = vendas_sheet_u['data ped'].tolist()

vendas_sheet_dat = vendas_sheet[['nome', 'data ped']].copy()


st.write(vendas_sheet_dat)
data_u = []
for name in nome_vendas_sheet:
         rows = vendas_sheet_dat.loc[vendas_sheet_dat['nome'] == name]
         data_u.append(rows['data ped'].tolist())
         data_u.append(rows['nome'].tolist())
data_i = []
i=0
while i < (2*len(nome_vendas_sheet)):
         n = data_u[i+1]
         n1 = n[0]
         n2 = data_u[i]
         data_i.append({n1 : n2})
         i=i +2

d = data_i[0]


st.write(data_i)
st.write(d)         


# i = 0
# while i < len(nome_vendas_sheet):
#          opt = {'nome_i': [nome_vendas_sheet[i]], 'idade_i': [idade_vendas_sheet[i]], 'data_ult_i': [data_ult_vendas_sheet[i]]} 
#          opt_df = DataFrame(opt)
#          df2 = load_the_spreadsheet('client_fre')
#          new_df = df2.append(opt_df,ignore_index=True)
#          i = i+1
#          update_the_spreadsheet('client_fre',new_df)

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
