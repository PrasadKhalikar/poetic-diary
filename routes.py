from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db, Poem
from forms import RegistrationForm, LoginForm,PoemForm

# Create a blueprint
routes = Blueprint('routes', __name__)

# Route for user registration
@routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username = form.username.data, email = form.email.data, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('routes.login'))
        except:
            db.session.rollback()
            flash('An error occurred while creating the account. Try again.', 'danger')
    return render_template('register.html', form=form)

# Route for user login
@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('routes.dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

# Route for user logout
@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('routes.login'))

# Route for user dashboard
@routes.route('/dashboard')
@login_required
def dashboard():
    poems = Poem.query.filter_by(user_id=current_user.id).all()  # Get the user's own poems that are not public
    return render_template('dashboard.html', poems=poems)

# Placeholder for Poetic Diary writing functionality
@routes.route('/write_poem', methods=['GET','POST'])
@login_required
def write_poem():
    form = PoemForm()
    if form.validate_on_submit():
        new_poem = Poem(title=form.title.data, content=form.content.data, is_public=form.public.data, user_id=current_user.id)
        db.session.add(new_poem)
        db.session.commit()
        flash('Poem added successfully!', 'success')
        return redirect(url_for('routes.dashboard'))
    return render_template('write_poem.html', form=form)

@routes.route('/public_poems')
def public_poems():
    poems = Poem.query.filter_by(is_public=True).all()  # Get all public poems
    return render_template('public_poems.html', poems=poems)


