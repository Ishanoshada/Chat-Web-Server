# This Flask app is coded by Ishan Oshada (@ishanoshada)
# It provides a real-time chat web application using Flask, JSON file, and MongoDB for data storage.
# Users can sign up, log in, send messages, and delete their own messages.
# The code demonstrates how to build a simple chat app with basic authentication and data storage.
# Feel free to read and explore the code to learn more about Flask web development.


from flask import * #Flask, render_template, request, jsonify, session, redirect ...
from datetime import datetime
from markupsafe import escape
import json
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

#### Choose the Data Storage Method (JSON File or MongoDB)
USE_JSON_STORAGE = True

#### User Data File (JSON)
USER_DATA_FILE = 'data/users_data.json'
CHAT_FILE = "data/chats.json"

#### MongoDB Configuration
if not USE_JSON_STORAGE:
 MONGO_URI = 'mongodb://localhost:27017/'
 MONGO_DB_NAME = 'chat_app_db'
 MONGO_COLLECTION_NAME = 'messages'
 MONGO_USER_COLLECTION_NAME = 'users'

# Rest of the load_messages function...
def load_messages():
    if USE_JSON_STORAGE:
        try:
            with open(CHAT_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    else:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_COLLECTION_NAME]
        return list(collection.find())

# Rest of the save_messages function...
def save_messages(messages):
    if USE_JSON_STORAGE:
        with open(CHAT_FILE, 'w') as f:
            json.dump(messages, f)
    else:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_COLLECTION_NAME]
        collection.delete_many({})  #### Clear the existing messages
        collection.insert_many(messages)

# Rest of the load_user_data function...
def load_user_data():
    if USE_JSON_STORAGE:
        try:
            with open(USER_DATA_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    else:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_USER_COLLECTION_NAME]
        return list(collection.find())

# Rest of the save_user_data function...
def save_user_data(users):
    if USE_JSON_STORAGE:
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(users, f)
    else:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_USER_COLLECTION_NAME]
        collection.delete_many({})  #### Clear the existing user data
        collection.insert_many(users)

messages = load_messages()
users = load_user_data()

# Rest of the custom function for XSS protection...
def safe_content(content):
    return escape(content)

# Rest of the index route...
@app.route('/',methods=['POST',"GET"])
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', messages=messages, template_folder="templates")

# Rest of the send_message route...
@app.route('/send', methods=['POST'])
def send_message():
    if 'user' not in session:
        return jsonify({'error': 'You must be logged in to send messages.'}), 401

    message = safe_content(request.form.get('message'))
    if not message:
        return jsonify({'error': 'Message content cannot be empty.'}), 400

    messages = load_messages()
    new_message = {
        'id': len(messages) + 1,
        'sender': session['user'],
        'message': message,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'deleted': False
    }
    messages.append(new_message)
    save_messages(messages)

    return jsonify({'messages': messages})

# Rest of the signup route...
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        if not email or not username or not password:
            return jsonify({'error': 'All fields are required.'}), 400

        hashed_password = generate_password_hash(password)
        new_user = {'email': email, 'username': username, 'password': hashed_password}
        users.append(new_user)
        save_user_data(users)
        redirect(url_for('login'))
       # return jsonify({'message': 'Signup successful!'}), 201

    return render_template('signup.html', template_folder="templates")

# Rest of the login route...
@app.route('/login', methods=['GET', 'POST'])
def login():
    if not 'user' in session:
        return redirect(url_for('login'))
    else:
         return redirect(url_for('index'))
   
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        if not username_or_email or not password:
            return jsonify({'error': 'All fields are required.'}), 400

        user = next((u for u in users if u['email'] == username_or_email or u['username'] == username_or_email), None)
        if not user or not check_password_hash(user['password'], password):
            return jsonify({'error': 'Invalid username/email or password.'}), 401

        session['user'] = user['username']
        return redirect(url_for('index'))

    return render_template('login.html', template_folder="templates")

# Rest of the get_messages route..
@app.route('/get_messages')
def get_messages():
    messages = load_messages()
    return jsonify({'messages': messages})

# Rest of the delete_message route...
@app.route('/delete/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    if 'user' not in session:
        return jsonify({'error': 'You must be logged in to delete messages.'}), 401

    messages = load_messages()
    for message in messages:
        if message['id'] == message_id and message['sender'] == session['user']:
            message['deleted'] = True
            save_messages(messages)
            session.setdefault('deleted_messages', []).append(message_id)
            return jsonify({'messages': messages})

    return jsonify({'error': 'Message not found or you are not allowed to delete it.'}), 404

# Rest of the logout route...
@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
    return redirect(url_for('index'))

# Error handling for 404 - Page Not Found...
# Rest of the errorhandler for 404...
@app.errorhandler(404)
def page_not_found(error):
    if 'user' in session:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('signup'))


# Running the app 
if __name__ == '__main__':
    app.run(debug=True)

