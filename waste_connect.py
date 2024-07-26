import streamlit as st
import pandas as pd
from datetime import datetime

# Define the areas in Chennai
areas = ["Adyar", "Anna Nagar", "T. Nagar", "Kodambakkam", "Mylapore", "Royapettah", "Velachery", "Nungambakkam", 
         "Alwarpet", "Besant Nagar", "Saidapet", "Thiruvanmiyur", "Perambur", "Egmore", "Guindy",
         "Pallavaram", "Chromepet", "Tambaram", "Porur", "Madipakkam"]

# Function to load existing data
@st.cache_data
def load_data():
    xlsx_path = 'waste_data.xlsx'
    try:
        waste_data = pd.read_excel(xlsx_path, engine='openpyxl', index_col=0)
    except FileNotFoundError:
        # Initialize an empty DataFrame with columns for areas
        columns = [f"{area} Dry Waste" for area in areas] + [f"{area} Wet Waste" for area in areas]
        waste_data = pd.DataFrame(columns=columns, index=pd.date_range(start="2024-01-01", end=datetime.today()))
    # Convert the index to datetime, handling any errors
    waste_data.index = pd.to_datetime(waste_data.index, errors='coerce')
    # Drop any rows with invalid datetime index
    waste_data = waste_data.dropna(how='all', subset=waste_data.columns)
    return waste_data

# Function to save data
def save_data(waste_data):
    xlsx_path = 'waste_data.xlsx'
    waste_data.to_excel(xlsx_path, engine='openpyxl')
    

# Load existing data
waste_data = load_data()

# Define product suggestions for different waste types
product_suggestions = {
    "Plastic Waste": {
        "Product": "Reusable Grocery Bags",
        "Description": "Durable and eco-friendly alternative to single-use plastic bags."
    },
    "Food Waste": {
        "Product": "Compost Bin",
        "Description": "Ideal for composting food scraps and creating nutrient-rich soil."
    },
    "Paper Waste": {
        "Product": "Recycled Notebooks",
        "Description": "Notebooks made from recycled paper, perfect for eco-conscious note-taking."
    },
    "Energy Waste": {
        "Product": "LED Light Bulbs",
        "Description": "Energy-efficient light bulbs that reduce electricity consumption."
    },
    "Chemical Waste": {
        "Product": "Eco-friendly Cleaners",
        "Description": "Non-toxic cleaning products that are safe for the environment."
    }
}

# Extract dry and wet waste columns
dry_waste_columns = [col for col in waste_data.columns if 'Dry Waste' in col]
wet_waste_columns = [col for col in waste_data.columns if 'Wet Waste' in col]

# Set up the Streamlit app
st.sidebar.title("Waste Connect")

# Custom CSS to style the buttons to be the same size
st.markdown(
    """
    <style>
    .sidebar .stButton button {
        width: 100%;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state if not already set
if 'menu' not in st.session_state:
    st.session_state['menu'] = 'Home'

# Add sidebar buttons for each menu option
if st.sidebar.button("Home"):
    st.session_state['menu'] = "Home"
if st.sidebar.button("Areas"):
    st.session_state['menu'] = "Areas"
if st.sidebar.button("Waste Area Input"):
    st.session_state['menu'] = "Waste Area Input"
if st.sidebar.button("Product Suggestion"):
    st.session_state['menu'] = "Product Suggestion"

# Check session state to determine the current menu
menu_option = st.session_state['menu']

if menu_option == "Home":
    st.title("Welcome to Waste Connect")
    st.write("This app helps you track waste data in Chennai and provides eco-friendly product suggestions.")
    st.write("Menu Options:")
    st.write("1. Areas: Enter an area and date to see the amount of waste collected.")
    st.write("2. Waste Area Input: Input dry and wet waste data for your area.")
    st.write("3. Product Suggestion: Select a type of waste to get product recommendations.")

elif menu_option == "Areas":
    st.title("Waste Data by Area")
    waste_data = load_data()  # Reload data to reflect any updates
    area = st.selectbox("Select Area", [col.replace(" Dry Waste", "") for col in dry_waste_columns])
    date = st.date_input("Select Date", value=datetime.today().date(), min_value=waste_data.index.min().date(), max_value=datetime.today().date())
    
    if st.button("Submit"):
        date_str = date.strftime("%Y-%m-%d")
        if pd.Timestamp(date) in waste_data.index:
            dry_waste_amount = waste_data.at[pd.Timestamp(date), f"{area} Dry Waste"]
            wet_waste_amount = waste_data.at[pd.Timestamp(date), f"{area} Wet Waste"]
            total_waste_amount = dry_waste_amount + wet_waste_amount
            st.write(f"On {date_str}, a total of {total_waste_amount:.2f} tons of waste were collected in {area}.")
            st.write(f"  - Dry Waste: {dry_waste_amount:.2f} tons")
            st.write(f"  - Wet Waste: {wet_waste_amount:.2f} tons")
        else:
            st.write("No data available for the selected date.")

elif menu_option == "Waste Area Input":
    st.title("Waste Data Input")

    area = st.selectbox("Select Area", areas)
    date = datetime.today().strftime('%Y-%m-%d')
    st.write(f"Date: {date}")

    dry_waste = st.number_input("Enter Dry Waste (tons)", min_value=0.0, step=0.01)
    wet_waste = st.number_input("Enter Wet Waste (tons)", min_value=0.0, step=0.01)

    if st.button("Submit"):
        dry_col = f"{area} Dry Waste"
        wet_col = f"{area} Wet Waste"

        # Ensure the correct columns exist in the DataFrame
        if dry_col not in waste_data.columns:
            waste_data[dry_col] = 0.0
        if wet_col not in waste_data.columns:
            waste_data[wet_col] = 0.0

        # If the date exists, update the existing values
        if date in waste_data.index:
            waste_data.at[date, dry_col] = waste_data.at[date, dry_col] + dry_waste if not pd.isna(waste_data.at[date, dry_col]) else dry_waste
            waste_data.at[date, wet_col] = waste_data.at[date, wet_col] + wet_waste if not pd.isna(waste_data.at[date, wet_col]) else wet_waste
        else:
            # If the date does not exist, create a new row
            new_row = pd.DataFrame([[dry_waste if col == dry_col else wet_waste if col == wet_col else 0.0 for col in waste_data.columns]], index=[date], columns=waste_data.columns)
            waste_data = pd.concat([waste_data, new_row])

        save_data(waste_data)
        st.success("Data submitted successfully and saved to file.")

    # Display the updated data
    st.write("Updated Waste Data:")
    st.dataframe(waste_data)

elif menu_option == "Product Suggestion":
    st.title("Product Suggestions for Waste Reduction")
    waste_type = st.selectbox("Select Waste Type", list(product_suggestions.keys()))
    suggestion = product_suggestions[waste_type]

    st.write(f"**Product:** {suggestion['Product']}")
    st.write(f"**Description:** {suggestion['Description']}")

    st.write(f"**Product:** {suggestion['Product']}")
    st.write(f"**Description:** {suggestion['Description']}")
