#all the required modules are imported here
#the below import statement is for flask module 
from flask import Flask, render_template,request,redirect,url_for
#the below import statement is for datetime module for timestamp and timestamp to string and vice versa conversion
from datetime import datetime

app = Flask(__name__)

#user information after login gets initialised to variables defined below
name = "name"
username = "user name"
school = "school"
place_of_work = "place of work"
marital_status = "gender"
password = "password"
post_file_name = "post file name"
post_count = 0
post_file_primary_index = "post file primary index"
post_file_secondary_index = "post file secondary index"
last_login_date = "last login date"

#index records are stored here by default it is primary_index_records
primary_index_records = list()
secondary_index_records = list()
friends = list()
friends_friend_list = list()
friends_secondary_index_records = list()
friends_primary_index_records = list()

#gets the primary index of the post file into 2D list
def get_post_primary_index():
	global primary_index_records,username
	fh_post_file_primary_index = open(username+"_post_primary_index_file"+".txt", "r")
	index_content = fh_post_file_primary_index.read()
	index_entry = index_content.split('$') 
	index_entry.pop()
	for i in range(len(index_entry)):
		index_entry[i] = index_entry[i].split('|')
	primary_index_records = index_entry
	fh_post_file_primary_index.close()

#gets the friends primary index of the post file into 2D list
def get_friends_post_primary_index(friend_username):
	global friends_primary_index_records
	fh_post_file_primary_index = open(friend_username+"_post_primary_index_file"+".txt", "r")
	index_content = fh_post_file_primary_index.read()
	index_entry = index_content.split('$') 
	index_entry.pop()
	for i in range(len(index_entry)):
		index_entry[i] = index_entry[i].split('|')
	friends_primary_index_records = index_entry
	fh_post_file_primary_index.close()

#saves the primary index of the post file back to file in secondary storage
def save_post_primary_index():
	global primary_index_records
	fh_post_file_primary_index = open(username+"_post_primary_index_file"+".txt", "w")
	for entry in primary_index_records:
		file_entry = entry[0]+'|'+str(entry[1])+'$'
		fh_post_file_primary_index.write(file_entry)
	fh_post_file_primary_index.close()

#gets the secondary index of the post file into 2D list
def get_post_secondary_index():
	global secondary_index_records
	fh_post_secondary_index = open(username+"_post_secondary_index_file.txt", 'r')
	index_content = fh_post_secondary_index.read()
	index_entry = index_content.split('$')
	index_entry.pop()
	for i in range(len(index_entry)):
		index_entry[i] = index_entry[i].split('|')
		index_entry[i][0] = datetime.strptime(index_entry[i][0], '%Y/%m/%d')
	secondary_index_records = index_entry
	fh_post_secondary_index.close()

#saves the secondary index of the post file back to file in secondary storage
def save_post_secondary_index():
	global secondary_index_records
	fh_post_secondary_index = open(username+"_post_secondary_index_file.txt", 'w')
	for entry in secondary_index_records:
		entry[0] = entry[0].strftime("%Y/%m/%d")
		file_entry = make_file_string(entry)
		fh_post_secondary_index.write(file_entry)
	fh_post_secondary_index.close()

#gets the friends secondary index of the post file into 2D list
def get_friends_post_secondary_index(friend_username):
	global friends_secondary_index_records
	fh_post_secondary_index = open(friend_username+"_post_secondary_index_file.txt", 'r')
	index_content = fh_post_secondary_index.read()
	index_entry = index_content.split('$')
	index_entry.pop()
	for i in range(len(index_entry)):
		index_entry[i] = index_entry[i].split('|')
		index_entry[i][0] = datetime.strptime(index_entry[i][0], '%Y/%m/%d')
	friends_secondary_index_records = index_entry
	fh_post_secondary_index.close()

#pass a list of elements it returns a string with those concatenated
def make_file_string(element_list):
	file_entry_string = str()
	i = 0
	while i < len(element_list)-1:
		file_entry_string += str(element_list[i])+'|'
		i += 1
	file_entry_string += str(element_list[i])+"$"
	return file_entry_string

#gets the index file for inforamtion about users into 2D list
def get_user_index():
	global primary_index_records,username
	fh_user_index = open("users_index_file.txt", "r")
	index_content = fh_user_index.read()
	index_entry = index_content.split('$') 
	index_entry.pop()
	for i in range(len(index_entry)):
		index_entry[i] = index_entry[i].split('|')
	primary_index_records = index_entry
	fh_user_index.close()

#saves the index file of users back to the secondary storage
def save_user_index():
	global primary_index_records
	fh_user_index = open("users_index_file.txt", "w")
	for entry in primary_index_records:
		file_entry = entry[0]+'|'+str(entry[1])+'$'
		fh_user_index.write(file_entry)
	fh_user_index.close()

