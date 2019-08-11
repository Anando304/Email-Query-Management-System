# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 12:53:21 2019

@author: anando.zaman
"""
#Environment Query & Email Alerts Management system
#Works in association with automated_emails script to update Email_Alerts List and Environments Names for Queries
#Web dashboard development using WebForms for POST requests, Jinja2 templating, login authentication with session decorators, and error handling.

from flask import Flask,render_template,request,redirect,url_for, session, g
import os
#import mysql.connector
from flask.ext.mysql import MySQL

app = Flask(__name__)
app.secret_key = os.urandom(24)

mysql = MySQL()
 
#************** MySQL configurations***************
app.config['MYSQL_DATABASE_USER'] = 'USERNAME'
app.config['MYSQL_DATABASE_PASSWORD'] = 'PASSWORD'
app.config['MYSQL_DATABASE_DB'] = 'DATABASE_NAME'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
#******************************************


@app.route('/Login', methods=['GET','POST'])    
    
def login():
    error = None
    if request.method == 'POST': #if we know that a POST request is being sent to the server using the /lOGIN route
                                 # This runs only when a POST in executed via button click and whatnot
                                 # A POST request is typically used for updating data and doing changes to the server such as reading input data from HTML and have the backend interpret and make use of it
                                 # A GET request is in URL form and is typically for fetching documents/data, not making changes to the server. Such as fetching an HTML webpage but not individual user inputted contents
                                 # request.form[name of textbox/button ui element] is used for doing anything with UI POST requests
        username = request.form['username'] #Retrieves information from the text field with name ID of username
        password = request.form['password'] #Retrieves information from the text field with name ID of password
        

        if((username!='ADMIN') and (password!='PASSWORD')):
            error = "Invalid credentials. Please try again"
            
            
        elif((username=='ADMIN') and (password=='PASSWORD')):
            session.pop('logged_in',None) #lOGOUT of any existing session
            session['logged_in'] = True
            return redirect(url_for('home')) #Routes to homepage. Could also do it using return home()
      
        else:
            error = "Invalid credentials. Please try again"
            
    return render_template('Login.html',error = error) #GETS the Login page if credentials are false
    


    
@app.before_request #Use of request decorators to check if a session is active before moving onto an authenticated page
def before_request():
    #g is a global variable representing the session
    g.logged_in = None
    if 'logged_in' in session: #If a user exists or is currently logged. logged_in is the key in the session that is associated with True
        g.user = session['logged_in']
    


@app.errorhandler(404) # For 404 errors
def page_not_found(e):
    if request.method == 'POST':
        if request.form['LoginRedirect'] == 'Login Page': #Login Page is the value associated with the button once clicked sending POST request data
           return redirect(url_for('login')) #Redirects to login page using login function. 
    return render_template('404.html')
    
@app.errorhandler(500)
def page_not_found500(e):
    if request.method == 'POST':
        if request.form['LoginRedirect'] == 'Login Page': 
           return redirect(url_for('login')) 
    return render_template('500.html')



@app.route('/home', methods=['GET','POST'])   #Authenticated HOMEpage
def home():
    if request.method == 'POST': #Used for buttons and ui processed from HTML to Flask backend
        if request.form['LogoutButton'] == 'Logout': #LogoutButton is the name of the HTML button. This button is also associated with a value set in HTML but can be dynamically set using things like forms
            session.pop('logged_in',None) #Pops the user value from the session dictionary essentially logging them out
            print("Successfully logged out")
            return redirect(url_for('login')) #Routes to homepage. Could also do it using return home()

            
    elif request.method == 'GET': #GET method is not necessary since python will know it by default
        if g.user: #If currently a user exists, this means user is logged in
            return render_template('index.html')

#************************************NON PROD ENVS********************************************************                     
@app.route('/CHROME', methods=['GET','POST'])  
def CHROME():
    if request.method == 'POST': 
        if request.form['submit'] == 'Logout': 
            session.pop('logged_in',None) #Pops the user value from the session dictionary essentially logging them out
            print("Successfully logged out")
            return redirect(url_for('login')) 
            
        if request.form['submit'] == 'submit': #"submit" value gets set when submit button pressed. This causes a POST request from webpage to Flask server
            ENVNAME = request.form['ENVNAME_textbox']
            if (ENVNAME!=""):
                print("VAlUE CHANGED")
                Environment = ENVNAME
                MyDB = mysql.connect()
                CursorConnect = MyDB.cursor()
                CursorConnect.execute(""" UPDATE ENV_names_Data SET Environment_Data = %s
                                WHERE Scriptname = %s """,(Environment,"WEB",))
                MyDB.commit() #Needed for databse updates
                return render_template('CHROME.html',Environment=Environment)
                #return redirect(url_for('login'))
                
    elif request.method == 'GET':
        MyDB = mysql.connect() 
        CursorConnect = MyDB.cursor()
        CursorConnect.execute("SELECT Environment_Data FROM ENV_names_Data WHERE Scriptname = 'WEB'")
        Environment = CursorConnect.fetchall()[0][0]        
        if g.user:
            return render_template('CHROME.html',Environment=Environment)

            
#**********************************************************************************************************    

    

#************************************P****PROD ENVS********************************************************                       
@app.route('/ANDROID', methods=['GET','POST'])  
def ANDROID():
    if request.method == 'POST': 
        if request.form['submit'] == 'Logout': 
            session.pop('logged_in',None) #Pops the user value from the session dictionary essentially logging them out
            print("Successfully logged out")
            return redirect(url_for('login')) 
            
        if request.form['submit'] == 'submit': #"submit" value gets set when submit button pressed. This causes a POST request from webpage to Flask server
            ENVNAME = request.form['ENVNAME_textbox']
            if (ENVNAME!=""):
                print("VAlUE CHANGED")
                Environment = ENVNAME
                MyDB = mysql.connect()
                CursorConnect = MyDB.cursor()
                CursorConnect.execute(""" UPDATE ENV_names_Data SET Environment_Data = %s
                                WHERE Scriptname = %s """,(Environment,"MOBILE",))
                MyDB.commit() #Needed for database updates
                return render_template('ANDROID.html',Environment=Environment)

                
    elif request.method == 'GET':
        MyDB = mysql.connect() 
        CursorConnect = MyDB.cursor()
        CursorConnect.execute("SELECT Environment_Data FROM ENV_names_Data WHERE Scriptname = 'MOBILE'")
        Environment = CursorConnect.fetchall()[0][0]        
        if g.user:
            return render_template('ANDROID.html',Environment=Environment)
        

#************************************EMAIL ALERTS******************************************************** 
#Email alerts page              
@app.route('/emailalerts', methods=['GET','POST'])  
def emailalerts():
    if request.method == 'POST': 
        if request.form['submit'] == 'Logout': 
            session.pop('logged_in',None) 
            print("Successfully logged out")
            return redirect(url_for('login')) 
            
        elif request.form['submit'] == 'ADD USER':
                return render_template('emailADD.html')
                
        elif request.form['submit'] == 'UPDATE USER': 
                return render_template('emailUPDATE.html')
        
        elif request.form['submit'][0:6] == 'Remove':
                user_to_remove = (request.form.get('submit')[9:-3]).strip() #Gets the email of user to remove              
                #return(user_to_remove)

                MyDB = mysql.connect() 
                CursorConnect = MyDB.cursor()
                CursorConnect.execute("DELETE from Emails_names WHERE Email = %s ", (user_to_remove,))
                MyDB.commit()
                return redirect(url_for('emailalerts'))
               

           
    elif request.method == 'GET':
        MyDB = mysql.connect() 
        CursorConnect = MyDB.cursor()
        CursorConnect.execute("SELECT Person FROM emails_names")
        listdata = CursorConnect.fetchall()
        CursorConnect.execute("SELECT Email FROM emails_names")
        listdataemail = CursorConnect.fetchall()
        if g.user:
            return render_template('emailalerts.html',listdata = listdata,listdataemail = listdataemail) 
  


          
@app.route('/emailADD', methods=['GET','POST'])  
def emailADD():
    if request.method == 'POST': 
        if request.form['submit'] == 'Logout': 
            session.pop('logged_in',None) 
            print("Successfully logged out")
            return redirect(url_for('login')) 
            
        if request.form['submit'] == 'SUBMIT': 
            username = request.form['Username']
            Email = request.form['Email'] #could also do .form.get(nameID) which returns None if the key name DNE
            MyDB = mysql.connect()
            CursorConnect = MyDB.cursor()
            CursorConnect.execute("INSERT INTO Emails_names VALUES(%s,%s)",(username,Email))
            MyDB.commit()
            success = "SUCCESSFULY UPDATED DATABASE"
            return render_template('emailADD.html',success=success)

           
    elif request.method == 'GET':
        if g.user:
            return render_template('emailADD.html') 
            

@app.route('/emailUPDATE', methods=['GET','POST'])  
def emailUPDATE():
    if request.method == 'POST': 
        if request.form['submit'] == 'Logout': 
            session.pop('logged_in',None) 
            print("Successfully logged out")
            return redirect(url_for('login')) 
            
        if request.form['submit'] == 'SUBMIT': 
            username = request.form.get('UsernameUPDATED')
            Email = request.form.get('EmailUPDATED')
            #return(Email) #To test on screen if input is recieved
            MyDB = mysql.connect()
            CursorConnect = MyDB.cursor()
            CursorConnect.execute(""" UPDATE Emails_names SET Email = %s
                                WHERE Person = %s """,(Email,username,))
            MyDB.commit()
            success = "SUCCESSFULY UPDATED DATABASE"
            return render_template('emailUPDATE.html',success=success)

           
    elif request.method == 'GET':
        if g.user:
            return render_template('emailUPDATE.html')
#**********************************************************************************************************    





          
if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)