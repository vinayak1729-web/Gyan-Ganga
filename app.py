from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
from datetime import datetime
import secrets
from pathlib import Path

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Create necessary directories
os.makedirs('database', exist_ok=True)
os.makedirs('database/details', exist_ok=True)

def load_users():
    try:
        with open('database/users.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users):
    with open('database/users.json', 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        users = load_users()
        
        # Check if username exists
        if any(user['username'] == username for user in users):
            return jsonify({'success': False, 'error': 'Username already exists'})

        new_user = {
            'username': username,
            'email': email,
            'password': password,
            'signup_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        users.append(new_user)
        save_users(users)
        
        session['username'] = username
        session['email'] = email
        
        return jsonify({'success': True, 'redirect': '/questionnaire'})
        
    return render_template('signup.html')

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    if 'username' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        data = request.get_json()
        username = session['username']
        
        questionnaire_data = {
            "username": username,
            "submission_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "questions": [
                {"id": "fan_duration", "answer": data.get('fan_duration')},
                {"id": "favorite_teams", "answer": data.get('favorite_teams')},
                {"id": "favorite_players", "answer": data.get('favorite_players')},
                {"id": "selected_team", "answer": data.get('selected_team')},
                {"id": "favorite_match", "answer": data.get('favorite_match')},
                {"id": "notifications", "answer": data.get('notification_frequency')}
            ]
        }
        
        with open(f'database/details/{username}.json', 'w') as f:
            json.dump(questionnaire_data, f, indent=4)
            
        return jsonify({'success': True, 'redirect': '/login'})
        
    return render_template('questionnaire.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = load_users()
        user = next((user for user in users if user['username'] == username and user['password'] == password), None)
        
        if user:
            session['username'] = username
            return redirect(url_for('index'))
            
        return "Invalid credentials"
        
    return render_template('login.html')

@app.route('/')
def index():
    username = session.get('username', 'Guest')
    return render_template('hometest.html', username=username)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
