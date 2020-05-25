# Online-Quiz
Requirements:
1. Python 3.0+
2. PIP

How To Start The Project:
1. Open The CMD/Terminal in the quizadmin folder 
2. In window write dir adn in lixux/mac write ls in terminal and press enter
-->Verify That You Are inside the run.py folder
3. Install The Virtual Enviorment In Your System By entering the command 
-->pip install virtualenv(In Windows)
-->sudo pip3 install virtualenv(In Linux)
4. After Installing The Virtual enviorment activate the virtual enviorment
5. Install All The Project requirement by entering the command 
--->pip install -r requirements.txt (In Windows)
--->sudo pip3 install -r requirements.txt (In Linux)
6. To Run the server type the command
--->python run.py (in Windows)
--->sudo python3 run.py (in Linux)

Your Project Will get Start
It will Give you the host address 
Copy The Address and paste it into your any faviorate Browser


There are two panels inside the project 
1. Admin
2. User

The default panel will open is the user panel
IF you want to open the admin panel then write the /admin at the end of the address that you copied from the command prompt 
(127.0.0.1:8080/admin)
This Will be the address if you didn't touch run.py after installation.



1. Admin Can Add,Edit,Update and Delete The Questions,Check The result of all the users and filter the result of quiz
2. User Can Give The Quiz according to the levels and check their marks


How To Create An Admin User
1. Run The Command 
---->python createsuperuser.py(In windows)
---->sudo python3 createsuperuser.py (In Linux)
Enter the details asked by the Command Prompt
It will create a new super user.

How to run test cases.
1. Front_end test case
for front end cases we first need to open config.py file of the online Quiz project and then replace quiz.db data with test.sqlite3 and then write the following command
---->python test_front_end.py
2. Back_end test case
To run back end test case run the following command on command prompt
---->python test_back_end.py

