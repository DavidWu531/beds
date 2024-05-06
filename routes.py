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
    cur.execute("SELECT * FROM Base;")

    return render_template('base.html')


@app.route('/bed_base/<int:id>')
def bed_base(id):
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Base WHERE BaseID=?', (id,))

    base = cur.fetchone()
    return render_template('base.html', base=base)


if __name__ == "__main__":
    app.run(debug=True)
