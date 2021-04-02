import login
import register
import doctor_back

wtd=input("1. Register 2. Login 3. Create Slots 4. Make slots available \n")
exit=='n'
while exit != 'y':
	if wtd=='1':
		register.register()
		exit=input("Do you want to exit?y or n")
		wtd=input()
	elif wtd=='2':
		f=input("For 1.Doctor 2.Patient ")
		login.login(f)
		exit=input("Do you want to exit?y or n")
		wtd=input()
	elif wtd=='3':
		doctor_back.create_slots()
		exit=input("Do you want to exit?y or n")
		wtd=input()
	elif wtd=='4':
		doctor_back.make_all_slots_available()
		exit=input("Do you want to exit?y or n")
		wtd=input()