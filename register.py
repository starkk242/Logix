from db_conn import connect


mydb=connect()
mycursor=mydb.cursor()

def register():
	role=input("For 1.Doctor \n 2.Patient")
	fname=input("Enter Fname")
	lname=input("Enter Lname")
	email=input("Enter email")
	password=input("Enter password")
	gender=input("Enter gender")
	dob=input("Enter date of birth")
	phone_number1=input("Phone Number1:")
	phone_number2=input("Phone Number2:")
	phone_number3=input("Phone Number3:")
	

	if role=='1':
		sql="INSERT INTO doctors (first_name,last_name,email,password,gender) values (%s,%s,%s,%s,%s)"
		val=(fname,lname,email,password,gender)
		sql1="INSERT INTO phone_number (email,ph1,ph2,ph3) values (%s,%s,%s,%s)"
		val1=(email,phone_number1,phone_number2,phone_number3)
	elif role=='2':
		sql="INSERT INTO patients (first_name,last_name,email,password,gender) values (%s,%s,%s,%s,%s)"
		val=(fname,lname,email,password,gender)
		sql1="INSERT INTO phone_number (email,ph1,ph2,ph3) values (%s,%s,%s,%s)"
		val1=(email,phone_number1,phone_number2,phone_number3)
	mycursor.execute(sql,val)
	mycursor.execute(sql1,val1)
	mydb.commit()

def get_table_data():
	mycursor.execute("Select * from doctors")
	print(mycursor.fetchall())