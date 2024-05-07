import streamlit as st
import sqlite3
import pandas as pd

# Database Connection
def db_connection():
    conn = sqlite3.connect('mario_kart.db', check_same_thread=False)
    return conn

# Initialize Database
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

# Define functions for each screen
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
            register_user(new_username)
            st.success("User registered successfully")
    if st.button('Go to Choose Game Master'):
        st.session_state.current_screen = 'choose_master'

def choose_game_master_screen():
    st.title('Choose the Game Master')
    st.write('Placeholder for choosing the game master.')
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

# Set default screen if not set
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'welcome'

# Display the current screen
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

# Initialize the database
init_db()
