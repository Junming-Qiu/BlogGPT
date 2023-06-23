from flask import Flask, render_template, request, url_for, flash, redirect
from flask import Flask, render_template
import sqlite3
app = Flask(__name__)

# Use debugging mode
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

# Connects to query DB
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Shows all posts
@app.route('/')
def index():
    conn = get_db_connection()
    query = 'SELECT * FROM posts'
    posts = conn.execute(query).fetchall()
    conn.close()

    return render_template('index.html.j2', posts=posts)   

# About page (update this)
@app.route('/about')
def about():
    return render_template('about.html.j2')

# Shows individual blog
@app.route('/blog/<int:blogID>')
def render_blog_page(blogID):
    conn = get_db_connection()
    query = f'SELECT * from posts WHERE id={blogID}'

    post = conn.execute(query).fetchall()
    if len(post) == 0:
        return redirect('/')
     
    return render_template('blog_page.html.j2', post=post[0])

# Shows categories of blogs
@app.route('/categories')
def render_categories():
    conn = get_db_connection()
    query = f'SELECT DISTINCT category FROM posts'

    categories = conn.execute(query).fetchall()

    return render_template('category.html.j2', categories=categories)

# Shows all articles of a particular category
@app.route('/categories/<string:category>')
def search_category(category):
    print(category)
    conn = get_db_connection()
    query = f"SELECT * FROM posts WHERE category='{category}'"

    posts = conn.execute(query).fetchall()

    return render_template('index.html.j2', posts=posts)