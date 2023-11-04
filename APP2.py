import streamlit as st
import pandas as pd
# # df=pd.read_excel("rate_database.xlsx",sheet_name="Sheet1")
# @st.cache_data
# def load_data(file_name):
#   return pd.read_csv(file_name)
# df=load_data("Rate.csv")
df=pd.read_csv(file_name)

form=st.sidebar.form("Rate Update")
m_size=form.selectbox(
    "Machine Size",
    ["12x17","23x17", "25x36", "28x40","35x45","40x56"])
# enter_age=form.checkbox("Enable Age")
Col=form.selectbox(
    "Feature",df.columns[1:10]
    # ["12x17","23x17", "25x36", "28x40","35x45","40x56"]
    )
Rate=form.number_input("Rate",)
submitted = form.form_submit_button("Submit")
if submitted:
   try:
    df.loc[df.Machine_size ==m_size,Col]=Rate
    df.to_csv("Rate.csv",index=False)
   except Exception as e:
     print(e)

form1=st.sidebar.form("Rate_Update")
Col=form1.selectbox(
    "Feature",df.columns[10:]
    )
Rate=form1.number_input("Rate",)
submit = form1.form_submit_button("Submit")
if submit:
   try:
    df.loc[:,Col]=Rate
    df.to_csv("Rate.csv",index=False)
   except Exception as e:
     print(e)

st.dataframe(df.iloc[:,:10],hide_index=True)
st.dataframe(df.iloc[:1,10:],hide_index=True)


import streamlit as st

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df)
st.sidebar.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='Rate.csv',
    mime='text/csv',
)
