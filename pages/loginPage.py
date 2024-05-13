import streamlit as st
import sqlite3

conn = sqlite3.connect('userData.db')
c = conn.cursor()

def loginUser(username, password):

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    if user:
        return True
    else:
        return False

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

conn.close()