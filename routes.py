from flask import Flask, render_template, redirect, request, flash, session, \
    get_flashed_messages  # pip install Flask
import sqlite3
from flask_bcrypt import Bcrypt  # pip install Flask-Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "iT's OvEr 9000!!"
hashed_password = None


@app.route('/')  # Home Route
def home_page():
    return render_template('home.html')


@app.errorhandler(404)  # 404 Error Page Route
def not_found(e):
    return render_template('404.html'), 404


# Get combo id submitted by user
@app.route('/cid_submit', methods=['POST'])  # Gets ComboId from form
def get_combo_id():
    id = request.form.get('cid')
    return redirect("/combos/" + str(id))


# Account login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    get_flashed_messages()
    if 'username' in session:
        # Checks whether the user is logged in or not
        return redirect("/dashboard")
    else:
        if request.method == 'POST':
            # Get data entered from login form
            username = request.form['username']
            password = request.form['password']

            # Compare and verify data between form and database
            conn = sqlite3.connect('account.db')
            cur = conn.cursor()
            cur.execute('SELECT * FROM Details WHERE\
                         Username = ?', (username,))
            user = cur.fetchone()
            conn.close()
            # Check if hashed password entered equals
            # Hashed password in database, sign in if true
            if user and bcrypt.check_password_hash(user[2], password):
                session['username'] = username
                flash('You are now logged in')
                return redirect('/dashboard')
            else:
                flash('Invalid username or password')
                return redirect('/login')

        return render_template('login.html')


# Account register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    get_flashed_messages()
    if 'username' in session:
        # Checks whether user is logged in or not
        return redirect("/dashboard")
    else:
        if request.method == 'POST':
            # Get data entered from register form
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm-password']

            # Transforms password into fixed-size string of characters
            hashed_password = bcrypt.generate_password_hash(
                password).decode('utf-8')
            # Add data into database
            conn = sqlite3.connect('account.db')
            cur = conn.cursor()

            try:
                # Checks whether username is unique
                cur.execute('INSERT INTO Details (Username, Password)\
                            VALUES (?, ?)',
                            (username, hashed_password))
                conn.commit()
            except sqlite3.IntegrityError:
                # Handle error caused by unique constraint (no equal inputs)
                flash('Username already exists. Please choose a different one')
                return redirect('/register')
            else:
                # Passes arguments to password checking
                if password == confirm_password:
                    # Checks if both password and confirm password are the same
                    flash('User registered successfully! You can now log in.')
                    return redirect('/login')
                else:
                    # Delete the commit if they're not the same
                    cur.execute("DELETE FROM Details WHERE UserID=(SELECT \
                                MAX(UserID) FROM Details)")
                    conn.commit()
                    conn.close()

                    flash("Passwords don't match")
                    return redirect('/register')

        return render_template('register.html')


# Account dashboard route
@app.route('/dashboard')
def dashboard():
    get_flashed_messages()
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        flash('You need to log in to access the dashboard.')
        return redirect("/login")


# Account logout route
@app.route('/logout')
def logout():
    get_flashed_messages()
    session.pop('username', None)
    flash('You have successfully logged out.')
    return redirect("/")


# Account delete route
@app.route('/delete')
def delete():
    get_flashed_messages()
    username = session['username']

    conn = sqlite3.connect('account.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM Details WHERE Username=?', (username,))
    conn.commit()

    session.pop('username', None)
    flash("Account successfully deleted")
    return redirect("/")


# Bed Base Route
@app.route('/bed_base/', defaults={"id": None})
# Get all or one data from bed base table depending on id
@app.route('/bed_base/<int:id>')
# Ensures that id can be empty as well to allow redirecting
def bed_base(id):
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
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


# Mattress Route
@app.route('/mattress/', defaults={"id": None})
# Get all or one data from mattress table depending on id
@app.route('/mattress/<int:id>')
# Ensures that id can be empty as well to allow redirecting
def mattress(id):
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    mattress = None
    if id is None:
        # Checks if id is empty and redirects to id=0
        return redirect("/mattress/0")
    elif id == 0:
        # Grabs everything if id is 0
        # Else grab individual data
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
            return render_template('individual_mattress.html',
                                   mattress=mattress)


@app.route('/blanket/', defaults={"id": None})
# Get all or one data from blanket table depending on id
@app.route('/blanket/<int:id>')
# Ensures that id can be empty as well to allow redirecting
def routes(id):
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    blanket = None
    if id is None:
        # Checks if id is empty and redirects to id=0
        return redirect("/blanket/0")
    elif id == 0:
        # Grabs everything if id is 0
        # Else grab individual data
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


# Many-to-many relationship route
@app.route("/combos/", defaults={'id': None})
# Get all or one data from many-to-many relationship table depending on id
@app.route("/combos/<int:id>")
# Ensures that id can be empty as well to allow redirecting
def combos(id):
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    combo = None
    if id is None:
        # Checks if id is empty and redirects to id=0
        return redirect("/combos/0")
    elif id == 0:
        # Renders combo input template for inputting combo id
        return render_template('combo_input.html', combo=combo)
    else:
        # Get combo based on id
        cur.execute('SELECT BedCombos.RelationshipID,\
                            Base.*, \
                            Blankets.*, \
                            Mattress.*\
                    FROM BedCombos\
                    JOIN Base ON BedCombos.BaseID = Base.BaseID\
                    JOIN Blankets ON BedCombos.BlanketID = Blankets.BlanketID\
                    JOIN Mattress ON BedCombos.MattressID = \
                    Mattress.MattressID \
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
