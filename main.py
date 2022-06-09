from faulthandler import disable
import tkinter as tk
from tkinter.font import BOLD
import create_user
import authenticate_user as auth
from tkinter import CENTER, END, StringVar, messagebox
import os.path
import json
import re
import pyperclip
from tkinter import ttk




def get_user_data(creds):
    path=os.path.join(r'users',creds.get('hashed_username'),creds.get('hashed_username')+'.json')
    file=open(path,'r')
    usr_data=json.loads(file.read())
    file.close()
    return usr_data 
        
def user_data_overwrite(creds,data):
    #print(creds)
    path=os.path.join(r'users',creds.get('hashed_username'),creds.get('hashed_username')+'.json')
    file=open(path,'w')
    js=json.dumps(data)
    print(js)
    file.write(js)
    file.close()

def onselect(evt):
    widget = evt.widget
    index = int(widget.curselection()[0])
    value = widget.get(index)
    items=data.get(value)
    listbox_items.delete(0,END)
    for item in items:
        listbox_items.insert('end',item)


def search(evt):
    selected= data.copy()
    searchvar=evt.widget.get()
    #print(searchvar)
    
    if searchvar :
        for key in list(data.keys()):
            if not (re.search(searchvar,key,re.IGNORECASE)):
                selected.pop(key)
            listbox_accounts.delete(0,END)
            for item in selected:
                listbox_accounts.insert('end',item)
    else:
        listbox_accounts.delete(0,END)
        for key in list(data.keys()):
            listbox_accounts.insert('end',key)

def copy(self):
    widget = self.widget
    index = int(widget.curselection()[0])
    value = widget.get(index)
    items=data.get(value)
    pyperclip.copy(value)

def edit_mode(root,creds):
        clear_slaves(root)
        edit_window(root,creds)
def default_mode(root,creds):
        clear_slaves(root)
        default_window(root,creds)

def  Option_menu(self):
    options={
        'Edit mode':edit_mode,
        'Default mode':default_mode
    }
    widget = self.widget
    option=widget.get()

    options[option](widget.master,creds)

def default_window(root,creds):
    root.title('Sentinel')
    root.configure(bg='#635d5d')   
    root.geometry('865x600')


    global data
    data=get_user_data(creds)
    

    
    global variable
    variable = StringVar(root)
    variable.set('Menu') # default value
    dropdown_menu=ttk.Combobox(root,textvariable=variable)
    dropdown_menu['values']=('Default mode','Edit mode')
    dropdown_menu['state'] = 'readonly'
    dropdown_menu.configure(font=('Helvetica',18,BOLD),justify=CENTER)
    dropdown_menu.bind("<<ComboboxSelected>>",Option_menu)
    dropdown_menu.grid(row=1,column=0,columnspan=2,sticky='NW',pady=(0,20))




    username_label=tk.Label(root,text=f'usr : {creds.get("username")}',font=('Helvetica',20,BOLD),bg='navajowhite')
    username_label.grid(row=1,column=0,columnspan=3,padx=(5,0),pady=(45,0),sticky='NW')
    #search entry
    search_label=tk.Label(root,text='Search :',font=('Helvetica',20,BOLD),justify=CENTER,bg='navajowhite')
    search_label.grid(row=2,column=0,padx=(5,0),ipadx=5,pady=(25,0),sticky='NW')

    search_entry=tk.Entry(root,width=20,font=('Helvetica',20,BOLD))
    search_entry.bind('<Return>',search)
    search_entry.grid(row=2,column=1,padx=(10,0),pady=(25,0),sticky='W')

   
    #item list
    global listbox_items
    items=[]
    items_var=tk.StringVar(value=items)
    listbox_items = tk.Listbox(root, listvariable=items_var, height=12,width=30)
    listbox_items.configure(font=('Helvetica',20,BOLD),justify=CENTER,bd=3,bg='navajowhite')
    listbox_items.bind("<<ListboxSelect>>",copy)
    listbox_items.grid(row=3,column=0,columnspan=3,padx=(5,0),pady=(25,0),sticky='W')

    #content list
    global listbox_accounts
    content=list(data.keys())
    content_var=tk.StringVar(value=content)
    listbox_accounts = tk.Listbox(root, listvariable=content_var, height=17,width=23)
    listbox_accounts.bind("<<ListboxSelect>>",onselect)
    listbox_accounts.configure(font=('Helvetica',20,BOLD),justify=CENTER,bd=3,bg='navajowhite')
    listbox_accounts.grid(row=1,rowspan=3,column=2,padx=(60,0),pady=(5,0),sticky='NE')

    scrollbar = tk.Scrollbar(root)
    listbox_accounts.config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = listbox_accounts.yview)
    scrollbar.grid(row=1,rowspan=3,column=2,padx=(0,0),pady=(25,25),sticky='NSE')