#binary search implementation 
def binary_search(key_element, index_records):
	count = 0
	low = 0
	high = len(index_records)-1
	while(low<=high):
		mid = (low+high)/2
		if index_records[mid][0] == key_element:
			return mid
			break
		elif index_records[mid][0] < key_element:
			low = mid+1
		else : 
			high = mid-1
	return -1

#after username and password is authenticated the below function gets the users information into the above declared variables
def get_user_information():
	global name,username, school, place_of_work,marital_status, password, post_file_name, post_count, post_file_primary_index, post_file_secondary_index, last_login_date
	fh_user = open(username+'.txt', 'r')
	user_record = fh_user.read().split('$')
	fh_user.close()
	user_record.pop()
	user_details = user_record[0].split('|')
	name = user_details[0]
	username = user_details[1]
	school = user_details[2]
	place_of_work = user_details[3]
	marital_status = user_details[4]
	password = user_details[5]
	post_file_name = user_details[6]
	post_count = int(user_details[7])
	post_file_primary_index = user_details[8]
	post_file_secondary_index = user_details[9]
	last_login_date = datetime.strptime(user_details[10], '%Y/%m/%d')

#this function takes a secondary index record's list as a parameter and gets all the details of the post and its content and returns a list of it for a particular days post 
def make_posts_list(post_file_of_username, list_of_primary_keys):
	fh_master_post_file = open(post_file_of_username+"_post_file.txt", 'r')
	post_list = [list_of_primary_keys[0].date()]
	for i in range(1, len(list_of_primary_keys)-1):
		primary_key = list_of_primary_keys[i]
		post_location = primary_index_records[binary_search(primary_key, primary_index_records)][1]
		fh_master_post_file.seek(int(post_location))
		posts = fh_master_post_file.read().split('$')
		post = posts[0].split('|')
		post[2] = datetime.strptime(post[2], "%H:%M:%S").time()
		post_list.append([post[2], post[3]])
	return post_list

#this function gets the friends of the user into friends list
def get_friends_list():
	global friends
	fh_friends_file = open(username+"_friends.txt",'r')
	all_friends = fh_friends_file.read()
	fh_friends_file.close()
	friends = all_friends.split('$')
	friends.pop()
	for i in range(len(friends)):
		friends[i] = friends[i].split('|')

#this function writes the friends list back to the friends file
def save_friends_list():
	fh_friends_file = open(username+"_friends.txt",'w')
	for element in friends:
		if element[1] != "Declined" and element[1] != "you_declined":
			fh_friends_file.write(element[0]+'|'+element[1]+'$')
	fh_friends_file.close()

#this function gets the friends of a friend into friends friend list
def get_friends_friend_list(username_of_friend):
	global friends_friend_list
	fh_friends_file = open(username_of_friend+"_friends.txt",'r')
	all_friends = fh_friends_file.read()
	fh_friends_file.close()
	friends_friend_list = all_friends.split('$')
	friends_friend_list.pop()
	for i in range(len(friends_friend_list)):
		friends_friend_list[i] = friends_friend_list[i].split('|')

#this function writes the friends friendfriends_friend_list list back to the friend's friends file
def save_friends_friend_list(username_of_friend):
	fh_friends_file = open(username_of_friend+"_friends.txt",'w')
	for element in friends_friend_list:
		if element[1] != "Declined":
			fh_friends_file.write(element[0]+'|'+element[1]+'$')
	fh_friends_file.close()

#fetches the list of users 
def get_to_friend_names():
	global friends_friend_list
	users_list = list()
	friends_already = list()
	fh_user_index = open('users_index_file.txt', 'r')
	all_users = fh_user_index.read()
	users = all_users.split('$')
	users.pop()
	get_friends_list()
	for element in friends:
		if element[1] == 'Confirmed' or element[1] == 'Requested' or element[1] == 'Requested_you':
			friends_already.append(element[0])
	friends_already.append(username)
	for i in range(len(users)) :
		users[i] = users[i].split('|')
		if users[i][0] not in friends_already:
			users_list.append(users[i][0])
	return users_list

#the applicaton starts with this as the first called function
@app.route("/")
def main():
	global username
	return render_template('login.html')

#this authenticates and validates the login page username and passwords
@app.route("/password_authentication")
def password_authentication():
	global username
	username = request.args.get('Username', '')
	entered_password = request.args.get('Password', '')
	get_user_index()
	search_return_index = binary_search(username, primary_index_records)
	if search_return_index == -1:
		return render_template('login.html')
	else :
		fh_master_user_file = open("master_user_file.txt", 'r')
		fh_master_user_file.seek(int(primary_index_records[search_return_index][1]))
		users_file_content = fh_master_user_file.read()
		users = users_file_content.split('$')
		user_credentials = users[0].split('|')
		fh_master_user_file.close()
		if entered_password == user_credentials[1]:
			get_user_information()
			return redirect(url_for('homepage'))
		else :
			return redirect(url_for('main'))

