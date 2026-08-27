import streamlit as st,pandas as pd,plotly.express as px
from login import authenticate
from loan_engine import calculate_risk
from ml_model import predict_default
from chat_assistant import chat
from pdf_generator import create_pdf
from pathlib import Path
if "logged" not in st.session_state: st.session_state.logged=False
if not st.session_state.logged:
 u=st.text_input("User")
 p=st.text_input("Password",type="password")
 if st.button("Login") and authenticate(u,p): st.session_state.logged=True; st.rerun()
 st.stop()
st.title("Smart Loan Approval Assistant")
t1,t2,t3=st.tabs(["Assessment","Dashboard","Chat"])
with t1:
 income=st.number_input("Income",value=80000)
 credit=st.slider("Credit",300,900,750)
 emi=st.number_input("EMI",value=10000)
 if st.button("Analyze"):
  score=calculate_risk(income,credit,emi)
  default=predict_default(income,credit,emi)
  st.metric('Risk Score',score)
  st.metric('Default Risk %',default)
  report=f'Risk Score:{score} Default:{default}%'
  pdf='/mnt/data/loan_report.pdf'
  create_pdf(pdf,report)
  with open(pdf,'rb') as f: st.download_button('Download PDF',f,'loan_report.pdf')
with t2:
 df=pd.read_csv('data/customers.csv')
 st.plotly_chart(px.bar(df,x='Customer',y='Income'))
 st.dataframe(df)
with t3:
 q=st.text_input('Ask AI')
 if q: st.write(chat(q,[80000,750,10000]))
