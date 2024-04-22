import psycopg2

class Database:
    def __init__(self, url):
        self.con = psycopg2.connect(url)
        self.cur = self.con.cursor()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255),
                price NUMERIC,
                rating VARCHAR(50)
            );
        """)
        self.con.commit()

    def insert_book(self, book):
        self.cur.execute("INSERT INTO books (title, price, rating) VALUES (%s, %s, %s)", 
                         (book['title'], book['price'], book['rating']))
        self.con.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

# Example usage
with Database(os.getenv('DATABASE_URL')) as db:
    db.create_table()
    for book in books:
        db.insert_book(book)
