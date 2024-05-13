import streamlit as st
import sqlite3

conn = sqlite3.connect('userData.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (userID INTEGER, username TEXT, password TEXT, name TEXT)''')
conn.commit()

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



st.sidebar.title("Nav")
page = st.sidebar.radio("Click to go to...", ["Sign Up", "Login", "Image Edit Temp"])



if page == "Sign Up":
    st.title("Sign Up to continue")

    name = st.text_input("Enter your name: ")
    username = st.text_input("Create a username: ")
    password = st.text_input("Create a password: ", type="password")
    confirmPass = st.text_input("Confirm password: ", type="password")

    if st.button("Register"):
        if name and username and password == confirmPass:
            registerUser(username, password, name)
        else:
            st.text("Please enter all the fields")

elif page == "Login":

    st.title("Login Page")

    username = st.text_input("Enter Username: ")
    password = st.text_input("Enter Password: ", type="password")

    if st.button("Login"):
        if username and password:
            if loginUser(username, password):
                st.text("login successful")
            else:
                st.text("unsuccessful login")
        else:
            st.text("Please enter your username and password")

elif page == "Image Edit Temp":

    st.text("this will be where the editor goes")

conn.close()