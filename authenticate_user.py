import re
import os.path
import hashlib

def sha3_256(string):
    hash=hashlib.sha256()
    hash.update(string.encode())
    return hash.hexdigest()

def get_user_list():
    users={}
    user_list_path=r'users\users\usr.seu'
    file=open(os.path.abspath(user_list_path))
    user_list_text=file.read()
    file.close
    user_list_text=re.findall('.'*128,user_list_text)
    for u in user_list_text:
        user=re.findall('.'*64,u)
        users.update({user[0]:user[1]})
    return users

def authenticate(username,password):
    hashed_username,hashed_password=hash_creds(username,password)
    user_list=get_user_list()
    user=user_list.get(hashed_username)
    return True if user==hashed_password else False

def hash_creds(username,password):
    hashed_username=sha3_256(username.strip())
    hashed_password=sha3_256(password.strip())
    return hashed_username,hashed_password

    


    