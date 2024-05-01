import streamlit as st
import sqlite3
import hashlib
import os
from streamlit_option_menu import option_menu
from PIL import Image
import yaml

data = {}
filename = 'user_data.yaml' 



def hash_password(password):
    # Create a hash object using SHA-256
    h = hashlib.sha256()
    # Update the hash object with the encoded password string
    h.update(password.encode('utf-8'))
    # Get the hashed password as a hexadecimal string
    password_hash = h.hexdigest()
    return password_hash



# Fonction pour vérifier les informations d'identification dans la base de données
def check_credentials(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM users WHERE username=? AND password=?''', (username, password))
    user_id = c.fetchone()
    conn.close()
    return user_id

def main():
    # Barre de navigation horizontale
    st.markdown(
        """
        <style>
            .navbar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 20px;
                background-color: #f0f0f0;
            }
            .nav-item {
                margin: 0 10px;
                cursor: pointer;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    selected_option = option_menu(
        menu_title=None,
        options=["login", "About our application"],
        icons=['lock', 'house'],
        menu_icon="cast", default_index=0, orientation="horizontal",
    )
    
    if selected_option == "login":
        st.title("login page")
        # Créer des zones de saisie pour le nom d'utilisateur et le mot de passe
        username = st.text_input("username")
        password = st.text_input("password", type="password")
        hashed_password = hash_password(password)
        
        # Bouton de connexion
        if st.button("login"):
            
            user_id = check_credentials(username, hashed_password)
            if user_id is not None:
                #Creating a dictionary of tuple for each session e.g {'5':('5','a,'fdsgg','a')} so one key one value (which is the tuple) dictionary in each session
                data[user_id[0]]= user_id
                yaml_data = yaml.dump(data)
                
                with open('user.yaml', 'w') as file:
                    file.write(yaml_data)
            
                st.session_state['user_id'] = user_id
                st.success("Login successful! Redirecting to the main page...")
                # Redirection vers la page app.py

                st.write(f"Welcome, {username}! :wave:")
 
                st.session_state.logged_in = True

                os.system("streamlit run main.py --server.enableXsrfProtection=false")
            else:
                st.error("Username or password incorrect.")


        # Bouton de création d'un compte
        if st.button("sign up"):
            # Redirection vers la page creation.py
            os.system("streamlit run creation.py --server.enableXsrfProtection=false")

    elif selected_option == "About our application":
        st.title("About our application :")
        # Définir le style CSS pour le titre
        title_style = """
            color: #1f77b4;
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
        """

        # Afficher le titre avec le style personnalisé
        st.markdown(
            f'<p style="{title_style}">"Sign language translator"</p>',
            unsafe_allow_html=True
        )

        # Définir un style pour le texte de la description
        description_style = "font-size: 18px; line-height: 1.6; color: #333;"

        # Afficher la description avec un style personnalisé
        st.markdown(
            """
            <div style="{style}">
            Our sign language translation application aims to facilitate communication between deaf or hard of hearing individuals and hearing individuals. By using our application, users can simply make sign language gestures in front of their camera, import an image or video, and our intelligent system translates these gestures in real-time into text or audible speech. This groundbreaking technology helps overcome language barriers and promotes smooth and efficient communication in various contexts, whether it be at school, work, or in daily life.
            </div>
            """.format(style=description_style),
            unsafe_allow_html=True
        )

        # Ajouter une phrase d'introduction avant la vidéo
        st.markdown(
            """
            <br>
            <div style="{style}">
            To enhance your sign language learning experience, watch the video below:
            </div>
            """.format(style=description_style),
            unsafe_allow_html=True
        )

        # Ajouter la vidéo avec des contrôles
        video_url = "https://www.youtube.com/watch?v=G6hVRVG74lc"  
        st.video(video_url)

if __name__ == "__main__":
  
   main()

    
    