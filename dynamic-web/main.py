from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import models

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:projectproduction@localhost:5435/production'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# instantiate the db object invoking SQLAlchemy.
db = SQLAlchemy(app)

from admin import admin_page # import admin_page defined in admin.py as Blueprint
app.register_blueprint(admin_page) # register the blueprint in the Flask app

app.secret_key = b'6\xb2\xd7\xf75z\xfaE\xd1\x19G\xd1\x15\xc4\xf5\x7f\x8e1\x94.m\xe1Q\xa6'

@app.route("/")
def home():
    return render_template('home.html', title="Home")

@app.route("/signup/")
def signup():
    return render_template('signup.html')

@app.route("/process-signup/", methods=['POST'])
def process_signup():
    # Let's get the request object and extract the parameters sent into local variables.
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    # let's write to the database
    try:
        user = models.User(firstname=firstname, lastname=lastname, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        # Error caught, prepare error information for return
        information = 'Could not submit. The error message is {}'.format(e.__cause__)
        return render_template('signup.html')
    # If we have gotten to this point, it means that database write has been successful. Let us compose success info
    information = 'Account successfully created!'
    return render_template('signup.html', information=information)

@app.route("/login/")
def login():
    # Save off in session where we should go after login process. Session survives across requests. #Where to go is passed as parameter named next along with the request to /login/ URL.
    session['next_url'] = request.args.get('next', '/') #get the next or use default '/' URL after login
    return render_template('login.html', title="SIGN IN", information="Enter login details")

@app.route("/process-login/", methods=['POST'])
def process_login():
    # Get the request object and the parameters sent.
    email = request.form['email']
    password = request.form['password']
    # call our custom defined function to authenticate user
    if (authenticateUser(email, password)):
        session['username'] = email
        session['userroles'] = 'admin' #just hardcoding for the sake of illustration. This should be read from database.
        return redirect(session['next_url'])
    else:
        error = 'Invalid user or password'
        return render_template('login.html', title="SIGN IN", information=error)

def authenticateUser(email, password):
    # First check to see if the user with the email can be found
    user = models.User.query.filter_by(email=email).first()
    # Notice below that we are using the check_password() function defined in the User class # to check password correctness.
    if user and user.check_password(password):# return True only if both are True.
        return True
    else:
        return False

def logged_in():
    if 'username' not in session:
        return False
    else:
        return True

@app.route("/no-anonymity-here/")
def no_anonymity_here():
    if not logged_in():
        return redirect(url_for('login', next='/no-anonymity-here/'))
    # username in session, continue
    return '''
    You have successfully entered a non-anonymous zone. You are logged in as {}.
    <a href="/">Click here to go to the Home page</a> '''.format(session['username'])

@app.route("/logout/")
def logout():
    session.pop('username', None)  # remove the item with key called username from the session
    session.pop('userroles', None)  # remove the item with key called userroles from the session
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(port=5001) # here we are using a different port so as not to conflict with that allocated to our helloworld.py
