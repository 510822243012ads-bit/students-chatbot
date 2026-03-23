import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="GTEC Student Bot", page_icon="🎓", layout="wide")

# 1. Loading the Data
@st.cache_data
def load_data():
    # Try multiple paths in case the file is in the root or the folder
    paths = ["student_chatbot/students.csv", "students.csv"]
    for path in paths:
        try:
            df = pd.read_csv(path)
            # Clean up Column Names (Remove extra spaces)
            df.columns = df.columns.str.strip()
            # Ensure Reg Number is a string (to prevent commas like 5,108...)
            df['Reg. Number'] = df['Reg. Number'].astype(str)
            return df
        except:
            continue
    return None

df = load_data()

if df is not None:
    st.title("🎓 GTEC Staff Assistant")
    st.markdown("---")

    # --- SIDEBAR SUMMARY ---
    st.sidebar.header("Quick Stats")
    st.sidebar.metric("Total Students", len(df))
    
    show_all = st.sidebar.checkbox("Show All Student Records")

    # --- SEARCH SECTION ---
    st.subheader("🔍 Student Search")
    user_query = st.text_input("Search by Name or Registration Number:", "").strip().upper()

    if user_query:
        # Search in both Name and Reg Number columns
        results = df[
            (df['Name of the Student'].str.upper().str.contains(user_query, na=False)) |
            (df['Reg. Number'].str.contains(user_query, na=False))
        ]

        if not results.empty:
            for _, student in results.iterrows():
                with st.expander(f"✅ {student['Name of the Student']} ({student['Reg. Number']})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Parent Name:** {student['Parent Name']}")
                        st.write(f"**Phone No:** {student['Parent Phone No']}")
                        st.write(f"**Aadhar:** {student['Aadhar No']}")
                    with col2:
                        st.write(f"**Apaar ID:** {student['Apaar Id']}")
                        st.write(f"**Mail ID:** {student['Mail id']}")
                        st.write(f"**Address:** {student['Communication Address']}")
        else:
            st.error("❌ No student found with that detail.")

    # --- SHOW ALL DATA ---
    if show_all:
        st.markdown("---")
        st.subheader("Full Student Directory")
        st.dataframe(df, use_container_width=True)

else:
    st.error("🛑 **Error:** Could not find `students.csv`. Please ensure you have uploaded it to GitHub and named it correctly.")
    st.info("Tip: If the file is inside the 'student_chatbot' folder, make sure the path in the code matches.")