#sign up page starts exectution below
@app.route("/signup")
def signup():
	return render_template('signup.html')

#after the user provides his/her information this function is called to create basic records for him to provide him with the functionalities of the application 
@app.route("/new_user_file_write")
def new_user_file_write():
	if request.method == 'GET':
		new_user_name = request.args.get('name', '')
		new_user_username = request.args.get('Username', '')
		new_user_school = request.args.get('school', '')
		new_user_work = request.args.get('work', '')
		new_user_marital_status = request.args.get('marital', '')
		new_user_password = request.args.get('Password', '')
		new_user_confirm_password = request.args.get('CPassword', '')
		if new_user_password == new_user_confirm_password :
			fh_master_user_file = open("master_user_file.txt", 'a')
			fh_user_index = open("users_index_file.txt", "a")
			reference_address = fh_master_user_file.tell()
			fh_master_user_file.write(new_user_username+'|'+new_user_password+'|'+new_user_username+".txt"+'$')
			fh_users_profile_file = open(new_user_username+".txt", 'a')
			fh_post_primary_index = open(new_user_username+"_post_primary_index_file"+".txt", "w")
			fh_post_secondary_index = open(new_user_username+"_post_secondary_index_file.txt", 'w')
			fh_friends_file = open(new_user_username+"_friends.txt",'w')
			fh_post_file = open(new_user_username+"_post_file.txt",'w')
			login_time = datetime.now()
			login_time = login_time.strftime("%Y/%m/%d")
			fh_users_profile_file.write(new_user_name+'|'+new_user_username+'|'+new_user_school+'|'+new_user_work+'|'+new_user_marital_status+'|'+new_user_password+'|'+new_user_username+"_post_file.txt"+'|'+'0'+'|'+new_user_username+"_post_primary_index_file.txt"+'|'+
				new_user_username+"_post_secondary_index_file.txt"+'|'+login_time+'$')
			get_user_index()
			primary_index_records.append([new_user_username, reference_address])
			primary_index_records.sort()
			save_user_index()
			fh_user_index.close()
			fh_master_user_file.close()
			fh_users_profile_file.close()
			fh_post_primary_index.close()
			fh_post_secondary_index.close()	
			fh_friends_file.close()
			fh_post_file.close()
			return render_template('login.html')
		else :
			return render_template('signup.html')

#after successful login this function is called
@app.route("/homepage")
def homepage():
	global username,last_login_date, friends
	get_friends_list()
	all_posts_to_display = list()
	for element in friends:
		if element[1] == "Confirmed":
			get_friends_post_secondary_index(element[0])
			get_friends_post_primary_index(element[0])
			fh_friends_post_file = open(element[0]+"_post_file.txt",'r')
			content = fh_friends_post_file.read()
			if content == '':
				continue
			a_friends_posts = list()
			a_friends_posts.append(element[0])
			for entry in friends_secondary_index_records:
				if entry[0] >= last_login_date:
					a_days_posts = list()
					a_days_posts.append(entry[0].strftime("%y/%m/%d"))
					for i in range(1,len(entry)-1):
						seek_to_reference_address = int(friends_primary_index_records[binary_search(entry[i], friends_primary_index_records)][1])
						fh_friends_post_file.seek(seek_to_reference_address)
						post_content = fh_friends_post_file.read()
						post_needed = post_content.split('$')
						the_post = post_needed[0].split('|')
						the_post[2] = datetime.strptime(the_post[2], "%H:%M:%S").time()
						a_days_posts.append([the_post[2], the_post[3]])
					a_friends_posts.append(a_days_posts)
			all_posts_to_display.append(a_friends_posts)
	return render_template("profile_page.html", name = name, username=username, all_posts_to_display = all_posts_to_display, a_friends_posts = [], a_days_posts = [], a_post = [])

#add new post funstionality is implemented starting with the below function
@app.route("/addNewPost",endpoint="addNewPost")
def addNewPost():
	global username
	return render_template("addNewPost.html")

