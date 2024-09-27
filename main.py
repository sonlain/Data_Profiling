import streamlit as st
import pandas as pd
import numpy as np
import io
import openpyxl
from profiling import data_profiling
from io import BytesIO



def features_selection():
    features = ['Data Type',
                'Row Count',
                'Missing (%)',
                'Unique Value Counts',
                'Sample Values' ,
                'Top 5 Values']
    selected_features = st.multiselect(
        "Select Required Features :",
        options=features,
        default=features  
    )
    return selected_features


def upload(df,text):
    uploaded_file = st.file_uploader("Drag and drop a CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file is not None:
        text=str(text_file_name)
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file,na_values=[""], keep_default_na=False)
        else:
            df = pd.read_excel(uploaded_file,na_values=[""], keep_default_na=False)
    return df,text


def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data Profile')
    processed_data = output.getvalue()
    return processed_data

def download():
    st.download_button(
        label="Download Data Profile as an Excel",
        data=excel_data,
        file_name=text_,
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

df=pd.DataFrame({
    'col1': ['A', 'B', '', 'D', np.nan],
    'col2': [1, 2, 3, np.nan, 5],
    'col3': ['NA', '', 'E', np.nan, 'F']
}
)




text='Template Data'
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: blue;'>Data Profiling</h1>", unsafe_allow_html=True)

st.markdown("")
st.markdown(f"<h3 style='text-align: center; color: lightblue;'>User Input</h3>", unsafe_allow_html=True)
l,col1, gap, col2,r = st.columns([0.05,1,0.1,1,0.05])
with col1:
    text_file_name = st.text_input("Enter Your File Name") 
    feature=features_selection()
with col2:
    df,text=upload(df,text)

selected_features_list = list(feature) +['Column Name']

st.markdown("")
st.markdown(f"<h3 style='text-align: center; color: lightblue;'>{text}</h3>", unsafe_allow_html=True)
st.dataframe(df)
ans=data_profiling(df)
ans=ans.loc[:, ans.columns.isin(selected_features_list)]
st.markdown("")
st.markdown(f"<h3 style='text-align: center; color: lightblue;'>Profiled Data</h1>", unsafe_allow_html=True)
st.dataframe(ans)
st.markdown("")
st.markdown(f"<h3 style='text-align: center; color: lightblue;'>Download Data</h1>", unsafe_allow_html=True)
text_=text+'.xlsx'
excel_data = to_excel(ans)
download()



