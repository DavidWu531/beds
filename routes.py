from flask import Flask, render_template, redirect, request, flash, session, \
    get_flashed_messages  # pip install Flask
import sqlite3
from flask_bcrypt import Bcrypt  # pip install Flask-Bcrypt
import os


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.urandom(12)  # Generates 12 random characters for sessions
hashed_password = None


@app.route('/')  # Home Route
def home_page():
    return render_template('home.html')


@app.errorhandler(404)  # 404 Error Page Route
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)  # 500 Error Page Route
def internal_server_error(e):
    return render_template("500.html"), 500


@app.route('/force_500/')  # Force 500 Error Page
def deliberate_error():
    raise Exception("You have forced the internal server error")


# Execute queries in a function for simplicity
def execute_query(query, params=(), fetchone=False, fetchall=False,
                  commit=False):
    conn = sqlite3.connect('beds.db')
    cur = conn.cursor()
    try:  # Execute a query with parameters
        cur.execute(query, params)
        if commit:
            conn.commit()

        if fetchone:
            result = cur.fetchone()
        elif fetchall:
            result = cur.fetchall()
        else:
            result = None
    except sqlite3.Error as e:
        # Return 500 Page when an error occurs
        str(e).split().clear()
        result = None
        return render_template("500.html"), 500
    finally:
        conn.close()
    return result


def robust_limits():
    return {
        "username_min_limit": 6,
        "username_max_limit": 30,
        "password_min_limit": 8,
        "password_max_limit": 64
    }


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
        flash("You are already logged in")
        return redirect("/dashboard")
    else:
        if request.method == 'POST':
            # Get data entered from login form
            username = request.form['username']
            password = request.form['password']

            # Compare and verify data between form and database
            user = execute_query('SELECT * FROM Details WHERE\
                         Username = ?', (username,), fetchone=True)
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
    limits = robust_limits()
    if 'username' in session:
        # Checks whether user is logged in or not
        flash("You are already logged in")
        return redirect("/dashboard")
    else:
        if request.method == 'POST':
            # Get data entered from register form
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm-password']

            # Checks if username contains other characters besides
            # letters and numbers
            if not (username.isalnum() and username.isascii()):
                flash('Username can only contain alphanumeric characters')
                return redirect('/register')

            # Checks if password contains spaces since they're not recommended
            if (password.strip() != password) or (username.strip() !=
                                                  username):
                flash('Usernames and passwords cannot contain whitespaces')
                return redirect('/register')

            # Transforms password into fixed-size string of characters
            hashed_password = bcrypt.generate_password_hash(
                password).decode('utf-8')
            # Add data into database

            try:
                # Checks whether username is unique
                execute_query('INSERT INTO Details (Username, Password)\
                            VALUES (?, ?)', (username, hashed_password),
                              commit=True)
            except sqlite3.IntegrityError:
                # Handle error caused by unique constraint (no equal inputs)
                flash('Username already exists. Please choose a different one')
                return redirect('/register')
            else:
                # Passes arguments to password checking
                if password == confirm_password:
                    # Checks if both password and confirm password are the same
                    flash('User registered successfully!')
                    session['username'] = username
                    return redirect('/dashboard')
                else:
                    # Delete the commit if they're not the same
                    execute_query("DELETE FROM Details WHERE UserID=(SELECT \
                                MAX(UserID) FROM Details)", commit=True)

                    flash("Passwords don't match")
                    return redirect('/register')

        return render_template('register.html', **limits)


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
    if 'username' in session:
        session.pop('username', None)
        flash('You have successfully logged out.')
    return redirect("/login")


# Account delete route
@app.route('/delete')
def delete():
    get_flashed_messages()
    if 'username' in session:
        username = session['username']

        # Look for the current username in the database and deletes it
        try:
            execute_query('DELETE FROM Details WHERE Username=?', (username,),
                          commit=True)
        except TypeError:
            return render_template("404.html"), 404
        else:
            session.pop('username', None)
        # Signs the user out after the account is deleted
            flash("Account successfully deleted")
    return redirect("/login")


# Bed Base Route
@app.route('/bed_base/', defaults={"id": None})
# Get all or one data from bed base table depending on id
@app.route('/bed_base/<int:id>')
# Ensures that id can be empty as well to allow redirecting
def bed_base(id):
    base = None
    if id is None:
        # Checks if id is empty and redirects to id=0
        return redirect("/bed_base/0")
    elif id == 0:
        # Grabs everything if id is 0
        # Else grab individual data
        base = execute_query('SELECT * FROM Base', fetchall=True)
        return render_template('all_base.html', base=base)
    else:
        try:
            base = execute_query('SELECT * FROM Base WHERE BaseID=?', (id,),
                                 fetchone=True)
        except OverflowError:
            return render_template('404.html'), 404

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
    mattress = None
    if id is None:
        # Checks if id is empty and redirects to id=0
        return redirect("/mattress/0")
    elif id == 0:
        # Grabs everything if id is 0
        # Else grab individual data
        mattress = execute_query('SELECT * FROM Mattress', fetchall=True)
        return render_template('all_mattress.html', mattress=mattress)
    else:
        try:
            mattress = execute_query('SELECT * FROM Mattress WHERE \
                                     MattressID=?', (id,), fetchone=True)
        except OverflowError:
            return render_template('404.html'), 404

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
    blanket = None
    if id is None:
        # Checks if id is empty and redirects to id=0
        return redirect("/blanket/0")
    elif id == 0:
        # Grabs everything if id is 0
        # Else grab individual data
        blanket = execute_query('SELECT * FROM Blankets', fetchall=True)
        return render_template('all_blanket.html', blanket=blanket)
    else:
        try:
            blanket = execute_query('SELECT * FROM Blankets WHERE BlanketID=?',
                                    (id,), fetchone=True)
        except OverflowError:
            return render_template('404.html'), 404

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
    combo = None
    if id is None:
        # Checks if id is empty and redirects to id=0
        return redirect("/combos/0")
    elif id == 0:
        # Renders combo input template for inputting combo id
        return render_template('combo_input.html', combo=combo)
    else:
        # Get combo based on id
        try:
            combo = execute_query('SELECT BedCombos.RelationshipID,\
                                Base.*, \
                                Blankets.*, \
                                Mattress.*\
                        FROM BedCombos\
                        JOIN Base ON BedCombos.BaseID = Base.BaseID\
                        JOIN Blankets ON BedCombos.BlanketID = \
                        Blankets.BlanketID\
                        JOIN Mattress ON BedCombos.MattressID = \
                        Mattress.MattressID \
                        WHERE BedCombos.RelationshipID=?', (id,),
                                  fetchone=True)
        except OverflowError:
            return render_template('404.html'), 404

        if combo is None:
            # Returns 404 error page when nothing is found
            # Else returns available data
            return render_template('404.html'), 404
        else:
            return render_template('combo.html', combo=combo)


# Running the website
if __name__ == "__main__":
    app.run(debug=False)
