from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')  # Home Route
def home_page():
    return render_template('home.html')


# All Bed Base Sources: https://thebedshop.co.nz/collections/bed-bases
@app.route('/bed_base')  # All Bed Base Route
def all_bed_base():
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Base")

    base = cur.fetchall()
    return render_template('all_base.html', base=base)


@app.route('/bed_base/<int:id>')  # Individual Bed Base Route
def bed_base(id):
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Base WHERE BaseID=?', (id,))

    base = cur.fetchone()
    return render_template('individual_base.html', base=base)


# All Mattress Sources: https://www.bedsrus.co.nz/collections/mattress-only | https://mattresswarehouse.co.nz/collections/mattresses
@app.route('/mattress')  # All Mattress Route
def all_mattress():
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Mattress;")

    mattress = cur.fetchall()
    return render_template('all_mattress.html', mattress=mattress)


@app.route('/mattress/<int:id>')  # Individual Mattress Route
def mattress(id):
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Mattress WHERE MattressID=?', (id,))

    mattress = cur.fetchone()
    return render_template('individual_mattress.html', mattress=mattress)


# All Blanket Sources: https://www.bedbathntable.co.nz/bed/bed-linen/blankets
@app.route('/blanket')  # All Blanket Route
def all_blanket():
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Blankets')

    blanket = cur.fetchall()
    return render_template('all_blanket.html', blanket=blanket)


# Individual Blanket Route
@app.route('/blanket/<int:id>')
def blanket(id):
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Blankets WHERE BlanketID=?', (id,))

    blanket = cur.fetchone()
    return render_template('individual_blanket.html', blanket=blanket)


# Running the website
if __name__ == "__main__":
    app.run(debug=True)
