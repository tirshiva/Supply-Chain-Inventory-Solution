"""
interface.py

Streamlit interface for uploading bills and viewing results.
"""
import streamlit as st
import requests

st.title("Smart Inventory Scanner")

uploaded_file = st.file_uploader("Upload Bill Image", type=["jpg", "png", "jpeg"])
bill_type = st.selectbox("Bill Type", ["purchase", "sale"])

if uploaded_file and bill_type:
    files = {"file": uploaded_file.getvalue()}
    data = {"bill_type": bill_type}
    response = requests.post("http://127.0.0.1:8000/inventory/upload-bill/", files={"file": uploaded_file}, data=data)
    if response.ok:
        st.success("Inventory Updated!")
        st.json(response.json())
    else:
        st.error("Failed to process bill.")
