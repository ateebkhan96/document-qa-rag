import streamlit as st
import os
from generate import generate_answer

from retriever import index_documents

st.title("DocuQuery: Ask anything about your documents")

uploaded_file = st.file_uploader("Choose a file")

file_path = None

if uploaded_file is not None:

    save_dir = "uploaded_files"
    os.makedirs(save_dir, exist_ok=True)

    file_path = os.path.join(save_dir, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    index_documents(file_path)

text_input = st.text_input("Enter your question: ")

submit = st.button("Submit")

if submit:
    st.write(generate_answer(text_input))


