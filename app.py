from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
import csv
from io import StringIO
from flask import make_response
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from io import BytesIO
from flask import send_file

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
login_manager.login_view = 'welcome'

# --- MODELS ---
class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    org_access_code = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), default="Supporting our local community.")

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False) 
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=True)
    organization = db.relationship('Organization', backref='members')

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), default="General 📦")
    quantity = db.Column(db.Integer, default=1)
    unit = db.Column(db.String(20), default="units")  # Add this!    
    # NEW: Custom Threshold
    low_threshold = db.Column(db.Integer, default=5) 
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(50))
    item_name = db.Column(db.String(100))
    action = db.Column(db.String(50)) 
    change = db.Column(db.String(20))
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
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
        reg_type = request.form.get('reg_type')

        if User.query.filter_by(username=username).first():
            flash('Username taken.')
            return redirect(url_for('register'))

        if reg_type == 'create':
            org_name = request.form.get('org_name')
            new_access_code = request.form.get('new_access_code')
            new_org = Organization(name=org_name, org_access_code=new_access_code)
            db.session.add(new_org)
            db.session.commit()
            target_org_id = new_org.id
            user_role = 'founder'
        else:
            access_code = request.form.get('access_code')
            org = Organization.query.filter_by(org_access_code=access_code).first()
            if not org:
                flash('Invalid Organization Access Code.')
                return redirect(url_for('register'))
            target_org_id = org.id
            user_role = role

        hashed_pw = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, password=hashed_pw, role=user_role, org_id=target_org_id)
        db.session.add(new_user)
        db.session.commit()

        flash(f'Success! Welcome to {Organization.query.get(target_org_id).name}')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('welcome'))

@app.route('/')
@login_required
def index():
    search_query = request.args.get('q', '')
    base_query = Item.query.filter_by(org_id=current_user.org_id)
    
    if search_query:
        items = base_query.filter((Item.name.contains(search_query)) | (Item.category.contains(search_query))).all()
    else:
        items = base_query.order_by(Item.date_added.desc()).all()
    
    # Secure logs by org_id
    logs = ActivityLog.query.filter_by(org_id=current_user.org_id).order_by(ActivityLog.timestamp.desc()).limit(10).all()
    return render_template('index.html', items=items, search_query=search_query, user=current_user, logs=logs)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html', user=current_user)

@app.route('/add', methods=['POST'])
@login_required
def add_item():
    name = request.form.get('name')
    category = request.form.get('category')
    unit = request.form.get('unit')
    threshold = request.form.get('threshold', 5)
    
    # Verify current_user.org_id exists to prevent IntegrityError
    if not current_user.org_id:
        flash("User is not associated with an organization.")
        return redirect(url_for('index'))

    new_item = Item(name=name, category=category, org_id=current_user.org_id, low_threshold=int(threshold))
    db.session.add(new_item)

    log = ActivityLog(
        username=current_user.username,
        item_name=name,
        action="Added Item",
        change="+1",
        org_id=current_user.org_id
    )
    db.session.add(log)
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

    change_text = "+1" if action == 'increase' else "-1"
    new_log = ActivityLog(
        username=current_user.username,
        item_name=item.name,
        action="Updated Qty",
        change=change_text,
        org_id=current_user.org_id
    )
    db.session.add(new_log)    
    db.session.commit()
    return jsonify({'new_qty': item.quantity})

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_item(id):
    if current_user.role not in ['volunteer', 'founder']:
        return jsonify({'error': 'Unauthorized'}), 403
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    log = ActivityLog(
        username=current_user.username,
        item_name=item.name,
        action="Deleted Item",
        change="-1",
        org_id=current_user.org_id
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit_item(id):
    item = Item.query.get_or_404(id)
    if current_user.role not in ['volunteer', 'founder']:
         return redirect(url_for('index'))
         
    item.name = request.form.get('name')
    item.category = request.form.get('category')
    # Update threshold
    item.low_threshold = int(request.form.get('threshold', 5))
    
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/export_audit_xlsx')
@login_required
def export_audit_xlsx():
    if current_user.role not in ['volunteer', 'founder']:
        return "Unauthorized", 403
    
    # FIX: Ensure we use 'ActivityLog' (matching the class name)
    logs = ActivityLog.query.filter_by(org_id=current_user.org_id).order_by(ActivityLog.timestamp.desc()).all()
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Audit Trail"
    
    headers = ['Timestamp', 'User', 'Action', 'Item Name', 'Change']
    ws.append(headers)
    
    header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    for log in logs:
        ws.append([
            log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            log.username,
            log.action.upper(),
            log.item_name,
            log.change
        ])

    # (Column width logic remains the same)
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except: pass
        ws.column_dimensions[column].width = max_length + 2

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    # Secure filename
    org_name = current_user.organization.name.replace(' ', '_') if current_user.organization else "Admin"
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f"Shelf_Audit_{org_name}.xlsx"
    )

@app.route('/team')
@login_required
def team_management():
    if current_user.role not in ['volunteer', 'founder']:
        flash("Access Denied.")
        return redirect(url_for('index'))

    all_members = User.query.filter_by(org_id=current_user.org_id).all()
    volunteers = [user for user in all_members if user.role in ['volunteer', 'founder']]
    donors = [user for user in all_members if user.role == 'donor']
    
    logs = ActivityLog.query.filter_by(org_id=current_user.org_id)\
                        .order_by(ActivityLog.timestamp.desc())\
                        .limit(10).all()

    return render_template('team.html', volunteers=volunteers, donors=donors, logs=logs)

@app.route('/remove_member/<int:user_id>', methods=['POST'])
@login_required
def remove_member(user_id):
    if current_user.role.lower() != 'founder':
        return jsonify({'error': 'Only the Founder can remove members'}), 403
    
    user_to_remove = User.query.get_or_404(user_id)
    if user_to_remove.org_id == current_user.org_id and user_to_remove.id != current_user.id:
        db.session.delete(user_to_remove)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Invalid request'}), 400

@app.route('/update_mission', methods=['POST'])
@login_required
def update_mission():
    if current_user.role.lower() != 'founder':
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    current_user.organization.description = data.get('description')
    db.session.commit()
    return jsonify({'success': True})

if __name__ == "__main__":
    app.run(debug=True)
