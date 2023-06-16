import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content, author) VALUES (?, ?, ?)",
            ('First Post', 'Content for the first post', 'Bob Smith')
            )

cur.execute("INSERT INTO posts (title, content, author) VALUES (?, ?, ?)",
            ('Second Post', 'Content for the second post', 'Bob Smith')
            )

connection.commit()
connection.close()