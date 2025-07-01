import streamlit as st
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("Groq API key not found. Please set the environment variable GROQ_API_KEY.")
else:
    client = Groq(api_key=GROQ_API_KEY)

    def generate_clause(clause_type, context, tone, max_retries=3):
        prompt = f"""
        Write a professional legal clause for the following details:

        Clause Type: {clause_type}
        Context: {context}
        Tone: {tone}

        Ensure the clause is clear, formal, and legally appropriate.
        """
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=300
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                error = str(e).lower()
                if "rate limit" in error and attempt < max_retries - 1:
                    time.sleep((attempt + 1) * 5)
                    continue
                return f"Error: {str(e)}"

    st.title("Legal Clause Generator")

    clause_type = st.text_input("Clause Type (e.g., NDA, Indemnity):")
    context = st.text_area("Context of the Clause:")
    tone = st.selectbox("Tone:", ["Formal", "Concise", "Detailed"])

    if st.button("Generate Clause"):
        if clause_type.strip() == "" or context.strip() == "":
            st.error("Please enter both Clause Type and Context.")
        else:
            with st.spinner("Generating legal clause..."):
                clause = generate_clause(clause_type, context, tone)
                st.subheader("Generated Legal Clause:")
                st.code(clause)