#this function is responsible for adding the records(post content) to the file and append to the index files that are in the main memory as well
@app.route("/post_file_write")
def post_file_write():
	global username, post_count
	if request.method == 'GET':
		post_timestamp = datetime.now()
		post_date_string_format = post_timestamp.strftime("%Y/%m/%d")
		post_date = datetime.strptime(post_date_string_format,'%Y/%m/%d')
		post_time_string_format = post_timestamp.strftime("%H:%M:%S")
		fh_master_post_file = open((username+"_post_file"+".txt"), "a")
		post_content = request.args.get('content', '')
		post_id = username+"_post_"+str(post_count)
		reference_address = fh_master_post_file.tell()
		post_count += 1
		fh_master_post_file.write(post_id+'|'+post_date_string_format+'|'+post_time_string_format+'|'+post_content+'$')
		get_post_primary_index()
		get_post_secondary_index()
		primary_index_records.append([post_id, reference_address])
		primary_index_records.sort()
		if_new_day = True
		if_already_exists_then_index_position = 0
		return_value = binary_search(post_date, secondary_index_records)
		if return_value != -1:
			if_new_day = False
			if_already_exists_then_index_position = return_value
		if if_new_day:
			secondary_index_records.append([post_timestamp, post_id, -1])
			secondary_index_records.sort()
		else:
			secondary_index_records[if_already_exists_then_index_position].pop()
			secondary_index_records[if_already_exists_then_index_position].extend([post_id, -1])
		save_post_primary_index()
		save_post_secondary_index()
		fh_master_post_file.close()
	return redirect(url_for('addNewPost'))

#edit user information functionality is implemented below
@app.route("/edit_user_info")
def edit_user_info():
	return render_template("edit_user_info.html", name=name, username=username, school=school, place_of_work=place_of_work, marital_status=marital_status, password=password)

#This function gets new information from the edit_user_info.html page
@app.route("/get_new_info")
def get_new_info():
	global name,username, school, place_of_work,marital_status, password
	temp_password = request.args.get('Password','')
	temp_confirm_password = request.args.get('CPassword','')
	if temp_password != temp_confirm_password:
		return redirect(url_for('edit_user_info'))
	else:
		name = request.args.get('name','')
		username = request.args.get('Username','')
		school = request.args.get('school','')
		place_of_work = request.args.get('work','')
		marital_status = request.args.get('marital','')
		password = temp_password
		return redirect(url_for('homepage'))

#add new friend functionality is implemented below
@app.route("/addNewFriend",endpoint="addNewFriend")
def addNewFriend():
	return render_template("addNewFriend.html", users_list = get_to_friend_names())

@app.route("/add_friend/<add_friend_username>")
def add_friend(add_friend_username):
	global friends,friends_friend_list
	get_friends_list()
	get_friends_friend_list(add_friend_username)
	friends.append([add_friend_username, "Requested"])
	friends_friend_list.append([username, "Requested_you"])
	save_friends_list()
	save_friends_friend_list(add_friend_username)
	return redirect(url_for('addNewFriend'))

#this function gets all the users posts and displays them
@app.route("/view_own_post")
def view_own_post():
	get_post_secondary_index()
	get_post_primary_index()
	all_the_posts = list()
	for secondary_index_record in secondary_index_records:
		all_the_posts.append(make_posts_list(username, secondary_index_record))
	return render_template("view_post.html",all_the_posts = all_the_posts, post_on_a_particular_day = [])

#this function gets all the friend requests 
@app.route("/view_friend_requests")
def view_friend_requests():
	get_friends_list()
	friend_requests = list()
	for element in friends:
		if element[1] == 'Requested_you' :
			friend_requests.append(element[0])
	return render_template("friend_requests.html",friend_requests = friend_requests)

#this function is called a accept/decline button is pressed
@app.route("/request_choice/<requested_username>")
def request_choice(requested_username):
	global friends,friends_friend_list
	user_choice = request.args.get('button','')
	get_friends_friend_list(requested_username)
	print(friends_friend_list)
	if user_choice == 'Accept':
		for requested_user in friends:
			if requested_user[0] == requested_username :
				requested_user[1] = "Confirmed"
			print(friends)
		for requested_user in friends_friend_list:
			if requested_user[0] == username :
				requested_user[1] = "Confirmed"
			print(friends_friend_list)
	else:
		for requested_user in friends:
			if requested_user[0] == requested_username :
				requested_user[1] = "you_declined"
		for requested_user in friends_friend_list:
			if requested_user[0] == username :
				requested_user[1] = "Declined"
	save_friends_list()
	save_friends_friend_list(requested_username)
	return redirect(url_for('view_friend_requests'))

#this below implementation is for a functionality for view friends
@app.route("/view_friends")
def view_friends():
	global friends
	get_friends_list()
	print(friends)
	list_to_display = list()
	for element in friends:
		if element[1] == "Confirmed":
			list_to_display.append(element[0])
	return render_template("view_friends.html", list_to_display = list_to_display)

#updates the user information file with new content if editted
@app.route("/update_user_info")
def update_user_info():
	global last_login_date
	fh_user = open(username+".txt", 'w')
	last_login_date = datetime.now()
	last_login_date_string_format = last_login_date.strftime("%Y/%m/%d")
	fh_user.write(make_file_string([name, username, school, place_of_work, marital_status, password, post_file_name, post_count, post_file_primary_index, post_file_secondary_index, last_login_date_string_format]))
	fh_user.close()
	return redirect(url_for('main'))

if __name__=="__main__":
	app.run(debug=True)