def button_save_callback(creds):
    #print(creds)
    global data
    static_account_name=entry_current_edit.get()
    account_name=static_account_name
    text= text_items.get("1.0",END)
    print(text)
    print(type(text))
    
    items=text.split('\n')
    print(items)
    for i in range(len(items)):
        items[i]=items[i].strip()
    while(True):
        if('' in items):
            items.remove('')
        else:
            break
    account={account_name:items}   
    if not account_name in list(data.keys()):
        data.update(account)
        user_data_overwrite(creds,data)
        messagebox.showinfo('message','Save successful!')
    else:
        message='The account already exits! Are you sure you want to owerwrite it?'
        answer = messagebox.askyesno('Sentinel', message)
        if answer==True:
            data.pop(static_account_name)
            data.update(account)
            user_data_overwrite(creds,data)

def edit_window(root,creds):
    #print(creds)
    def onselect(evt):
        widget = evt.widget
        index = int(widget.curselection()[0])
        value = widget.get(index)
        items=data.get(value)
        text_items.delete(1.0,END)
        entry_current_edit.delete(0,END)
        entry_current_edit.insert(0,value)
        for item in items:
            text_items.insert(1.0,item+'\n')

    
    

    global variable
    variable = StringVar(root)
    variable.set('Menu') # default value
    dropdown_menu=ttk.Combobox(root,textvariable=variable)
    dropdown_menu['values']=('Default mode','Edit mode')
    dropdown_menu['state'] = 'readonly'
    dropdown_menu.configure(font=('Helvetica',18,BOLD),justify=CENTER)
    dropdown_menu.bind("<<ComboboxSelected>>", Option_menu)
    dropdown_menu.grid(row=1,column=0,columnspan=2,sticky='NW',pady=(0,20))




    username_label=tk.Label(root,text=f'usr : {creds.get("username")}',font=('Helvetica',20,BOLD),bg='navajowhite')
    username_label.grid(row=1,column=0,columnspan=3,padx=(5,0),pady=(45,0),sticky='NW')
    #search entry
    search_label=tk.Label(root,text='Search :',font=('Helvetica',20,BOLD),justify=CENTER,bg='navajowhite')
    search_label.grid(row=2,column=0,padx=(5,0),ipadx=5,pady=(25,0),sticky='NW')

    search_entry=tk.Entry(root,width=20,font=('Helvetica',20,BOLD))
    search_entry.bind('<Return>',search)
    search_entry.grid(row=2,column=1,padx=(10,0),pady=(25,0),sticky='W')

   
    #item text
    global entry_current_edit
    entry_current_edit=tk.Entry(root,text='',font=('Helvetica',20,BOLD),bg='navajowhite')
    entry_current_edit.configure(width=26,border=3)
    entry_current_edit.grid(row=3,column=0,columnspan=3,padx=(10,0),pady=(30,0),sticky='W')

    global text_items
    
    text_items = tk.Text(root, height=8,width=30)
    text_items.configure(font=('Helvetica',20,BOLD),bd=3,bg='navajowhite')
    text_items.grid(row=4,column=0,columnspan=3,padx=(5,0),pady=(5,0),sticky='NW')

    button_save=tk.Button(root,text='Save',font=('Helvetica',16,BOLD),height=1,bg='#ea6f04',command=lambda:button_save_callback(creds))
    button_save.configure(border='4')
    button_save.grid(row=5,column=1,pady=25,sticky='S',padx=5)

    #content list
    global listbox_accounts
    content=list(data.keys())
    content_var=tk.StringVar(value=content)
    listbox_accounts = tk.Listbox(root, listvariable=content_var, height=17,width=23)
    listbox_accounts.bind("<<ListboxSelect>>",onselect)
    listbox_accounts.configure(font=('Helvetica',20,BOLD),justify=CENTER,bd=3,bg='navajowhite')
    listbox_accounts.grid(row=1,rowspan=5,column=2,padx=(60,0),pady=(5,0),sticky='NE')

    scrollbar = tk.Scrollbar(root)
    listbox_accounts.config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = listbox_accounts.yview)
    scrollbar.grid(row=1,rowspan=5,column=2,padx=(0,0),pady=(25,25),sticky='NSE')

