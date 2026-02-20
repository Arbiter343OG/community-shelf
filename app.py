from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

app = Flask(__name__)

# 2. Configure App from .env
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-123')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///shelf.db')
app.config['VOLUNTEER_ACCESS_CODE'] = os.getenv('VOLUNTEER_ACCESS_CODE', 'JOIN-SHELF-2026')

db = SQLAlchemy(app)

# --- LOGIN SETUP ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- MODELS ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'volunteer' or 'donor'

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), default="General 📦")
    quantity = db.Column(db.Integer, default=1)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize DB and Test Users
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        # High-performer note: use scrypt for consistency across the whole app
        db.session.add(User(username='admin', password=generate_password_hash('123', method='scrypt'), role='volunteer'))
        db.session.add(User(username='guest', password=generate_password_hash('123', method='scrypt'), role='donor'))
        db.session.commit()

# --- ROUTES ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('index'))
        flash('Login Failed. Check your credentials.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        access_code = request.form.get('access_code')

        if User.query.filter_by(username=username).first():
            flash('Username already taken. Try another!')
            return redirect(url_for('register'))

        if role == 'volunteer':
            if access_code != app.config['VOLUNTEER_ACCESS_CODE']:
                flash('Incorrect Volunteer Access Code.')
                return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, password=hashed_pw, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created! You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    search_query = request.args.get('q', '')
    if search_query:
        items = Item.query.filter((Item.name.contains(search_query)) | (Item.category.contains(search_query))).all()
    else:
        items = Item.query.order_by(Item.date_added.desc()).all()
    return render_template('index.html', items=items, search_query=search_query, user=current_user)

@app.route('/add', methods=['POST'])
@login_required
def add_item():
    name = request.form.get('name')
    category = request.form.get('category')
    db.session.add(Item(name=name, category=category))
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>/<string:action>', methods=['POST'])
@login_required
def update(id, action):
    item = Item.query.get_or_404(id)
    if current_user.role == 'donor' and action == 'decrease':
        return jsonify({'error': 'Donors cannot remove stock'}), 403
    
    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease' and item.quantity > 0:
        item.quantity -= 1
        
    db.session.commit()
    return jsonify({'new_qty': item.quantity})

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_item(id):
    if current_user.role != 'volunteer':
        return jsonify({'error': 'Unauthorized'}), 403
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit_item(id):
    item = Item.query.get_or_404(id)
    # Security: Ensure only volunteers or the "owner" (if you add that later) can edit
    if current_user.role != 'volunteer':
         return redirect(url_for('index'))
         
    item.name = request.form.get('name')
    item.category = request.form.get('category')
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
