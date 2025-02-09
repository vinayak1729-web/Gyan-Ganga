from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
from datetime import datetime
import secrets

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
@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    if 'username' not in session:
        return redirect(url_for('signup'))
        
    if request.method == 'POST':
        data = request.get_json()
        username = session['username']
        
        questionnaire_data = {
            "username": username,
            "submission_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "questions": [
                {"id": "education_level", "answer": data.get('education_level')},
                {"id": "interests", "answer": data.get('interests')},
                {"id": "programming_level", "answer": data.get('programming_level')},
                {"id": "learning_goals", "answer": data.get('learning_goals')},
                {"id": "time_commitment", "answer": data.get('time_commitment')},
                {"id": "learning_environment", "answer": data.get('learning_environment')},
                {"id": "problem_solving_approach", "answer": data.get('problem_solving_approach')},
                {"id": "learning_motivation", "answer": data.get('learning_motivation')}
            ]
        }
        
        with open(f'database/details/{username}.json', 'w') as f:
            json.dump(questionnaire_data, f, indent=4)
            
        session.clear()
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
            return redirect(url_for('home'))
            
        return "Invalid credentials"
        
    return render_template('login.html')

@app.route('/')
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Create mock data for the dashboard
    user_data = {
        'name': session['username'],
        'streak': 5,  # Example streak
        'badges': 3   # Example badges
    }
    
    # Example course data
    courses = [
        {
            'title': 'Python Programming',
            'description': 'Learn Python from scratch',
            'modules': 12,
            'duration': 24
        },
        # Add more courses as needed
    ]
    
    # Example learning tools
    learning_tools = [
        {
            'icon': 'book',
            'title': 'Study Materials',
            'description': 'Access comprehensive study materials'
        },
        # Add more tools as needed
    ]
    
    return render_template('home.html', 
                         user=user_data, 
                         courses=courses, 
                         learning_tools=learning_tools)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

from flask import Flask, render_template,request,jsonify,json
from datetime import datetime

# Demo courses data
courses = [
    {
        "title": "Bhagavad Gita",
        "description": "Learn the divine knowledge of Krishna and Arjuna's dialogue",
        "duration": "12 weeks",
        "level": "Intermediate"
    },
    {
        "title": "Vedic Mathematics",
        "description": "Master the ancient Indian system of mathematics",
        "duration": "8 weeks",
        "level": "Beginner"
    },
    {
        "title": "Ayurveda Basics",
        "description": "Understand the fundamental principles of Ayurvedic science",
        "duration": "10 weeks",
        "level": "Beginner"
    }
]

@app.route('/Gurukul')
def dashboard():
    current_hour = datetime.now().hour
    
    # Determine time period
    if 4 <= current_hour < 8:
        period = "morning"
    elif 8 <= current_hour < 16:
        period = "midday"
    elif 16 <= current_hour < 20:
        period = "evening"
    else:
        period = "night"
    
    return render_template('Gurukuldashboard.html', period=period, courses=courses)

def get_scene_for_hour(hour):
    scenes = {
        'brahma-muhurta': {
            'background': 'linear-gradient(to bottom, #1a1a2e, #4a3b52)',
            'ambient_sound': 'early_morning_birds.mp3',
            'description': 'The sacred pre-dawn hours'
        },
        'sunrise': {
            'background': 'linear-gradient(to bottom, #FF7F50, #FFD700)',
            'ambient_sound': 'morning_birds.mp3',
            'description': 'The rising sun brings new energy'
        },
        'morning': {
            'background': 'linear-gradient(to bottom, #87CEEB, #E0FFFF)',
            'ambient_sound': 'morning_nature.mp3',
            'description': 'A bright, energetic morning'
        },
        'afternoon': {
            'background': 'linear-gradient(to bottom, #00BFFF, #87CEEB)',
            'ambient_sound': 'afternoon_breeze.mp3',
            'description': 'The sun at its peak'
        },
        'evening': {
            'background': 'linear-gradient(to bottom, #FF4500, #FFD700)',
            'ambient_sound': 'evening_crickets.mp3',
            'description': 'The calming sunset hours'
        },
        'night': {
            'background': 'linear-gradient(to bottom, #000033, #191970)',
            'ambient_sound': 'night_sounds.mp3',
            'description': 'The peaceful night time'
        }
    }

    if 4 <= hour < 6:
        return scenes['brahma-muhurta']
    elif 6 <= hour < 8:
        return scenes['sunrise']
    elif 8 <= hour < 12:
        return scenes['morning']
    elif 12 <= hour < 16:
        return scenes['afternoon']
    elif 16 <= hour < 19:
        return scenes['evening']
    else:
        return scenes['night']

