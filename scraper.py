import requests
from bs4 import BeautifulSoup
import sqlite3

def scrape_books(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = []

    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        rating = book.p['class'][1]
        books.append((title, price, rating))

    return books

def save_to_db(books, db_path='books.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (title TEXT, price TEXT, rating TEXT)''')
    c.executemany('INSERT INTO books (title, price, rating) VALUES (?, ?, ?)', books)
    conn.commit()
    conn.close()

# Main scraping function
base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
for i in range(1, 51):  # Assuming there are 50 pages
    books = scrape_books(base_url.format(i))
    save_to_db(books)
