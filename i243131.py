import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="EDA Dashboard", layout="wide")
st.title("Exploratory Data Analysis Interface")

# 1. Sidebar: File Upload
st.sidebar.header("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # 2. Dataset Overview
        st.header("Dataset Preview & Metadata")
       

        st.write("**First 5 Rows:**")
        st.dataframe(df.head())
        st.write(f"**Shape:** ({df.shape[0]} , {df.shape[1]} )")
        st.write("**Column Data Types:**")
        st.dataframe(df.dtypes.astype(str))

        st.write("**Missing Values per Column:**")
        st.dataframe(df.isnull().sum())

   

        # 3. Sidebar: Attribute Selection
        st.sidebar.header("Attribute Selection")
        selected_column = st.sidebar.selectbox("Select a column:", df.columns)

        # Detect numerical vs categorical
        if pd.api.types.is_numeric_dtype(df[selected_column]) and df[selected_column].nunique() > 10:
            column_type = "Numerical"
        else:
            column_type = "Categorical"

        # 4. Visualization
        st.subheader("Visualization")
        fig, ax = plt.subplots(figsize=(8, 4))

        if column_type == "Numerical":
            sns.histplot(df[selected_column].dropna(), ax=ax, color="skyblue", edgecolor="black")
            ax.set_title(f"Histogram of {selected_column}")
            ax.set_ylabel("Frequency")
        else:
            counts = df[selected_column].astype(str).value_counts()
            ax.bar(counts.index, counts.values, color="teal", edgecolor="black")
            ax.set_title(f"Frequency of {selected_column}")
            ax.set_ylabel("Count")
            plt.xticks(rotation=45, ha="right")

        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error reading file: {e}")

else:
    st.info("Please upload a CSV file to start EDA.")