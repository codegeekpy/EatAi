import streamlit as st
from utils.ai import generate_recipe

def show():
    st.title("👨‍🍳 AI Recipe Assistant")
    
    with st.form("ai_recipe_form"):
        ingredients = st.text_input("What ingredients do you have?")
        cuisine = st.selectbox("Cuisine style", ["Andhra", "Telangana", "Hyderabadi"])
        
        if st.form_submit_button("Generate Recipe"):
            with st.spinner("Creating your recipe..."):
                recipe = generate_recipe(f"{ingredients} {cuisine} style")
                st.success("Here's your AI-generated recipe:")
                st.write(recipe)