import streamlit as st
import openai
import pandas as pd

# Add custom pastel theme using CSS
st.markdown("""
    <style>
    body {
        background-color: #FCE4EC; /* Light pink background */
    }
    .stApp {
        background-color: #FCE4EC;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #4A148C; /* Deep purple for headings */
    }
    .sidebar .sidebar-content {
        background-color: #FFF8E1; /* Light yellow sidebar */
    }
    button {
        background-color: #81D4FA; /* Light blue buttons */
        color: white;
        border-radius: 5px;
        border: none;
        font-size: 16px;
    }
    button:hover {
        background-color: #4FC3F7; /* Slightly darker blue on hover */
    }
    .stTextArea, .stDataFrame {
        background-color: #EDE7F6; /* Light purple for text and tables */
        border: 2px solid #CE93D8; /* Lavender borders */
        border-radius: 10px;
    }
    .download-button {
        background-color: #FFCCBC; /* Light coral for download button */
        color: #BF360C; /* Deep orange text */
        font-size: 16px;
        padding: 10px;
        border-radius: 10px;
        border: none;
    }
    .download-button:hover {
        background-color: #FFAB91; /* Slightly darker coral on hover */
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for OpenAI API key
st.sidebar.header("API Key")
api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")

# App Title
st.title("💖 Cloze Test Generator 💖")

# Input Section
st.header("📜 Input Passage")
passage = st.text_area("Enter the passage to generate cloze test questions:")

# Button to generate cloze test
if st.button("Generate Cloze Test"):
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    elif not passage:
        st.error("Please enter a passage to generate questions.")
    else:
        # Set OpenAI API key
        openai.api_key = api_key
        
        # Prompt engineering for cloze test generation
        prompt = f"""
        Generate 10 cloze test questions from the following passage:
        '{passage}'
        Provide the output in the following format:
        - Question: (Cloze test sentence with blank)
        - Answer: (Correct answer)
        """
        
        try:
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": prompt}]
            )
            
            # Process API response
            content = response.choices[0].message.content.strip()
            questions = []
            for line in content.split("\n"):
                if line.startswith("Question"):
                    q = line.split(":", 1)[1].strip()
                elif line.startswith("Answer"):
                    a = line.split(":", 1)[1].strip()
                    questions.append({"Question": q, "Answer": a})
            
            # Create and display DataFrame
            df = pd.DataFrame(questions)
            st.dataframe(df, width=700, height=400)
            
            # Downloadable CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="💾 Download Questions",
                data=csv,
                file_name="cloze_test.csv",
                mime="text/csv",
                key="download-button",
            )
        
        except Exception as e:
            st.error(f"An error occurred: {e}")
