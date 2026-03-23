import streamlit as st
import pandas as pd

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Restaurant Booking", layout="wide")

# -------------------------------
# Advanced Styling (VISIBLE + INTERACTIVE)
# -------------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.card {
    background: linear-gradient(135deg, #1f2937, #111827);
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    color: white;
    border: 1px solid #2d3748;
    transition: 0.3s;
}

.card:hover {
    transform: scale(1.02);
    box-shadow: 0px 8px 20px rgba(0,0,0,0.5);
}

.title {
    font-size: 26px;
    font-weight: bold;
}

.subtitle {
    color: #9ca3af;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Title
# -------------------------------
st.markdown('<p class="title">🍽️ Find & Book Restaurants</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover the best restaurants based on your taste</p>', unsafe_allow_html=True)

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Zomato_data.csv")

    df['rate'] = df['rate'].astype(str).str.replace('/5', '', regex=False)
    df['float_ratings'] = pd.to_numeric(df['rate'], errors='coerce')

    df['approx_cost(for two people)'] = df['approx_cost(for two people)'].astype(str)
    df['approx_cost(for two people)'] = df['approx_cost(for two people)'].str.replace(',', '')
    df['approx_cost(for two people)'] = pd.to_numeric(df['approx_cost(for two people)'], errors='coerce')

    return df

df = load_data()

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("🔍 Filters")

rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.5)
cost = st.sidebar.slider("Max Cost for Two", 100, 5000, 1000)

restaurant_type = st.sidebar.selectbox(
    "Restaurant Type",
    df['listed_in(type)'].dropna().unique()
)

# -------------------------------
# Apply Filters
# -------------------------------
filtered_df = df[
    (df['float_ratings'] >= rating) &
    (df['approx_cost(for two people)'] <= cost) &
    (df['listed_in(type)'] == restaurant_type)
]

# -------------------------------
# Results
# -------------------------------
st.markdown("## 🍴 Available Restaurants")

if filtered_df.empty:
    st.warning("No restaurants found. Try changing filters.")
else:
    for index, row in filtered_df.head(10).iterrows():

        name = row.get('name', 'Restaurant')
        rating_val = row.get('float_ratings', 'N/A')
        cost_val = row.get('approx_cost(for two people)', 'N/A')

        location = (
            row.get('location') or
            row.get('address') or
            row.get('city') or
            "Not Available"
        )

        st.markdown(f"""
        <div class="card">
            <h3>{name}</h3>
            <p>⭐ Rating: {rating_val}</p>
            <p>💰 Cost for two: ₹{cost_val}</p>
         
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"🍽️ Book Now - {name}", key=index):
            st.success(f"🎉 Table booked at {name}!")