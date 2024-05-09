import streamlit as st
import pandas as pd
import random

# Global Variables
users = []  # List to store registered user names
race_results = []  # List to store results of each race

points_dict = {
    1: 15, 2: 12, 3: 10, 4: 8, 5: 7, 6: 6, 7: 5, 8: 4, 9: 3, 10: 2, 11: 1, 12: 0
}
def welcome_screen():
    st.title('Welcome to the Mario Kart Ranking App')
    if st.button('Register all Players'):
        st.session_state.current_screen = 'register'
        
def register_user(username):
    if username not in users:
        users.append(username)
        return True
    else:
        st.error(f"Error: A user with the username '{username}' already exists.")
        return False

def register_user_screen():
    st.title('Register a New User')
    new_username = st.text_input("Enter a new username to register:")
    register_button = st.button("Register")
    start_racing_button = st.button("Let's start racing")

    if register_button:
        if register_user(new_username):
            st.success("User registered successfully")

    # Display registered users table only once and always
    if st.session_state.users:
        st.write("Registered Users:")
        user_df = pd.DataFrame(st.session_state.users, columns=["Username"])
        st.table(user_df)

    # Allow moving to the next screen only if there are users registered
    if start_racing_button:
        if st.session_state.users:
            st.session_state.current_screen = 'add_results'
        else:
            st.error("Please register at least one user before starting the race.")

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
            # Corrected data collection to include race number in the result
            for user, placement in placements.items():
                race_results.append({
                    'race_number': race_number,
                    'username': user,
                    'position': placement,
                    'points': points_dict[placement]
                })
            st.success(f"Results for Race {race_number} submitted successfully.")
            if race_number < st.session_state.total_races:
                st.session_state.current_race += 1
            else:
                st.session_state.current_screen = 'view_leaderboard'

def calculate_total_points():
    df = pd.DataFrame(race_results)
    # Ensuring the DataFrame is properly aggregated
    leaderboard_df = df.groupby('username')['points'].sum().reset_index()
    leaderboard_df.sort_values(by='points', ascending=False, inplace=True)
    leaderboard_df['Rank'] = leaderboard_df['points'].rank(method='min', ascending=False)
    return leaderboard_df

def view_leaderboard_screen():
    st.title('View Leaderboard')
    leaderboard_df = calculate_total_points()
    st.table(leaderboard_df)
    if st.button('Reset Game'):
        st.session_state.pop('total_races', None)
        st.session_state.pop('current_race', None)
        st.session_state.pop('race_results', None)
        st.session_state.pop('game_master', None, None)
        users.clear()
        st.session_state.current_screen = 'welcome'
    if st.button('Quit Game'):
        st.session_state.current_screen = 'welcome'

# Initialize session state for users list if it's not already initialized
if 'users' not in st.session_state:
    st.session_state.users = []

# Initialize session state for navigation
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'welcome'

# Render the current screen based on the session state
if st.session_state.current_screen == 'welcome':
    welcome_screen()
elif st.session_state.current_screen == 'register':
    register_user_screen()
elif st.session_state.current_screen == 'add_results':
    add_race_result_screen()
elif st.session_state.current_screen == 'view_leaderboard':
    view_leaderboard_screen()