@app.route('/my-gurukul')
def my_gurukul():
    routines = [
        {
            "section": "morning",
            "title": "🌅 Brahma Muhurta",
            "time": "4:00 AM - 5:00 AM",
            "activities": [
                {"time": "4:00 AM", "title": "Divine Awakening", "description": "Wake up (Brahma Muhurta, best time for knowledge & meditation)"},
                {"time": "4:05 AM", "title": "Morning Hygiene", "description": "Wash face, brush teeth, and drink warm water"},
                {"time": "4:15 AM", "title": "Short Prayer and Gratitude", "description": "Express thanks to nature and ancestors"},
                {"time": "4:30 AM", "title": "Meditation (Dhyana) & Breathing", "description": "Practice deep breathing (Pranayama) for mental clarity"}
            ]
        },
        {
            "section": "vedic",
            "title": "🕉️ Vedic Study & Spiritual Practices",
            "time": "5:00 AM - 6:00 AM",
            "activities": [
                {"time": "5:00 AM", "title": "Vedic Chanting", "description": "Chanting of Vedic mantras or Bhagavad Gita slokas"},
                {"time": "5:30 AM", "title": "Scripture Study", "description": "Study of Upanishads, Vedas, or philosophical texts"},
                {"time": "5:50 AM", "title": "Introspection", "description": "Self-reflection and introspection"}
            ]
        },
        {
            "section": "physical",
            "title": "🏋️‍♂️ Physical Training & Hygiene",
            "time": "6:00 AM - 7:30 AM",
            "activities": [
                {"time": "6:00 AM", "title": "Yoga", "description": "Surya Namaskar, flexibility, strength training"},
                {"time": "6:30 AM", "title": "Martial Arts", "description": "Outdoor exercises or martial arts (Kalaripayattu or wrestling)"},
                {"time": "7:00 AM", "title": "Bathing", "description": "Cold water bath preferred for vitality"},
                {"time": "7:15 AM", "title": "Dressing", "description": "Wearing clean, simple clothes (Dhoti/Kurta)"}
            ]
        },
        {
            "section": "breakfast",
            "title": "🍛 Sattvic Breakfast",
            "time": "7:30 AM - 8:00 AM",
            "activities": [
                {"time": "7:30 AM", "title": "Healthy Meal", "description": "Simple, nutritious meal (fruits, nuts, milk, and light grains)"},
                {"time": "7:45 AM", "title": "Mindful Eating", "description": "Eating mindfully in silence, respecting the food"}
            ]
        },
        {
            "section": "education",
            "title": "📚 Core Education & Knowledge",
            "time": "8:00 AM - 12:00 PM",
            "activities": [
                {"time": "8:00 AM - 10:00 AM", "title": "Learning", "description": "Mathematics, Sanskrit, Astronomy, Ayurveda, Philosophy, etc."},
                {"time": "10:00 AM - 10:15 AM", "title": "Meditation Break", "description": "Short meditation or mindfulness break"},
                {"time": "10:15 AM - 12:00 PM", "title": "Practical Learning", "description": "Debates, science, craftsmanship, Vedic rituals"}
            ]
        },
        {
            "section": "lunch",
            "title": "🍽️ Midday Meal & Rest",
            "time": "12:00 PM - 2:00 PM",
            "activities": [
                {"time": "12:00 PM - 12:30 PM", "title": "Lunch", "description": "Wholesome sattvic food: rice, dal, vegetables, ghee, buttermilk"},
                {"time": "12:30 PM - 1:30 PM", "title": "Rest", "description": "Short nap or relaxation"},
                {"time": "1:30 PM - 2:00 PM", "title": "Creative Arts", "description": "Self-study or creative arts (painting, music, poetry, or storytelling)"}
            ]
        },
        {
            "section": "skill",
            "title": "📝 Skill Development & Practical Training",
            "time": "2:00 PM - 5:00 PM",
            "activities": [
                {"time": "2:00 PM - 3:30 PM", "title": "Hands-on Learning", "description": "Crafting, farming, vedic mathematics, archery, or weapon training"},
                {"time": "3:30 PM - 4:00 PM", "title": "Tea Break", "description": "Tea with fruits or light snacks"},
                {"time": "4:00 PM - 5:00 PM", "title": "Discussions", "description": "Moral stories, discussions, or spiritual discourses"}
            ]
        },
        {
            "section": "evening",
            "title": "🌇 Evening Rituals & Discipline",
            "time": "5:00 PM - 7:00 PM",
            "activities": [
                {"time": "5:00 PM - 6:00 PM", "title": "Physical Exercise", "description": "Running, games, self-defense, horse riding"},
                {"time": "6:00 PM - 6:30 PM", "title": "Evening Prayers", "description": "Sandhya Vandana (Evening prayers & mantra chanting)"},
                {"time": "6:30 PM - 7:00 PM", "title": "Devotional Music", "description": "Music or bhajans (devotional singing, instrumental practice)"}
            ]
        },
        {
            "section": "dinner",
            "title": "🍲 Light Dinner & Reflection",
            "time": "7:00 PM - 9:00 PM",
            "activities": [
                {"time": "7:00 PM - 7:30 PM", "title": "Dinner", "description": "Light and sattvic food (khichdi, roti, vegetables, warm milk)"},
                {"time": "7:30 PM - 8:30 PM", "title": "Revision", "description": "Revision of the day's lessons, discussions, or writing journal"},
                {"time": "8:30 PM - 9:00 PM", "title": "Contemplation", "description": "Silent contemplation or gratitude prayers"}
            ]
        },
        {
            "section": "night",
            "title": "🌙 Night Routine & Sleep",
            "time": "9:00 PM - 10:00 PM",
            "activities": [
                {"time": "9:00 PM - 9:30 PM", "title": "Evening Meditation", "description": "Short meditation or slow chanting (Om mantra)"},
                {"time": "9:30 PM - 10:00 PM", "title": "Sleep Preparation", "description": "Prepare for sleep, lying on the right side for good digestion"},
                {"time": "10:00 PM", "title": "Sleep", "description": "Sleep early to wake up energized at 4 AM"}
            ]
        }
    ]
    
    current_hour = datetime.now().hour
    scene = get_scene_for_hour(current_hour)
    
    return render_template('my_gurukul.html', routines=routines, scene=scene)


@app.route('/api/routines', methods=['POST'])
def save_routines():
    routines = request.json
    # Save to your database
    with open('routines.json', 'w') as f:
        json.dump(routines, f)
    return jsonify({'status': 'success'})



if __name__ == '__main__':
    app.run(debug=True)