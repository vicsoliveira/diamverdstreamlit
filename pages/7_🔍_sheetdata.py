# # streamlit_app.py
import streamlit as st
from google.oauth2 import service_account
import gspread
import pandas as pd

import plotly.figure_factory as ff
import plotly.graph_objects as go

from pandas import DataFrame
from gspread_pandas import Spread,Client
from statistics import mean
from datetime import datetime, timedelta



st.title("SheetData")


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

quantcount = vendas_sheet.groupby(['quant'])['quant'].count().reset_index(name='counts')


fig_quant = go.Figure(data=[
    go.Bar(name='Pedidos', x=quantcount['quant'], y=quantcount['counts'])
])

fig_quant.update_layout(title_x = 0.5,
                   title = 'Pedidos',
                  hovermode = 'x',
                   xaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=1
            )
                    )
fig_quant.update_layout(height=300,
                       width=300,
                       margin={'l': 20, 'r': 20, 't': 0, 'b': 0})

i=0
while i < len(vendas_sheet['valor'].tolist()):
         f = str(vendas_sheet.iloc[i]['valor'])
         x = f.replace("R$ ", "").replace(".", "").replace(",", ".")
         x = float(x)
         vendas_sheet['valor'] = vendas_sheet['valor'].replace(f, x)
         i=i+1
         
quantcount2 = vendas_sheet.groupby(['quant'])['valor'].sum().reset_index(name='faturamento')

while i < len(quantcount2['faturamento'].tolist()):
         f = quantcount2.iloc[i]['faturamento']
         x = f'R$ {str(f)}'.replace(".", ",")
         quantcount2['faturamento'] = quantcount2['faturamento'].replace(f, x)
         i=i+1


fig_quant2 = go.Figure(data=[
    go.Bar(name='Pedidos', x=quantcount2['quant'], y=quantcount2['faturamento'])
])

fig_quant2.update_layout(title_x = 0.5,
                   title = 'Faturamento',
                  hovermode = 'x',
                   xaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=1
            )
                    )
fig_quant2.update_layout(height=300,
                       width=300,
                       margin={'l': 20, 'r': 20, 't': 0, 'b': 0})


left_column, right_column = st.columns(2)
left_column.subheader('Frequência de Pedidos')
right_column.subheader('Faturamento por frequência de pedidos')
left_column.plotly_chart(fig_quant)
right_column.plotly_chart(fig_quant2)





vendas_sheet_u = vendas_sheet.drop_duplicates(subset=['nome'], keep= 'last')


nome_vendas_sheet = vendas_sheet_u['nome'].tolist()
idade_vendas_sheet = vendas_sheet_u['idade'].tolist()
data_ult_vendas_sheet = vendas_sheet_u['data ped'].tolist()

vendas_sheet_dat = vendas_sheet[['nome', 'data ped']].copy()



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

i = 0
while i < len(data_i):
         d = data_i[i]
         d1 = list(d.values())
         dt= d1[0]
         if len(dt) > 1:
                  j=0
                  res=[]
                  while j < (len(dt)-1):
                           x = (datetime.strptime(dt[j+1], "%d/%m/%Y") - datetime.strptime(dt[j], "%d/%m/%Y")).days
                           res.append(int(x))
                           j=j +1
                  fremed = round(mean(res), 0)
                  d['fre'] = fremed
                  data_i[i] = d
                  i = i +1
         else:
                  d['fre'] = 0
                  data_i[i] = d
                  i = i +1
                  

i = 0
while i < len(data_i):
         d = data_i[i]
         d1 = list(d.values())
         dt= d1[0]
         u = dt[-1]
         d['ult'] = u
         data_i[i] = d
         i = i +1
         
i = 0
while i < len(data_i):
         d = data_i[i]
         d1 = list(d.values())
         dt= d1[0]
         u = datetime.strptime(dt[-1], "%d/%m/%Y")
         x = u + timedelta(days=d['fre'])
         d['prox'] = x.strftime("%d/%m/%Y")
         data_i[i] = d
         i = i +1


# Update to Sheet
def update_the_spreadsheet(sheetname,dataframe):
    col = ['nome_i','freq', 'data_ult_i', 'data_prox_i']
    spread.df_to_sheet(dataframe[col],sheet = sheetname,index = False)
    st.sidebar.info('Updated to GoogleSheet')


df = load_the_spreadsheet('client_fre')
df.clear()
update_the_spreadsheet('client_fre',df)
i = 0
while i < len(nome_vendas_sheet):
         d = data_i[i]
         d1 = list(d.keys())
         dt1 = d1[0]
         opt = {'nome_i': [dt1], 'freq': [d['fre']], 'data_ult_i': [d['ult']], 'data_prox_i': [d['prox']]} 
         opt_df = DataFrame(opt)
         new_df = df.append(opt_df,ignore_index=True)
         update_the_spreadsheet('client_fre',new_df)
         i = i+1
         
   



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
