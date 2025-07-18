import streamlit as st
import google.generativeai as genai
from streamlit_folium import st_folium
import folium
from folium.plugins import LocateControl

# --- Configuration ---
genai.configure(api_key='AIzaSyAAxxsdh9Jxka2AdvwYfCoBW80LbnvVqME')
model = genai.GenerativeModel('gemini-2.0-flash')

# App title and description
st.title("🍽️ AI Blogger & Reviewer")
st.write("Search for restaurants and cafes, view delivery location, and submit reviews!")

category = ''

# --- Sidebar: Delivery & Ranking ---
with st.sidebar:
    st.header("Delivery & Ranking")
    uber_choice = st.selectbox(
        "Show delivery location?",
        ['No', 'Show Location']
    )
    max_distance = st.slider('Max distance (km)', 1, 30, 10)
    ranking_method = st.radio('Rank by', ['Rating', 'Distance'])

# --- Tabs ---
tab_search, tab_map = st.tabs(["🔍 Search", "🗺️ Map"])

# --- Search Tab ---
with tab_search:
    st.subheader("Search Restaurants & Cafes")

    place = st.selectbox('Type of place', ['Restaurant', 'Cafe', 'Restaurant & Cafe'])

    if place != 'Cafe':
        meal = st.selectbox('Meal', ['Breakfast', 'Lunch', 'Dinner', 'Dessert'])
        options = {
            'Breakfast': ['Egyptian (Foul & Ta3mia)', 'Eggs', 'Milk & Cheese', 'Pastries'],
            'Lunch': ['Fried Chicken', 'Beef', 'Pizza & Pasta', 'Koshary'],
            'Dinner': ['Fried Chicken', 'Beef', 'Pizza & Pasta', 'Koshary'],
            'Dessert': ['Waffle', 'Ice Cream', 'Molten Cake', 'Rice Pudding']
        }[meal]
    else:
        category = st.selectbox('Category', ['Hot drinks','Drinks', 'Cold drinks', 'Desserts'])
        options = {
            'Drinks': ['Tea', 'Coffee', 'Latte'],
            'Hot drinks': ['Tea', 'Hot Chocolate', 'Coffee', 'Latte'],
            'Cold drinks': ['Soda', 'Juice', 'Iced Tea', 'Iced Coffee'],
            'Desserts': ['Waffle', 'Ice Cream', 'Molten Cake', 'Rice Pudding']
        }[category]

    choice = st.selectbox('What would you like?', options)
    city = st.text_input('City')

    st.write('---')
    col1, col2 = st.columns(2)
    with col1:
        min_rating = st.slider('Min Rating', 1, 5, 3)
    with col2:
        price = st.selectbox('Price level', ['Cheap', 'Moderate', 'Expensive'])

    extra = st.text_area('Extra details (optional)')

    if st.button('Search now'):
        prompt = f""" 
                Suggest for me a {place} for {choice} in  
                the "{category}" category with a minimum rating of {min_rating} stars or more.  
                The place should be {price} in price. 
                Give me 5 options in {city} to consider with the following details for each:
                1. Name of the place
                2. Address
                3. Rating (out of 5)
                4. Price range
                5. Specialties
                6. Brief description
                
                Extra notes: {extra}
                
                Please format the response clearly with each restaurant as a separate section.
                """ 
                
        with st.spinner('Searching...'):
            response = model.generate_content(prompt)
            st.write(response.text)

# --- Map Tab ---
with tab_map:
    st.subheader("Delivery Location")

    if 'Show' in uber_choice:
        st.markdown("**📍 Select your delivery location by clicking on the map or enabling location access**")

        # Initialize map centered on Cairo
        m = folium.Map(location=[30.0444, 31.2357], zoom_start=12)

        # Add geolocation button
        LocateControl(auto_start=False).add_to(m)

        # Show the map and allow user to click to select location
        output = st_folium(m, height=500, returned_objects=["last_clicked"])

        # Show selected coordinates if user clicked
        if output["last_clicked"]:
            lat = output["last_clicked"]["lat"]
            lon = output["last_clicked"]["lng"]
            st.success(f"📦 Delivery Location Selected:\nLatitude: {lat:.5f}, Longitude: {lon:.5f}")
        else:
            st.info("Click on the map or use the location button to select your delivery location.")
    else:
        st.info("Select 'Show Location' in the sidebar to view and select the delivery location on the map.")


# Footer
st.write('---')
