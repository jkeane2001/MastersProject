import sqlite3
import streamlit as st

conn = sqlite3.connect('userData.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (userID INTEGER, username TEXT, password TEXT, name TEXT)''')
conn.commit()


landingPage = st.container()
mainSection = st.container()
loginSection = st.container()
logoutSection = st.container()


def showMainPage():
    with mainSection:
        st.text("This will be the image editor")
        beginEditing = st.button("Start Editing")
        if beginEditing:
            st.balloons()

def loggedOutClicked():
    st.session_state['loggedIn'] = False

def showLogoutPage():
    logoutSection.empty()
    with logoutSection:
        st.button("Log Out", on_click=loggedOutClicked)


def loggedInClicked(username, password):
    if loginUser(username, password):
        st.session_state['loggedIn'] = True
    else:
        st.session_state['loggedIn'] = False
        st.text("Invalid username or password")

def showLoginPage():
    with loginSection:
        if st.session_state['loggedIn'] == False:
            username = st.text_input("Enter Username: ")
            password = st.text_input("Enter Password: ", type="password")
            st.button("Login", on_click=loggedInClicked, args=(username, password))

def registerUser(username, password, name):

    c.execute("INSERT INTO users (username, password, name) VALUES (?,?,?)", (username, password, name))
    conn.commit()
    st.text("User Registered")

def loginUser(username, password):

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    if user:
        return True
    else:
        return False

with landingPage:
    st.title("Image Editor")

    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        showLogoutPage()
        showMainPage()
    else:
        showLoginPage()

conn.close()