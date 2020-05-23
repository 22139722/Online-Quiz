from app.admin.models import User
from app import db
import re
print("Enter The Following Details To Create A Admin")
name = input("Enter The Name Of The Admin")
email_not_created = True
while email_not_created:
    email = input("Enter The Email")
    if User.query.filter(User.email==email).count()>0:
        print("The Email Entered By You Is Incorrect")
    else:
        email_not_created=False

password_not_created = True
while password_not_created:
    password = input("Enter The Password")
    if len(password)>=6:
        password_not_created=False
    else:
        print("Password Should Be Atleast 6 Characters.")

user = User(name=name, email=email, password=password, is_admin=True)
db.session.add(user)
db.session.commit()
print("Admin Created Successfully.")


