import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Hey, Act like an expert in analyzing the content of PDF documents and answering questions based on them. 
Assume that the PDF contains information related to a specific topic, and your task is to provide accurate responses. 
Your expertise should cover a broad range of subjects, and you should consider potential challenges in PDF extraction and question understanding. 
Provide a comprehensive answer structure, including relevant details and context.

prompt: {text}
question: {jd}

I want the response in one single string having the structure
{{"answer": "", "context": ""}}
"""

## streamlit app
st.title("Gen AI Internship")
st.text("Get answers to any question from your document")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")
jd=st.text_area("Ask your question here",help="Please ask your question here")


submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        st.subheader(response)