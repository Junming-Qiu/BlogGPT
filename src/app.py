from flask import Flask, render_template, request, url_for, flash, redirect
from flask import Flask, render_template
import sqlite3
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    query = 'SELECT * FROM posts'
    posts = conn.execute(query).fetchall()
    conn.close()
    posts = zip(posts, [i+1 for i in range(len(posts))])

    return render_template('index.html.j2', posts=posts)   

@app.route('/about')
def about():
    return render_template('about.html.j2')

@app.route('/blog/<int:blogID>')
def render_blog_page(blogID):
    conn = get_db_connection()
    query = f'SELECT * from posts WHERE id={blogID}'

    post = conn.execute(query).fetchall()
     
    return render_template('blog_page.html.j2', post=post[0])