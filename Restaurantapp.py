import streamlit as st
import openai
import os

# Load API key securely from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🍽️ AI Restaurant Name & Menu Generator")

cuisine = st.text_input("Enter a cuisine (e.g., Indian, Italian, Arabic)")

if cuisine:
    with st.spinner("Generating..."):
        # Step 1: Generate a restaurant name
        name_prompt = f"I want to open a restaurant for {cuisine} food. Suggest a fancy and creative name."
        name_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": name_prompt}],
            temperature=0.7,
            max_tokens=50
        )
        restaurant_name = name_response['choices'][0]['message']['content'].strip()

        # Step 2: Generate menu items
        menu_prompt = f"Suggest a menu for a {cuisine} restaurant named '{restaurant_name}'. List 5 items with short names."
        menu_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": menu_prompt}],
            temperature=0.7,
            max_tokens=100
        )
        menu_items = menu_response['choices'][0]['message']['content'].strip()

        # Display results
        st.subheader("🍴 Restaurant Name:")
        st.write(restaurant_name)

        st.subheader("🥘 Menu Items:")
        st.write(menu_items)
