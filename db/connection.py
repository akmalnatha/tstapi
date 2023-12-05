from errno import errorcode
import os
import mysql.connector 


# Load the stored environment variables
# load_dotenv()

# Obtain connection string information from the portal
config = {
  'host': 'kai-access.mysql.database.azure.com',
  'user': 'akmalkomeng',
  'password':'mh$ITB550436',
  'database':'tstauthapi',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': '/DigiCertGlobalRootG2.crt.pem'
}

# Construct connection string
def connectDB():
  try:
    print("Connection established")
    return mysql.connector.connect(**config)
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with the user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
    