import streamlit as st
import pandas as pd
from db import Database
import os
from dotenv import load_dotenv

load_dotenv()

st.title('Books Catalog')

# Database query functionality
@st.cache
def get_books():
    with Database(os.getenv('DATABASE_URL')) as db:
        return pd.read_sql('SELECT * FROM books', db.con)

df_books = get_books()
name = st.text_input('Search by book name')
if name:
    df_books = df_books[df_books['title'].str.contains(name, case=False, na=False)]

st.dataframe(df_books)

# For filtering and ordering
rating = st.selectbox('Filter by rating', ['All'] + sorted(df_books['rating'].unique()))
if rating != 'All':
    df_books = df_books[df_books['rating'] == rating]

price_order = st.selectbox('Order by price', ['Ascending', 'Descending'])
if price_order == 'Ascending':
    df_books = df_books.sort_values(by='price', ascending=True)
elif price_order == 'Descending':
    df_books = df_books.sort_values(by='price', ascending=False)

st.dataframe(df_books)
