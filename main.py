import streamlit as st
import pymysql
from urllib.parse import quote

conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='Kin@ub01',
    db='userIdentificationSystem'
)

cursor = conn.cursor()

# sql queries
getUser = 'SELECT * FROM userInfo WHERE username = %s AND password = %s'
fetchUser = 'SELECT * FROM userInfo WHERE username = %s'
createUser = 'INSERT INTO userInfo (username, email, contact, password) VALUES (%s, %s, %s, %s)'
updateUserInfo = 'UPDATE userInfo SET email = %s, contact = %s WHERE username = %s'
updatePwd = 'UPDATE userInfo SET password = %s WHERE username = %s'

# UI
st.title("User Identification System")

option = st.sidebar.selectbox("What do you want to do?", ["Home", "Login", "Sign Up", "View Data", "Update Info", "Update Password"])

if (option == "Home") :
    st.header("Choose desired option from the sidebar")

elif (option == "Login") :
    st.header("For Existing Users")
    username = st.text_input("Enter Username")
    pwd = st.text_input("Enter Password", type="password")

    loginBtn = st.button("Login")
    
    if (loginBtn) :
        cursor.execute(getUser, (username, pwd))
        user = cursor.fetchone()
    
        if (user) :
            st.success("Log in success")
            st.markdown("<h1>Welcome <span style='color: cyan'>{}</span></h1>".format(username), unsafe_allow_html=True)
        else :
            st.error("Invalid UserId / Password")

elif (option == "Sign Up") :
    st.header("For New Users")
    username = st.text_input("Enter Username")
    email = st.text_input("Enter email")
    contact = st.text_input("Enter Contact No.")
    pwd = st.text_input("Enter Password", type="password")

    registerBtn = st.button("Sign Up")

    if (registerBtn) :
        cursor.execute(fetchUser, (username))
        user = cursor.fetchone()

        if (user) :
            st.error("Username exists already. Try another one")
        else : 
            cursor.execute(createUser, (username, email, contact, pwd))
            conn.commit()
            st.success("User Created")
            st.success("Please Login")
            
elif (option == "View Data") :
    st.header("View User Data")
    username = st.text_input("Enter Username")

    viewDataBtn = st.button("View Data")

    if (viewDataBtn) :
        cursor.execute(fetchUser, (username))
        user = cursor.fetchone()

        if (user) :
            st.write("Username : {}".format(user[1]))
            st.write("Email : {}".format(user[2]))
            st.write("Contact : {}".format(user[3]))
        else : 
            st.warning("User does not exist")

elif (option == "Update Info") :
    st.header('Update User Info')
    username = st.text_input("Enter Username")
    pwd = st.text_input("Enter password", type="password")
    email = st.text_input("Enter Updated Email")
    contact = st.text_input("Enter Updated Contact")

    cursor.execute(getUser, (username, pwd))
    user = cursor.fetchone()

    updateInfoBtn = st.button("Update Info")
    
    if (updateInfoBtn) :
        if (user) :
            cursor.execute(updateUserInfo, (email, contact, username))
            conn.commit()
            st.success("Record updated successfully!")
        else :
            st.warning("Incorrect username / password")

elif (option == "Update Password") :
    st.header('Update Password')
    username = st.text_input("Enter username")
    pwd = st.text_input("Enter old passowrd", type="password")
    newPwd = st.text_input("Enter new password", type="password")


    updatePwdBtn = st.button("Update Password")

    if (updatePwdBtn) :
        cursor.execute(getUser, (username, pwd))
        user = cursor.fetchone()
        
        if (user) :
            cursor.execute(updatePwd, (newPwd, username))
            conn.commit()
            st.success("Passwod updated successfully!")
        else :
            st.warning("Incorrect username / password")



cursor.close()
conn.close()
