import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Performance Bot")

# 1. Load the data
@st.cache_data
def load_data():
    # Make sure students.csv is in the same folder as app.py
    df = pd.read_csv("C:/Users/sundhar/OneDrive/Desktop/student_chatbot/students.csv") 
    df['Reg. Number'] = df['Reg. Number'].astype(str)
    return df

try:
    df = load_data()

    st.title("🎓 Staff Assistant Bot")
    st.write("Enter a Name or Reg Number to see student details.")

    # 2. Chat Input
    query = st.text_input("Search Student:", "").strip().upper()

    if query:
        # Search logic
        result = df[(df['Reg. Number'] == query) | 
                    (df['Name of the Student'].str.upper().str.contains(query, na=False))]

        if not result.empty:
            student = result.iloc[0]
            st.success(f"Found: {student['Name of the Student']}")
            st.write(f"**Parent Name:** {student['Parent Name']}")
            st.write(f"**Phone:** {student['Parent Phone No']}")
            st.write(f"**Address:** {student['Communication Address']}")
        else:
            st.error("No student found. Please check the spelling or Reg No.")

except Exception as e:
    st.error(f"Error loading CSV: Please check if students.csv is in the folder. {e}")
