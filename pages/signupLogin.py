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

conn.close()