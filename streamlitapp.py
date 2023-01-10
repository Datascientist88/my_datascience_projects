import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np 
from PIL import Image
from pathlib import Path

path=Path("data")/"datasethospital.xlsx"


st.set_page_config(page_title="HOSPITAL PERFORMANCE DASHBOARD",layout='wide')

#read in the Data 
@st.cache(allow_output_mutation=True)
def get_data():
    df=pd.read_excel(path)
    return df

df=get_data()

# Data preprocessing :
# Remove the white spaces in the Dataframe :
df.columns=df.columns.str.strip()

df['REVENUES CATEGORY']=df['REVENUES CATEGORY'].str.replace(" ","")
# convert the date to datetime format :
df['DATE']=pd.to_datetime(df['DATE'])
# extract the months name :
df['MONAT']=df['DATE'].dt.month_name()
# now we format the dashboard components:
# order the months in chronological order 
lis= ['January','February','March','April','May','June','July','August','September','October','November','December']
df['MONAT']=pd.Categorical(df['MONAT'],categories=lis,ordered=True)

st.sidebar.title('HOSPITAL PERFORMANCE DASHBOARD')
img=Image.open("index.jpg")

st.sidebar.image(img)
# create a radio button :
choice=st.sidebar.radio('Choose the Revenue Category:',df['REVENUES CATEGORY'].unique())

 # filter the data to be visualized :
filtered_df=df[df['REVENUES CATEGORY']==choice].groupby('MONAT')['TOTAL REVENUES'].sum().reset_index()

# create the Layout for the dashboard :
chart1 ,chart2,=st.columns(2)
with chart1:
    fig1=px.line(data_frame=filtered_df,x='MONAT',y='TOTAL REVENUES',title="monthly revenue trends",width=700,template='plotly')
    st.plotly_chart(fig1)
    
filtered_df2=df[df['REVENUES CATEGORY']==choice].groupby('MONAT')['PATIENTS'].sum().reset_index()
    

with chart2:
    fig2=px.bar(data_frame=filtered_df2,x='MONAT',y='PATIENTS',title="monthly number of patients " ,color='PATIENTS' ,width=700,template='plotly')
    st.plotly_chart(fig2)
    
# create another columns
chart3 ,chart4=st.columns(2)


with chart3:
    filtered_df3=df[df['REVENUES CATEGORY']==choice].groupby('MONAT')['CASH','CREDIT'].sum().reset_index()
    fig3=px.line(data_frame=filtered_df3,x='MONAT',y=['CASH' ,'CREDIT'],title="cash to credit breakdown",width=700,template='plotly')
    st.plotly_chart(fig3)

with chart4:
    # create radio button to make the visual Dynamic:
    vizchoice=st.radio("Choose The Visualization Type:",['Scatterplot','Bar Chart'],horizontal=True)
    filtered_df4=df[df['REVENUES CATEGORY']==choice].groupby(['MONAT','CLINIC'])['TOTAL REVENUES','PATIENTS'].sum().reset_index().sort_values(by="TOTAL REVENUES")
    filtered_df5=df[df['REVENUES CATEGORY']==choice].groupby(['MONAT','CLINIC'])['TOTAL REVENUES'].sum().reset_index()
#create scatter chart 
    if vizchoice=='Scatterplot':
        fig4=px.scatter(data_frame=filtered_df4,x='TOTAL REVENUES',y='PATIENTS',animation_frame='MONAT',animation_group='CLINIC',size='PATIENTS',color='TOTAL REVENUES'
,hover_name="CLINIC",log_x=True,width=800,template='plotly',title='The Relationship between number of Patients and Revenues')
        st.plotly_chart(fig4)
    if vizchoice=='Bar Chart':
        fig5=px.bar(data_frame=filtered_df5,x='CLINIC',y='TOTAL REVENUES',animation_frame='MONAT',animation_group='CLINIC',color='TOTAL REVENUES'
,hover_name="CLINIC",width=800,template='plotly',title='Total Revenues Per Clinic')
        st.plotly_chart(fig5)