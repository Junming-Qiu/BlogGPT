import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content, author, category, img_path) VALUES (?, ?, ?, ?, ?)",
            ('First Post', 'Content for the first post', 'Bob Smith', 'test', '/static/media/test.jpg')
            )

cur.execute("INSERT INTO posts (title, content, author, category) VALUES (?, ?, ?, ?)",
            ('Second Post', 'Content for the second post', 'Bob Smith', 'test')
            )

connection.commit()
connection.close()