#Use this to manually update/add/remove emails from emails database if cannot update using Flask Web App


import mysql.connector
# ********************************* MySQL DATABASE CONNECTION INITIALIZATION *************************************************************************
DatabaseConnection = mysql.connector.connect(host="localhost",
  user = 'USERNAME',
  passwd="PASSWORD",
  database = 'DATABASE NAME',
  auth_plugin='mysql_native_password'
)

cursorConnect = DatabaseConnection.cursor() # Used as a pointer to navigate where in the database you want do database manipulation


cursorConnect.execute("""CREATE TABLE Emails_names(
                     Person text,
                     Email text
                     

                      )""") #Comment these lines out after first run
#******************************************************************************************************************************************


# ********************************************* Functions for insertion, Selection/Queries, and Removal of Data from Database *************************************
def insertion(objectName):
    
    cursorConnect.execute("INSERT INTO Emails_names VALUES(%s,%s)",(objectName[0],objectName[1]))
    DatabaseConnection.commit()                        

def Selection_DataRetrieval(): 
    cursorConnect.execute("SELECT DISTINCT * FROM Emails_names") 
                                    
Email = ["Anando Zaman","anando@email.com"]
Email1 = ["Satya Nadella","Satya@email.com"]
Email2 = ["Tim Cook","Tim@email.com"]
Email2 = ["Mark Zuckerberg","Mark@email.com"]


insertion(Email)

#USED FOR UPDATING DATA
'''cursorConnect.execute(""" UPDATE Emails_names SET Email = %s
                                WHERE Person = %s """,("anando@email.com","anando100@gmail.com",))
DatabaseConnection.commit() ''' 

'''#DATA REMOVAL
cursorConnect.execute("DELETE from Emails_names WHERE Email = %s ",("anando@email.com",))
DatabaseConnection.commit()'''

#DATA RETRIEVAL
#cursorConnect.execute("SELECT Environment_Data FROM ENV_names WHERE Scriptname = 'VirginnonprodIOS' ")
#print(cursorConnect.fetchall())
DatabaseConnection.close()

