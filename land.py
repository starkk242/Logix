from flask import Flask, render_template,request
import hashlib
from db_conn import connect
import ast

mydb=connect()
mycursor = mydb.cursor()

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('landing.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/register',methods=['POST'])
def register():
	first_name=request.form['fname']
	last_name=request.form['lname']
	email=request.form['email']
	password=request.form['password']
	hash_object = hashlib.md5(password.encode())
	paswd_hash = hash_object.hexdigest()
	gender=request.form['gender']
	role=request.form['role']
	dob=request.form['dob']
	ph_num=request.form['phone_number']
	if role=='doctor':
		sql="INSERT INTO doctors (first_name,last_name,email,password,dob,gender) values (%s,%s,%s,%s,%s,%s)"
		val=(first_name,last_name,email,paswd_hash,dob,gender)
		mycursor.execute(sql,val)
		mydb.commit()
		return  '<b>Thank you Dr. %s %s for registering with us</b>'%(first_name,last_name)
	elif role=='patient':
		sql="INSERT INTO patients (first_name,last_name,email,password,dob,gender) values (%s,%s,%s,%s,%s,%s)"
		val=(first_name,last_name,email,paswd_hash,dob,gender)
		mycursor.execute(sql,val)
		mydb.commit()
		return  'Thank you %s %s for registering with us'%(first_name,last_name)


@app.route('/login_form',methods=['POST'])
def login_form():
	email=request.form['email']
	password=request.form['password']
	hash_object = hashlib.md5(password.encode())
	paswd_hash = hash_object.hexdigest()
	sql='SELECT password from doctors where email = %s'
	val=(email,)
	mycursor.execute(sql,val)
	f=mycursor.fetchall()
	if len(f)==0:
		sql='SELECT password from patients where email = %s'
		val=(email,)
		role=2
		mycursor.execute(sql,val)
		f=mycursor.fetchall()
		first_name,last_name=dashboard(email,role)
	else:
		role=1

	if f[0][0]==paswd_hash:
		first_name,last_name=dashboard(email,role)
		if role == 1:
			return render_template("doctor_dashboard.html",fname=first_name,lname=last_name)
		elif role == 2:
			mycursor.execute('SELECT first_name,email from doctors')
			f=mycursor.fetchall()
			doc_list=[]
			for i in f:
				doc_list.append(i[0])
			return render_template("patient_dashboard.html",fname=first_name,lname=last_name,len=len(doc_list),doc_list=doc_list)
	return "Incorrect Username or Password"

@app.route('/doctor_select',methods=['POST'])
def doctor_select():
	mydb=connect()
	mycursor = mydb.cursor()
	doc_name=request.form['doc_name']
	sql='SELECT slots from doctors where first_name = %s'
	val=(doc_name,)
	mycursor.execute(sql,val)
	f=mycursor.fetchall()
	if len(f)==0:
		return "Slots Not Selected by doctor"
	else:
		f=f[0][0]
		f=ast.literal_eval(f)
		available_slot=[]
		for i in f.keys():
			if f[i]=='0':
				available_slot.append(i)
		return render_template("booking.html",len=len(available_slot),available_slot=available_slot,doc_name=doc_name)

@app.route('/book_slot',methods=['POST'])
def book_slot():
	mydb=connect()
	mycursor = mydb.cursor()
	selected_slot=request.form['selected_slot']
	doc_name=request.form['doc_name']
	sql = 'SELECT slots from doctors where first_name = %s'
	val = (doc_name,)
	mycursor.execute(sql,val)
	av_slots=mycursor.fetchall()[0][0]
	available_slot=ast.literal_eval(av_slots)
	print(selected_slot)
	for i in available_slot:
		if i==selected_slot:
			print(i)
			available_slot[i]='1'
	update_db(available_slot,doc_name)
	return "Slot Booked"


@app.route('/slot',methods=['POST'])
def slot():
	mydb=connect()
	mycursor = mydb.cursor()
	slot=request.form['slot']
	start_time=request.form['start_time']
	end_time=request.form['end_time']
	doc_name=request.form['doc_name']
	start_hr,start_min=str.split(start_time,':')
	end_hr,end_min=str.split(end_time,':')
	start_hr=int(start_hr)
	start_min=int(start_min)
	end_hr=int(end_hr)
	end_min=int(end_min)
	slot=float(slot)
	slot=int(slot*60)
	available_slot={}
	slots=[]
	slots.append(str(start_hr)+':'+str(start_min))
	time_min=start_min
	time_hr=start_hr
	while True:
		if slot==30:	
			if time_min==30:
				time_hr=time_hr+1
				time_min=00
			else:
				time_min=30
		elif slot==60:
			time_hr=time_hr+1
			time_min=00
		slots.append(str(time_hr)+':'+str(time_min))
		Endt = str(end_hr)+':'+str(end_min)
		if (str(time_hr)+':'+str(time_min))==Endt:
			break
	for i in slots:
		available_slot[i]='0'
	update_db(available_slot,doc_name)
	return available_slot

def update_db(available_slot,doc_name):
	mydb=connect()
	mycursor = mydb.cursor()
	mydb=connect()
	mycursor = mydb.cursor()
	available_slot= str(available_slot)
	print(available_slot)
	sql="UPDATE doctors set slots=%s where first_name=%s"
	val=(available_slot,doc_name)
	mycursor.execute(sql,val)
	mydb.commit()


def dashboard(email,role):
	mydb=connect()
	mycursor = mydb.cursor()
	if role==1:
		sql='SELECT first_name,last_name from doctors where email = %s'
		val=(email,)
	elif role==2:
		sql='SELECT first_name,last_name from patients where email = %s'
		val=(email,)
	mycursor.execute(sql,val)
	f=mycursor.fetchall()[0]
	first_name=f[0]
	last_name=f[1]
	return (first_name,last_name)



if __name__=='__main__':
	app.run(host='0.0.0.0',port = 8090,debug=True)
