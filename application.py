from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["new"]
auth_users = db["users"]
accounts = db["accounts"]
groups = db["groups"]

@app.route('/')
def index():
    return render_template('index.html')

# API for login
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = auth_users.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        session['user'] = user['username']
        return jsonify({"success": True, "message": "Login successful"}), 200
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

# API for registration
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    hashed_pw = generate_password_hash(password)

    if auth_users.find_one({'email': email}):
        return jsonify({"success": False, "message": "Email already registered."}), 400

    auth_users.insert_one({'username': username, 'email': email, 'password': hashed_pw})
    return jsonify({"success": True, "message": "Registration successful! Please log in."}), 201

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', accounts=accounts.find(), groups=groups.find())

@app.route('/add_account', methods=['GET', 'POST'])
def add_account():
    if request.method == 'POST':
        account_name = request.form['account_name']
        accounts.insert_one({'name': account_name})
        flash('Account added successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_account.html')

@app.route('/add_user_to_account', methods=['GET', 'POST'])
def add_user_to_account():
    if request.method == 'POST':
        user_name = request.form['user_name']
        account_name = request.form['account_name']
        flash('User added to account successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_user_to_account.html')

@app.route('/add_user_with_new_account', methods=['GET', 'POST'])
def add_user_with_new_account():
    if request.method == 'POST':
        user_name = request.form['user_name']
        account_name = request.form['account_name']
        flash('User added with new account successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_user_with_new_account.html')

@app.route('/add_group', methods=['GET', 'POST'])
def add_group():
    if request.method == 'POST':
        group_name = request.form['group_name']
        groups.insert_one({'name': group_name})
        flash('Group added successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_group.html')

@app.route('/add_user_to_group', methods=['GET', 'POST'])
def add_user_to_group():
    if request.method == 'POST':
        user_name = request.form['user_name']
        group_name = request.form['group_name']
        flash('User added to group successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_user_to_group.html')

if __name__ == '__main__':
    app.run(debug=True)
