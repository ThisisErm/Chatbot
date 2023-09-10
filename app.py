import os
import streamlit as st
from langchain.llms import OpenAI
from apikey import apikey
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

# Import API keys
os.environ['OPENAI_API_KEY'] = apikey


if not firebase_admin._apps:
    cred = credentials.Certificate('project_key.json')
    firebase_admin.initialize_app(cred)


def app():
    st.title('🔥Erm\'s AI Chatbot 💯')
    
    
    # MANAGE STATE
    if 'username' not in st.session_state:
        st.session_state.username =''
    if 'usermail' not in st.session_state:
        st.session_state.usermail = ''
    
    
    # LOGIN LOGIC
    def logIn():
        try:
            user = auth.get_user_by_email(email)
            st.warning('Login Successful')
            
            # MANAGE STATE
            st.session_state.username = user.uid
            st.session_state.username = user.email
            
            st.session_state.signedOut = True
            st.session_state.signOut = True


            
           

        except:
            st.warning('Login Failed')
            
    # LOG OFF LOGIC
    def logOff():
        st.session_state.signOut = False
        st.session_state.signedOut = False
        st.session_state.username= ''
        
            
    if 'signedOut' not in st.session_state:
        st.session_state.signedOut = False
    if 'signOut' not in st.session_state:
        st.session_state.signOut = False
        
    if not st.session_state['signedOut']:
        choice = st.selectbox('Login/Signup', ['Log In', 'Sign Up'])

            
            
            
        
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
    
    if st.session_state.signOut:
        st.sidebar.header(f'Welcome {st.session_state.username}!')
        
        #LLM (temp decides how creative)
        llm = OpenAI(temperature=0.9)

        #LLM's response (prompt)
        prompt = st.text_input('How can I help?') 
        
        if prompt:
            response = llm(prompt)
            st.write(response)

        # LLM's response (file)
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file:
            file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type, "filesize": uploaded_file.size}

            if uploaded_file.type == "text/plain":
                raw_text = str(uploaded_file.read(), "utf-8") 
                st.write(file_details)
                st.write(raw_text)
                response = llm(raw_text)
                st.write(response)
            else:
                st.write("Please upload a text file.")
        
    
        
        st.sidebar.button('Sign Out', on_click =logOff, key='logoff')
        
        
            
app()
    
