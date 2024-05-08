import streamlit as st
import pandas as pd
import random

# Points dictionary remains unchanged
points_dict = {
    1: 15, 2: 12, 3: 10, 4: 8, 5: 7, 6: 6, 7: 5, 8: 4, 9: 3, 10: 2, 11: 1, 12: 0
}

# Use a list to store users and a list to store race results
users = []
race_results = []

def register_user(username):
    if username not in users:
        users.append(username)
        return True
    else:
        st.error(f"Error: A user with the username '{username}' already exists.")
        return False

def fetch_users():
    return users

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
    leaderboard_df = df.groupby('username', as_index=False)['points'].sum()
    leaderboard_df.sort_values(by='points', ascending=False, inplace=True)
    leaderboard_df['rank'] = leaderboard_df['points'].rank(method='min', ascending=False)
    return leaderboard_df

def view_leaderboard_screen():
    st.title('View Leaderboard')
    leaderboard_df = calculate_total_points()
    def color_top_three(val):
        color = 'yellow' if val == 1 else 'silver' if val == 2 else 'bronze' if val == 3 else ''
        return f'background-color: {color}'
    st.dataframe(leaderboard_df.style.applymap(color_top_three, subset=['rank']))
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Reset Game'):
            st.session_state.pop('total_races', None)
            st.session_state.pop('current_race', None)
            st.session_state.pop('race_results', None)
            st.session_state.current_screen = 'welcome'
    with col2:
        if st.button('Quit Game'):
            st.session_state.current_screen = 'welcome'
    if st.button('Back to Welcome'):
        st.session_state.current_screen = 'welcome'

# Navigation based on session state
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'welcome'
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
