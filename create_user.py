import hashlib
import os
import authenticate_user as auth
import json




content={
    'password':'hkar5845000A',
    'email':'rajkovicaleksa@yahoo.com',
    'comment':'retardacija',
    'comment_2':'retardacija 2'
}


def sha3_256(string):
    hash=hashlib.sha256()
    hash.update(string.encode())
    return hash.hexdigest()

def check_if_exists(users_dir_path,hashed_username):
    files=os.listdir(users_dir_path)
    return False if hashed_username in files else True
    
    


def create_user(username,password):
    users_dir_path=r'users'
    user_list_path=r'users\users\usr.seu'
    hashed_username,hashed_password=auth.hash_creds(username,password)
    filename=hashed_username+'.json'
    if os.path.exists(user_list_path):
        if check_if_exists(users_dir_path,hashed_username):
            path=os.path.join(os.path.abspath(users_dir_path),hashed_username)
            os.mkdir(path)
            file=open(os.path.join(path,filename),'w')
            file.write(json.dumps({}))
            file.close()
            file_usrs=open(os.path.abspath(user_list_path),'a')
            file_usrs.write(hashed_username+hashed_password)
            file_usrs.close()
            return True
        else:
            return False




