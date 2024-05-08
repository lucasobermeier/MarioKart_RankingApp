import streamlit as st
import pandas as pd
import random

# Global Variables
users = []  # List to store registered user names
race_results = []  # List to store results of each race

points_dict = {
    1: 15, 2: 12, 3: 10, 4: 8, 5: 7, 6: 6, 7: 5, 8: 4, 9: 3, 10: 2, 11: 1, 12: 0
}

def register_user(username):
    if username not in users:
        users.append(username)
        return True
    else:
        st.error(f"Error: A user with the username '{username}' already exists.")
        return False

def welcome_screen():
    st.title('Welcome to the Mario Kart Ranking App')
    if st.button('Go to Registration'):
        st.session_state.current_screen = 'register'

def register_user_screen():
    st.title('Register a New User')
    new_username = st.text_input("Enter a new username to register:")
    if st.button("Register"):
        if register_user(new_username):
            st.success("User registered successfully")
            st.session_state.current_screen = 'choose_master'

def choose_game_master_screen():
    st.title('Choose the Game Master')
    if users:
        if 'game_master' not in st.session_state or st.button('Choose a new Game Master'):
            st.session_state.game_master = random.choice(users)
        st.write(f"The chosen Game Master is: {st.session_state.game_master}")
        if st.button('Go to Add Race Results'):
            st.session_state.current_screen = 'add_results'
    else:
        st.error("No users registered. Please register some users first.")

def add_race_result_screen():
    st.title('Add Race Results')
    if 'total_races' not in st.session_state:
        st.session_state.total_races = st.number_input("Enter number of races", min_value=1, max_value=10, value=3, step=1)
        st.session_state.current_race = 1

    if 'total_races' in st.session_state and st.session_state.current_race <= st.session_state.total_races:
        race_number = st.session_state.current_race
        st.header(f'Race {race_number}: Results')
        placements = {user: st.selectbox(f"Select place for {user}:", range(1, 13), key=f"{user}{race_number}") for user in users}
        if st.button(f'Submit Results for Race {race_number}'):
            race_results.append({user: points_dict[placement] for user, placement in placements.items()})
            st.success(f"Results for Race {race_number} submitted successfully.")
            if race_number < st.session_state.total_races:
                st.session_state.current_race += 1
            else:
                st.session_state.current_screen = 'view_leaderboard'

def calculate_total_points():
    df = pd.DataFrame(race_results)
    leaderboard_df = df.sum().sort_values(by='points', ascending=False).reset_index()
    leaderboard_df.columns = ['Username', 'Total Points']
    leaderboard_df['Rank'] = leaderboard_df['Total Points'].rank(method='min', ascending=False)
    return leaderboard_df

def view_leaderboard_screen():
    st.title('View Leaderboard')
    leaderboard_df = calculate_total_points()
    st.table(leaderboard_df)
    if st.button('Reset Game'):
        st.session_state.pop('total_races', None)
        st.session_state.pop('current_race', None)
        st.session_state.pop('race_results', None)
        st.session_state.pop('game_master', None)
        users.clear()
        st.session_state.current_screen = 'welcome'
    if st.button('Quit Game'):
        st.session_state.current_screen = 'welcome'

# Initialize session state for navigation
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'welcome'

# Render the current screen based on the session state
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
