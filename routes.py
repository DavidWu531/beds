from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')  # Home Route
def home_page():
    return render_template('home.html')


# All Bed Base Source: https://thebedshop.co.nz/collections/bed-bases
@app.route('/bed_base')  # All Bed Base Route
def all_bed_base():
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Base")

    base = cur.fetchall()
    return render_template('base.html', base=base)


@app.route('/bed_base/<int:id>')  # Individual Bed Base Route
def bed_base(id):
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Base WHERE BaseID=?', (id,))

    base = cur.fetchone()
    return render_template('base.html', base=base)


# All Mattress Source: https://www.bedsrus.co.nz/collections/mattress-only | https://mattresswarehouse.co.nz/collections/mattresses
@app.route('/mattress')  # All Mattress Route
def all_mattress():
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Mattress;")

    mattress = cur.fetchall()
    return render_template('mattress.html', mattress=mattress)


@app.route('/mattress/<int:id>')  # Individual Mattress Route
def mattress(id):
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Mattress WHERE MattressID=?', (id,))

    mattress = cur.fetchone()
    return render_template('mattress.html', mattress=mattress)


@app.route('/triangles')  # All Triangle Route
def triangles():
    return render_template('triangles.html')


@app.route('/triangle/<string:direction>/<int:size>')  # Individual Triangle Route
def triangle(direction, size):
    bits = []
    if direction == "up_right" or direction == "down_right":
        if direction == "up_right":
            n = 1

            for i in range(size):
                bits.append(" " * (n - size) + "*" * n)
                n += 1

        elif direction == "down_right":
            n = size

            for i in range(size):
                bits.append(" " * (n - size) + "*" * n)
                n -= 1

        return ('<br>'.join(bits))

    elif direction == "up_pyramid" or direction == "down_pyramid":
        if direction == "up_pyramid":
            n = 1

            for i in range(size):
                bits.append("&nbsp" * (size - n) + "*" * (2 * n - 1))
                n += 1

        elif direction == "down_pyramid":
            n = size

            for i in range(size):
                bits.append("&nbsp" * (size - n) + "*" * (2 * n - 1))
                n -= 1

        return ('<br>'.join(bits))

    elif direction == "diamond":
        for i in range(1, size + 1):
            bits.append("&nbsp" * (size - i) + "*" * (2 * i - 1))
        for i in range(size - 1, 0, -1):
            bits.append("&nbsp" * (size - i) + "*" * (2 * i - 1))

        return ('<br>'.join(bits))


@app.route('/blanket')  # All Blanket Route
def all_blanket():
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Blankets')

    blanket = cur.fetchall()
    return render_template('blanket.html', blanket=blanket)


@app.route('/blanket/<int:id>')  # Individual Blanket Route
def blanket(id):
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Blankets WHERE BlanketID=?', (id,))

    blanket = cur.fetchone()
    return render_template('blanket.html', blanket=blanket)


if __name__ == "__main__":  # Running the website
    app.run(debug=True)
