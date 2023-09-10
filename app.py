import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth


if not firebase_admin._apps:
    cred = credentials.Certificate('project_key.json')
    firebase_admin.initialize_app(cred)


def app():
    st.title('Chatbot 2.0')
    
    choice = st.selectbox('Login/Signup', ['Log In', 'Sign Up'])
    
    
    # LOGIN LOGIC
    def logIn():
        try:
            user = auth.get_user_by_email(email)
            st.warning('Login Successful')
            
            st.header('My header')
            st.subheader('My sub header')

        except:
            st.warning('Login Failed')
    
    if choice == 'Log In':
        email = st.text_input('Email Address')
        password = st.text_input('Password', type ='password' )
                
        st.button('Log In', on_click= logIn, key='login')
    
    else: 
        email = st.text_input('Email Address')
        password = st.text_input('Password', type ='password' )
        username = st.text_input('Create a username' )
            
    # SIGNUP LOGIC
        if st.button('Sign Up'):
            user = auth.create_user(email = email, password = password, uid = username)
                
            st.success('Account Created Successfully')
            st.markdown('Please Log In using your email and password')
            st.balloons()
                
            
app()
    
