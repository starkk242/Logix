from db_conn import connect
mydb=connect()
mycursor = mydb.cursor()
available_slot={}
 
def create_slots():
	slot_amount=float(input("Time interval of a Slot like 0.5 or 1" ))
	start_time_hr=int(input("What is your starting Time hour? 10,11,12...likewise "))
	start_time_min=int(input("What is your starting Time minutes? 30 or 60 "))
	end_time_hr=int(input("What is your ending Time hour? 10,11,12...likewise "))
	end_time_min=int(input("What is your ending Time minutes? 30 or 60 "))

	slot=slot_amount*60
	slots=[]
	slots.append(str(start_time_hr)+':'+str(start_time_min))
	time_min=start_time_min
	time_hr=start_time_hr
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
		Endt = str(end_time_hr)+':'+str(end_time_min)
		if (str(time_hr)+':'+str(time_min))==Endt:
			break
	

	return slots

def book_slots(slot,doc_email):
	x=available_slot[slot]
	if x==0:
		available_slot[slot]='1'
		print("Slot booked")
		update_db(doc_email,available_slot)
		return True
	elif x==1:
		print("Slot Not available")
		return False

def make_all_slots_available():
	slots=create_slots()
	for i in slots:
		available_slot[i]='0'
	return available_slot

def update_db(doc_email,available_slot):
	updated_slots=(available_slot,)
	sql='UPDATE doctors SET slots %s where email = %s'
	val=(updated_slots,doc_email)
	mycursor.execute(sql,val)

def update_slots(doc_email):
	sql = 'SELECT slots from doctors where email = %s'
	val = (doc_email,)
	mycursor.execute(sql,val)
	av_slots=mycursor.fetchall()[0][0]
	available_slot=av_slot

create_slots()