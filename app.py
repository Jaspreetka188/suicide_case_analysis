import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="Suicide Dataset Explorer", layout="wide")

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv("sucide_case.csv")

df = load_data()

# Column Descriptions
column_info = {
    "country": "Country where the data was recorded.",
    "year": "Year of the record (1985 to 2016).",
    "sex": "Gender (Male or Female).",
    "age": "Age group (e.g., 15-24 years, 75+ years).",
    "suicides_no": "Total number of suicides for the group.",
    "population": "Population of that age/sex group in the country and year.",
    "suicides/100k pop": "Suicide rate per 100,000 people.",
    "country-year": "Combined field for country and year (used for merging).",
    "gdp_for_year ($)": "GDP of the country for that year (formatted with commas).",
    "gdp_per_capita ($)": "GDP per capita (individual economic measure).",
    "generation": "Generation category (e.g., Boomers, Millennials)."
}

column_table = pd.DataFrame({
    "Column Name": list(column_info.keys()),
    "Description": list(column_info.values())
})
# Initialize session state if not already
if "show_dataset" not in st.session_state:
    st.session_state.show_dataset = False
if "show_columns" not in st.session_state:
    st.session_state.show_columns = False


# --- SIDEBAR ---
st.sidebar.header("Navigation")

# Buttons update session state
if st.sidebar.button("🗃️ Show Dataset"):
    st.session_state.show_dataset = True
if st.sidebar.button(" Show Column Info"):
    st.session_state.show_columns = True

# --- MAIN PAGE ---
st.title("🧠 Global Suicide Dataset Explorer")

st.markdown("""
### This project presents an interactive dashboard that visualizes global suicide trends from 1985 to 2016 using publicly available data. It aims to raise awareness about mental health by uncovering patterns in suicide rates across countries, genders, age groups, and economic indicators such as GDP per capita.

Using an intuitive interface powered by Streamlit, users can explore suicide data across over 100 countries, filter results by demographics, and visualize trends through dynamic charts and maps. The dashboard also explains each column in the dataset for better understanding, making it accessible to both technical and non-technical audiences.

Ultimately, the project serves as a tool for researchers, educators, policymakers, and the public to analyze and reflect on global suicide trends — and to support data-driven discussions on mental health prevention and support.


""")
# Show full dataset if toggled
if st.session_state.show_dataset:
    st.subheader("🗃️ Full Dataset Preview")
    st.dataframe(df, use_container_width=True)
if st.session_state.show_columns:
    st.subheader(" Dataset Column Information")
    st.table(column_table)

# 1. Title
st.title(" Preprocessing on Dataset")

# 2. Column-Wise Issue Table
issue_table = pd.DataFrame({
    "Column Name": [
        "country", "year", "sex", "age", "suicides_no", "population", "suicides/100k pop",
        "country-year", "gdp_for_year ($)", "gdp_per_capita ($)", "generation"
    ],
    "Issues Found": [
        "Clean", "Clean", "clean", "clean",
        "May contain zeros", "Check for outliers", "Check for inf/0 values",
        "Redundant", "String with commas", "Clean", "Some overlaps"
    ],
    "Recommended Fix": [
        "Label encode or group", "Convert to datetime if needed", "Label encode",
        "Map to ordinal scale", "Retain or drop if zero-heavy", "Normalize / scale",
        "Recalculate or clean", "Drop", "Remove commas & convert", "Use directly", "Encode or check logic"
    ]
})
st.subheader(" Preprocessing: Column-wise Issues")
st.table(issue_table)

# 3. Load Raw Data
@st.cache_data
def load_data():
    return pd.read_csv("sucide_case.csv")  # Make sure this file exists in your folder

# 4. Clean Function
@st.cache_data
def clean_dataset(df):
    df = df.copy()
    
    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

    # Convert types
    df['suicides_no'] = pd.to_numeric(df['suicides_no'], errors='coerce')
    df['gdp_per_capita_$'] = pd.to_numeric(df['gdp_per_capita_$'], errors='coerce')

    # Clean GDP for year column
    if 'gdp_for_year_$' in df.columns:
        df['gdp_for_year_$'] = df['gdp_for_year_$'].astype(str).str.replace(r'[\$,]', '', regex=True)
        df['gdp_for_year_$'] = pd.to_numeric(df['gdp_for_year_$'], errors='coerce')

    # Drop HDI column if exists
    df.drop(columns=["hdi_for_year"], errors='ignore', inplace=True)

    # Rename problematic columns
    df.rename(columns={'gdp_per_capita_$': 'gdp_per_capita'}, inplace=True)

    return df

# Load datasets
df_raw = load_data()
df_clean = clean_dataset(df_raw)

# 5. Original Dataset Preview
st.header("1. Original Dataset (Before Cleaning)")
st.dataframe(df_raw.head(10), use_container_width=True)

# 6. Preprocessing Steps
st.header("🔧 2. Preprocessing Steps")
with st.expander("▶️ Show Detailed Cleaning Steps"):
    st.markdown("""
**1️⃣ Basic Info** – Check shape, dtypes  
**2️⃣ Null Values** – Drop or impute if required  
**3️⃣ Duplicates** – Remove if any  
**4️⃣ Convert Data Types** – e.g., GDP columns, suicides  
**5️⃣ Rename/Standardize Columns** – Remove special characters  
**6️⃣ GDP Cleanup** – Remove commas and `$`, convert to numeric  
**7️⃣ Drop Useless Columns** – like `hdi_for_year`  
**
""")

# 7. Cleaned Dataset Preview
st.header(" 3. Cleaned Dataset (After Preprocessing)")
st.dataframe(df_clean.head(10), use_container_width=True)

# 8. CSV Export
st.header(" 4. Download Cleaned Dataset")
csv = df_clean.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Cleaned CSV",
    data=csv,
    file_name="cleaned_suicide_data.csv",
    mime='text/csv'
)
