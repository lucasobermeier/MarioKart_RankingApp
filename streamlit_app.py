import streamlit as st
import pandas as pd
import random

#Global Variables for Data Storage
users = []
race_results = []
points_dict = {1: 15, 2: 12, 3: 10, 4: 8, 5: 7, 6: 6, 7: 5, 8: 4, 9: 3, 10: 2, 11: 1, 12: 0} #Points according to the official MarioKart Game

def setup_app():
    # Initialize session state for users list
    if 'users' not in st.session_state: 
        st.session_state.users = []
        
    #Initialize session state for race results
    if 'race_results' not in st.session_state:
        st.session_state.race_results = []
    
    # Initialize session state for navigation
    if 'current_screen' not in st.session_state:
        st.session_state.current_screen = 'welcome'

#Initial setup for the session state of the app
setup_app()

#Only for UI Design reasons
def welcome_bg_and_custom_css():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://pliki.ppe.pl/storage/39653022149bea4f5935/39653022149bea4f5935-1200w.jpg");
            background-size: cover;
            background-position: center;
        }
        .text-container {
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            position: relative;  /* Makes sure the container is properly positioned */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
#Adding a backround image troughout the app
def add_bg(): 
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://img.freepik.com/free-photo/2d-graphic-wallpaper-with-colorful-grainy-gradients_23-2151001521.jpg");
            background-size: cover;
            background-position: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
#Outsourced function for user registration and point calculation for more clarity
def register_user(username):
    # Check if the username is not already in the session state users list
    if username not in st.session_state.users:
        # Add the new username to the session state users lis
        st.session_state.users.append(username)
        return True
    else:
        #Display an error message if the username already exists
        st.error(f"Error: A user with the username '{username}' already exists.")  
        return False

def calculate_total_points():
    if st.session_state.race_results:  # Ensure there is data to process
        df = pd.DataFrame(st.session_state.race_results) # Convert race results from session state into a DataFrame
        if 'username' in df.columns and 'points' in df.columns:  # Check if the expected columns 'username' and 'points' are in the DataFrame
            leaderboard_df = df.groupby('username')['points'].sum().reset_index() # Group by username and sum the points for each user
            leaderboard_df.sort_values(by='points', ascending=False, inplace=True) # Sort the DataFrame by points in descending order
            leaderboard_df['rank'] = leaderboard_df['points'].rank(method='min', ascending=False).astype(int) # Assign ranks based on the total points, with the highest points getting rank 1
            return leaderboard_df
        else:
            st.error("Expected data columns missing in the race results.") # Display an error if the expected columns are missing
            return pd.DataFrame(columns=['Username', 'Total Points', 'Rank'])
    else:
        st.warning("No race results available yet.") # Display a warning if there are no race results available
        return pd.DataFrame(columns=['Username', 'Total Points', 'Rank'])


# Screen functions: Responsible for displaying different user interfaces of the app. 
# Each function represents an independent screen and controls the specific interactions (and the program logic behind) and layout.
def welcome_screen():
    welcome_bg_and_custom_css()
    st.title('Mario Kart: The Ranking App')

    st.markdown("""
        <div class="text-container">
            <p>Welcome to the <strong>Mario Kart: The Ranking App</strong>! This interactive application allows you to set up races, register players, and track race results in real-time. Here’s what you can do:</p>
            <ul>
                <li><strong>Register Players:</strong> Add participants to the race and manage your player list.</li>
                <li><strong>Record Race Results:</strong> After each race, input the results to see who's leading.</li>
                <li><strong>View Leaderboard:</strong> Check out the leaderboard to see rankings and find out who's on top in the Mario Kart championship.</li>
            </ul>
            <p>Whether you're hosting a Mario Kart tournament or just having fun with friends, this app will make managing and displaying results easy and fun. Get started by registering players and let the races begin!</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.button('Go to Registration')
    st.session_state.current_screen = 'register'

def register_user_screen():
    add_bg()
    
    st.title('Register a New User')
    st.header('Enter a new username to register:')
    new_username = st.text_input("")
    register_button = st.button("Register")
    start_racing_button = st.button("Let's start racing")

    if register_button:
        if register_user(new_username): # register_user() returns true if user is sucessfully registered
            st.success("User registered successfully")
    
    #Display registered users table
    if st.session_state.users:
        st.header("Registered Users:")
        user_df = pd.DataFrame(st.session_state.users, columns=["Username"])
        st.table(user_df)

    #Allow moving to the next screen only if there are users registered
    if start_racing_button:
        if st.session_state.users:
            st.session_state.current_screen = 'add_results'
        else:
            st.error("Please register at least one user before starting the race.")

def add_race_result_screen():
    add_bg()
    st.title('Race Results:')

    #Setting up the number of races with a confirmation button
    if 'total_races' not in st.session_state:
        # This initial setup will only ask for the number of races if not yet defined
        races_input = st.number_input("Enter number of races", min_value=1, max_value=10, value=3, step=1)
        if st.button('Start Racing'):
            st.session_state.total_races = races_input
            st.session_state.current_race = 1  #Initializing the current race here after confirmation
        return  #Return early to avoid executing further logic until 'Start Racing' is clicked

    #Ensuring current_race is defined before trying to access it
    if 'current_race' in st.session_state and st.session_state.current_race <= st.session_state.total_races:
        race_number = st.session_state.current_race
        st.header(f'Race {race_number}: Results')

        #User rank inputs
        placements = {user: st.selectbox(f"Select place for {user}:", range(1, 13), key=f"{user}_{race_number}") for user in st.session_state.users}
        
        if st.button(f'Submit Results for Race {race_number}'):
            #Store results for each user
            for user, placement in placements.items():
                st.session_state.race_results.append({
                    'race_number': race_number,
                    'username': user,
                    'position': placement,
                    'points': points_dict[placement]
                })
            st.success(f"Results for Race {race_number} submitted successfully.")
            
            #Move to the next race or finish/final results
            if race_number < st.session_state.total_races:
                st.session_state.current_race += 1
            else:
                st.button ('View Final Result')
                st.session_state.current_screen = 'view_leaderboard'
    else:
        st.error("Please set the total number of races first.")
    
def view_leaderboard_screen():
    add_bg()
    st.title('Final Leaderboard')
    leaderboard_df = calculate_total_points()  # Calculate and get the leaderboard
    st.table(leaderboard_df) # Display leaderboard as a table
    if st.button('Reset Races'):
        # Reset session state variables and clear users
        st.session_state.pop('total_races', None)
        st.session_state.pop('current_race', None)
        st.session_state.pop('race_results', None)
        users.clear()
        st.session_state.current_screen = 'register'
    if st.button('Quit Game'):
        st.session_state.current_screen = 'welcome' # Change screen to welcome

#Render the current screen based on the session state
if st.session_state.current_screen == 'welcome':
    welcome_screen()
elif st.session_state.current_screen == 'register':
    register_user_screen()
elif st.session_state.current_screen == 'add_results':
    add_race_result_screen()
elif st.session_state.current_screen == 'view_leaderboard':
    view_leaderboard_screen()
