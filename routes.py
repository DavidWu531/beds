from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/bed_base')
def all_bed_base():
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Base")

    base = cur.fetchall()
    return render_template('base.html', base=base)


@app.route('/bed_base/<int:id>')
def bed_base(id):
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Base WHERE BaseID=?', (id,))

    base = cur.fetchone()
    return render_template('base.html', base=base)


@app.route('/mattress')
def all_mattress():
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Mattress;")

    mattress = cur.fetchall()
    return render_template('mattress.html', mattress=mattress)


@app.route('/mattress/<int:id>')
def mattress(id):
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Mattress WHERE MattressID=?', (id,))

    mattress = cur.fetchone()
    return render_template('mattress.html', mattress=mattress)


@app.route('/blanket')
def all_blanket():
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Blanket')

    blanket = cur.fetchall()
    return render_template('blanket.html', blanket=blanket)


@app.route('/blanket/<int:id>')
def blanket(id):
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Blanket WHERE BlanketID=?', (id,))

    blanket = cur.fetchone()
    return render_template('blanket.html', blanket=blanket)


if __name__ == "__main__":
    app.run(debug=True)
