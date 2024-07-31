from flask import Flask, render_template, redirect, request
import sqlite3

app = Flask(__name__)


@app.route('/')  # Home Route
def home_page():
    return render_template('home.html')


@app.errorhandler(404)  # 404 Error Page Route
def not_found(e):
    return render_template('404.html'), 404


@app.route('/submit', methods=['POST'])  # Gets ComboId from form
def get_combo_id():
    id = request.form.get('cid')
    return redirect("/combos/" + str(id))


# All routes respective to its table except many-to-many relationship table
@app.route('/<string:data>/', defaults={'id': None})
# Ensures that id can be empty as well to allow redirecting
@app.route('/<string:data>/<int:id>')
def routes(data, id):
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    if data == "bed_base":
        # Checks if data is bed base and checks for id
        base = None
        if id is None:
            # Checks if id is empty and redirects to id=0
            return redirect("/bed_base/0")
        elif id == 0:
            # Grabs everything if id is 0
            # Else grab individual data
            cur.execute('SELECT * FROM Base')
            base = cur.fetchall()
            return render_template('all_base.html', base=base)
        else:
            cur.execute('SELECT * FROM Base WHERE BaseID=?', (id,))
            base = cur.fetchone()
            if base is None:
                # Returns 404 error page when nothing is found
                # Else returns available data
                return render_template('404.html'), 404
            else:
                return render_template('individual_base.html', base=base)
    elif data == "mattress":
        # Else if data is mattress and checks for id
        mattress = None
        if id is None:
            # Checks if id is empty and redirects to id=0
            return redirect("/mattress/0")
        elif id == 0:
            cur.execute('SELECT * FROM Mattress')
            mattress = cur.fetchall()
            return render_template('all_mattress.html', mattress=mattress)
        else:
            cur.execute('SELECT * FROM Mattress WHERE MattressID=?', (id,))
            mattress = cur.fetchone()
            if mattress is None:
                # Returns 404 error page when nothing is found
                # Else returns available data
                return render_template('404.html'), 404
            else:
                return render_template('individual_mattress.html', mattress=mattress)
    elif data == "blanket":
        # Else if data is blanket and checks for id
        blanket = None
        if id is None:
            # Checks if id is empty and redirects to id=0
            return redirect("/blanket/0")
        elif id == 0:
            cur.execute('SELECT * FROM Blankets')
            blanket = cur.fetchall()
            return render_template('all_blanket.html', blanket=blanket)
        else:
            cur.execute('SELECT * FROM Blankets WHERE BlanketID=?', (id,))
            blanket = cur.fetchone()
            if blanket is None:
                # Returns 404 error page when nothing is found
                # Else returns available data
                return render_template('404.html'), 404
            else:
                return render_template('individual_blanket.html', blanket=blanket)
    else:
        # Data doesn't match above conditions so returns 404 error page
        return render_template('404.html'), 404


# Many-to-many relationship route
@app.route("/combos/", defaults={'id': None})
@app.route("/combos/<int:id>")
def combos(id):
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    combo = None
    if id is None:
        return redirect("/combos/0")
    elif id == 0:
        return render_template('combo_input.html', combo=combo)
    else:
        cur.execute('SELECT BedCombos.RelationshipID,\
                            Base.*, \
                            Blankets.*, \
                            Mattress.*\
                    FROM BedCombos\
                    JOIN Base ON BedCombos.BaseID = Base.BaseID\
                    JOIN Blankets ON BedCombos.BlanketID = Blankets.BlanketID\
                    JOIN Mattress ON BedCombos.MattressID = Mattress.MattressID\
                    WHERE BedCombos.RelationshipID=?', (id,))
        combo = cur.fetchone()
        if combo is None:
            # Returns 404 error page when nothing is found
            # Else returns available data
            return render_template('404.html'), 404
        else:
            return render_template('combo.html', combo=combo)


# Running the website
if __name__ == "__main__":
    app.run(debug=True)
