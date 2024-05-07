import streamlit as st
import sqlite3
import pandas as pd
import random

# Database connection setup
def db_connection():
    conn = sqlite3.connect('mario_kart.db', check_same_thread=False)
    return conn

# Initialize the database with necessary tables
def init_db():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            position INTEGER NOT NULL,
            points INTEGER NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username)
        );
    """)
    conn.commit()
    conn.close()

# Register a new user in the database
def register_user(username):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error(f"Error: A user with the username '{username}' already exists.")
        return False
    finally:
        conn.close()

# Function definitions for each screen in the app
def welcome_screen():
    st.title('Welcome to the Mario Kart Ranking App')
    if st.button('Go to Registration'):
        st.session_state.current_screen = 'register'

def register_user_screen():
    st.title('Register a New User')
    with st.form("register_user"):
        new_username = st.text_input("Enter a new username to register:")
        submit_button = st.form_submit_button("Register")
        if submit_button:
            if register_user(new_username):
                st.success("User registered successfully")
    if st.button('Go to Choose Game Master'):
        st.session_state.current_screen = 'choose_master'


def fetch_users():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users

def choose_game_master_screen():
    st.title('Choose the Game Master')
    
    users = fetch_users()
    if not users:
        st.write('No registered users found. Please register some users first.')
        return

    if 'game_master' not in st.session_state or st.button('Choose a new Game Master'):
        st.session_state.game_master = random.choice(users)
        
    st.write(f"The chosen Game Master is: {st.session_state.game_master}")
    
    if st.button('Go to Add Race Results'):
        st.session_state.current_screen = 'add_results'

def add_race_result_screen():
    st.title('Add Race Results')
    st.write('Placeholder for adding race results.')
    if st.button('View Leaderboard'):
        st.session_state.current_screen = 'view_leaderboard'

def view_leaderboard_screen():
    st.title('View Leaderboard')
    st.write('Placeholder for leaderboard display.')
    if st.button('Back to Welcome'):
        st.session_state.current_screen = 'welcome'

# Initialize the app state if not already done
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'welcome'

# Render the current screen based on the state
if st.session_state.current_screen == 'welcome':
    welcome_screen()
elif st.session_state.current_screen == 'register':
    register_user_screen()
elif st.session_state.current_screen == 'choose_master':
    choose_game_master_screen()
elif st.session_state.current_screen == 'add_results':
    add_race_result_screen()
elif st.session_state.current_screen == 'view_leaderboard':
    view_leaderboard_screen()

# Ensure the database is initialized at least once
init_db()
