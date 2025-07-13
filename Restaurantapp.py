
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

import os

# ✅ Use st.secrets to load your API key securely (Streamlit Cloud)
# Or use this in Colab: os.environ["OPENAI_API_KEY"] = getpass("Enter API key:")
import openai
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🍽️ AI Restaurant Name & Menu Generator")

cuisine = st.text_input("Enter a cuisine (e.g., Indian, Italian, Arabic)")

if cuisine:
    llm = OpenAI(temperature=0.7)

    # Chain 1: Generate restaurant name
    prompt_template_name = PromptTemplate(
        input_variables=['cuisine'],
        template="I want to open a restaurant for {cuisine} food. Suggest a fancy name."
    )
    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="restaurant_name")

    # Chain 2: Generate menu items
    prompt_template_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="Suggest some menu items for {restaurant_name}. Return it as a comma-separated list."
    )
    food_items_chain = LLMChain(llm=llm, prompt=prompt_template_items, output_key="menu_items")

    # Combine chains
    sequential_chain = SequentialChain(
        chains=[name_chain, food_items_chain],
        input_variables=['cuisine'],
        output_variables=['restaurant_name', 'menu_items'],
        verbose=False
    )

    response = sequential_chain({'cuisine': cuisine})

    st.subheader("🍴 Restaurant Name:")
    st.write(response['restaurant_name'])

    st.subheader("🥘 Menu Items:")
    for item in response['menu_items'].split(","):
        st.write("- " + item.strip())
