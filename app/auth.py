from app.admin import models
import app.signals as signals


# Function to write authentication

# this function will return None If No Associate user found with the provided Credentials
def authenticate(email=None,password=None):
    if email == None or password ==None:
        raise Exception("Username and Password are not provided")
    else:
        user = models.User.query.filter_by(email=email,
                                            password=signals.generate_password(password)).first()
        if user is None:
            return None
        else:
            return user