def main():
    global data
    root=tk.Tk()
    root.title('Sentinel')
    photo = tk.PhotoImage(file = r"settings\icon.gif")
    root.iconphoto(False, photo)
    root.geometry('750x250')
    root.configure(bg='#635d5d')

    style = ttk.Style()
    comboboxstyle = ttk.Style()
    comboboxstyle.theme_create('combostyle', parent='clam', settings = {'TCombobox': 
                                                             {'configure': {'selectbackground': 'navajowhite',
                                                                            'fieldbackground': 'navajowhite',
                                                                            'background': 'white',
                                                                            'bordercolor':'black',
                                                                           'selectforeground': 'black'}}})

    style.theme_use('combostyle')
   

    #root.protocol("WM_DELETE_WINDOW", disable)
        #create user button
    button_new_user=tk.Button(root,text='Create User',font=('Helvetica',10,BOLD),width=20,height=2,command=lambda:button_new_user_callback(root))
    button_new_user.configure(border='3',background='navajowhite')
    button_new_user.grid(row=0,column=0,pady=10,sticky='NW',padx=5)
        #username input
    entry_username = tk.Entry(root,width=28,font=('Georgia 18'))
    entry_username.grid(row=1,column=1,pady=10,padx=5)
    
    label_username=tk.Label(root,text='Username :',font=('Helvetica',14,BOLD),bg='navajowhite')
    label_username.grid(row=1,column=0,pady=10,padx=(0,5))
        #password input
    entry_password = tk.Entry(root,width=28,font=('Georgia 18'))
    entry_password.grid(row=2,column=1,padx=5)

    label_password=tk.Label(root,text='Password :',font=('Helvetica',14,BOLD),bg='navajowhite')
    label_password.grid(row=2,column=0,pady=10,padx=(0,5))
        #login button
    button_login=tk.Button(root,text='Login',font=('Helvetica',14,BOLD),width=15,height=1,bg='#ea6f04',command=lambda:button_login_callback(root,entry_username,entry_password))
    button_login.configure(border='4')
    button_login.grid(row=3,column=1,pady=25,sticky='SE',padx=5)

    root.mainloop()

def clear_slaves(root):
    list = root.grid_slaves()
    for l in list:
        l.destroy()

def button_login_callback(root,entry_username,entry_password):
    username=entry_username.get()
    password=entry_password.get()
    
    authentication=auth.authenticate(username,password)
    message ='User logged in successfully!' if authentication else 'User login failed!'
    messagebox.showinfo('message',message)
    if authentication:
        hashed_username,hashed_password=auth.hash_creds(username,password)
        global creds
        creds={'username':username,'hashed_username':hashed_username,'password':password,'password':hashed_password}
        clear_slaves(root)
        default_window(root,creds)
        return creds

def button_submit_callback(create_user_window,entry_username,entry_password):
    username=entry_username.get()
    password=entry_password.get()
    message=''
    user_creation=create_user.create_user(username,password)
    message ='User created successfully!' if user_creation else 'User creation failed!'
    messagebox.showinfo('message',message)
    if (user_creation):
        create_user_window.destroy()
    

def button_new_user_callback(root):
    create_user_window=tk.Toplevel()
    create_user_window.title('Sentinel')
    photo = tk.PhotoImage(file = r"settings\icon.gif")
    create_user_window.iconphoto(False, photo)
    create_user_window.geometry('700x250')
    create_user_window.configure(bg='#635d5d')
    

        #username input
    entry_username = tk.Entry(create_user_window,width=28,font=('Georgia 18'))
    entry_username.grid(row=1,column=1,pady=(40,10),padx=5)
    
    label_username=tk.Label(create_user_window,text='Username :',font=('Helvetica',15,BOLD),bg='navajowhite')
    label_username.grid(row=1,column=0,pady=(40,10),padx=5)
        #password input
    entry_password = tk.Entry(create_user_window,width=28,font=('Georgia 18'))
    entry_password.grid(row=2,column=1,padx=5)

    label_password=tk.Label(create_user_window,text='Password :',font=('Helvetica',15,BOLD),bg='navajowhite')
    label_password.grid(row=2,column=0,pady=10,padx=5)
        #login button
    button_submit=tk.Button(create_user_window,text='Submit',font=('Helvetica',15,BOLD),width=15,height=1,bg='#ea6f04',command=lambda:button_submit_callback(create_user_window,entry_username,entry_password))
    button_submit.configure(border='4')
    button_submit.grid(row=3,column=1,pady=25,sticky='SE',padx=5)



    
main()