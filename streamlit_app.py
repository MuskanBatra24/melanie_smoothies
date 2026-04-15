# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session

# App title
st.title(f"Customize Your Smoothie 🥤 {st.__version__}")
st.write("Choose the fruits you want in your customer smoothie")

# Input: Name
name_on_order = st.text_input('Name on Smoothie', key="name_input")
st.write('The name on your smoothie will be:', name_on_order)

# Get Snowflake session
session = get_active_session()

# Fetch fruit data and convert to list
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
fruit_list = my_dataframe.to_pandas()['FRUIT_NAME'].tolist()

# Multiselect widget
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5,
    key="ingredients_select"
)

# Process selection
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients)
        VALUES ('{ingredients_string}')
    """

    st.write("SQL to execute:")
    st.code(my_insert_stmt)

    # Submit button
    time_to_insert = st.button('Submit Order', key="submit_button")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ✅')
