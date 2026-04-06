from groq import Groq
from retriever import retrieve
import streamlit as st

system_prompt= "You are a helpful assistant. Answer only from the provided context. If the answer isn't in the context, say I don't know based on the provided documents.Cite your sources by page number"


def generate_answer(question, k=3):

    # retrieve
    result = retrieve(question, k)

    documents = result["documents"][0]
    metadata = result["metadatas"][0]

    # format context

    context =  ""

    for i in range(len(documents)):
        context += f"[Chunk {i+1}] {documents[i]} (Source: {metadata[i]['source']}, Page: {metadata[i]['page_number']})\n"

    user_message = f"Context:\n{context}\nQuestion:\n{question}"

    api_key = st.secrets["GROQ_API_KEY"]

    client = Groq(api_key=api_key)

    # call ollama
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_message},]
    )

    # return answer
    return response.choices[0].message.content