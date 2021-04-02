from db_conn import connect

mydb=connect()
mycursor = mydb.cursor()
#mycursor.execute("SHOW TABLES")
#print(mycursor.fetchall())


def login(f):
	email=input("Email")
	password=input('Password')
	if f=='1':
		sql='SELECT password from doctors where email = %s'
		val=(email,)
	elif f=='2':
		sql='SELECT password from patients where email = %s'
		val=(email,)
	mycursor.execute(sql,val)
	passw=mycursor.fetchall()[0][0]
	if passw==password:
		print("Login Success")
	else:
		print("Login Failed")


#login(email,password)