import mysql.connector

############# Connecting To Mysql db#######################
def connect():
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="starkk",
	  password="Bimal24625",
	  db="system1"
	)
	return mydb
###########################################################
mydb=connect()
mycursor = mydb.cursor()

# mycursor.execute('ALTER TABLE doctors ADD slots VARCHAR(255)')
# mydb.commit()
# mycursor.execute("CREATE table patients (first_name VARCHAR(20),last_name VARCHAR(20),email VARCHAR(20),password VARCHAR(50),phone_number int(10),dob int(10),gender VARCHAR(6))")
# mycursor.execute("INSERT INTO doctors (first_name,last_name,email,password,phone_number,dob,gender) values('Bimal','Singh','bimalsingh@gmail.com','Bimal1234','9654875631','22092000','male')")

# print(mycursor.rowcount, "record inserted.")
# mycursor.execute("DROP table patient")
# mycursor.execute("SELECT * from patient")
# print(mycursor.fetchall())
mydb.commit()
