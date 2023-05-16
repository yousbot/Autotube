from instagrapi import Client
from termcolor import colored 

def upload_to_instagram():

    username = "username"
    password = "password"
    client = Client() 
    client.login(username, password) 
    print(colored("[ Logged in to instagram. ]",'blue'))
    send_to = client.user_id_from_username(username="sbaiidrissiyoussef")
    client.direct_send(text="Hello my friend from the other world.", user_ids=[send_to])
    print(colored("[ Message sent. ]",'blue'))
    

