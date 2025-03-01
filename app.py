import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Initialize app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class Participant(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    wishlist = db.Column(db.Text, nullable=True)

# Admin model (static for simplicity)
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = bcrypt.generate_password_hash("adminpass").decode('utf-8')

# User loader
@login_manager.user_loader
def load_user(user_id):
    return Participant.query.get(int(user_id))

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        if email == ADMIN_EMAIL:
            flash("You cannot register as admin. Please use a participant email.", "danger")
            return redirect(url_for('register'))

        existing_user = Participant.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please log in instead.', 'danger')
            return redirect(url_for('login'))

        new_user = Participant(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == ADMIN_EMAIL:
            if bcrypt.check_password_hash(ADMIN_PASSWORD, password):
                flash('Admin login successful.', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Admin login failed. Check your password.', 'danger')
                return redirect(url_for('login'))

        user = Participant.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check email and/or password.', 'danger')

    return render_template('login.html')

# Participant dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.email == ADMIN_EMAIL:
        flash("Admins cannot access the participant dashboard.", "danger")
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        wishlist = request.form['wishlist']
        current_user.wishlist = wishlist
        db.session.commit()
        flash('Wishlist updated successfully!', 'success')

    return render_template('dashboard.html', wishlist=current_user.wishlist)

# Admin dashboard
@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.email != ADMIN_EMAIL:
        flash("You are not authorized to access the admin panel.", "danger")
        return redirect(url_for('home'))

    participants = Participant.query.all()
    return render_template('admin_dashboard.html', participants=participants)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Create database tables before starting
    with app.app_context():
        db.create_all()
    app.run(debug=True)
