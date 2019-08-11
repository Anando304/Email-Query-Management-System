#Query updater script
#Use this to manually update using Python parameters for MySQL if Flask web App does not work!


import mysql.connector
# ********************************* MySQL DATABASE CONNECTION INITIALIZATION *************************************************************************
DatabaseConnection = mysql.connector.connect(host="localhost",
  user = 'USERNAME',
  passwd="PASSWORD",
  database = 'DATABASE NAME',
  auth_plugin='mysql_native_password'
)

cursorConnect = DatabaseConnection.cursor() # Used as a pointer to navigate where in the database you want do database manipulation


cursorConnect.execute("""CREATE TABLE ENV_names_Data(
                     Scriptname text,
                     Environment_Data text
                     

                      )""") #Comment these lines out after first run
#******************************************************************************************************************************************


# ********************************************* Functions for insertion, Selection/Queries, and Removal of Data from Database *************************************
def insertion(objectName):
    
    cursorConnect.execute("INSERT INTO ENV_names_Data VALUES(%s,%s)",(objectName[0],objectName[1]))
    DatabaseConnection.commit()                        

def Selection_DataRetrieval(): 
    cursorConnect.execute("SELECT DISTINCT * FROM ENV_names_Data ") 
                                    
EnvironmentNames = ["MOBILE","AnandoZaman - Android (JSON) – PROD"]
EnvironmentNames1 = ["WEB","AnandoZaman - Chrome (JSON) – PROD"]


insertion(EnvironmentNames)
insertion(EnvironmentNames1)

#USED FOR UPDATING DATA
'''cursorConnect.execute(""" UPDATE ENV_names_Data  SET Environment_Data = %s
                                WHERE Scriptname = %s """,("AnandoZaman - Android (JSON) – PROD","MOBILE",))
DatabaseConnection.commit() ''' 


#DATA RETRIEVAL
#cursorConnect.execute("SELECT Environment_Data FROM ENV_names_Data  WHERE Scriptname = 'MOBILE' ")
#print(cursorConnect.fetchall())
DatabaseConnection.close()

