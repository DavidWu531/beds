from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')  # Home Route
def home_page():
    return render_template('home.html')

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

"""
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
    return render_template('individual_blanket.html', blanket=blanket)"""


@app.route('/<string:data>/<int:id>')
def routes(data, id):
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    if data == "bed_base":
        # All Bed Base Sources: https://thebedshop.co.nz/collections/bed-bases | https://www.thebedroomstore.co.nz/product-category/bedding-more/bed-bases/
        base = None
        if id == 0:
            cur.execute('SELECT * FROM Base')
            base = cur.fetchall()
            return render_template('all_base.html', base=base)
        else:
            cur.execute('SELECT * FROM Base WHERE BaseID=?', (id,))
            base = cur.fetchone()
            return render_template('individual_base.html', base=base)
    elif data == "mattress":
        # All Mattress Sources: https://www.bedsrus.co.nz/collections/mattress-only | https://mattresswarehouse.co.nz/collections/mattresses
        mattress = None
        if id == 0:
            cur.execute('SELECT * FROM Mattress')
            mattress = cur.fetchall()
            return render_template('all_mattress.html', mattress=mattress)
        else:
            cur.execute('SELECT * FROM Mattress WHERE MattressID=?', (id,))
            mattress = cur.fetchone()
            return render_template('individual_mattress.html', mattress=mattress)
    # All Blanket Sources: https://www.bedbathntable.co.nz/bed/bed-linen/blankets
    elif data == "blanket":
        blanket = None
        if id == 0:
            cur.execute('SELECT * FROM Blankets')
            blanket = cur.fetchall()
            return render_template('all_blanket.html', blanket=blanket)
        else:
            cur.execute('SELECT * FROM Blankets WHERE BlanketID=?', (id,))
            blanket = cur.fetchone()
            return render_template('individual_blanket.html', blanket=blanket)
    else:
        return render_template('404.html')
    

# Running the website
if __name__ == "__main__":
    app.run(debug=True)
