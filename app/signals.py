import hashlib
import uuid



# This Function is Used To Encrypt The password
def generate_password(password):
    password_ = hashlib.md5(password.encode())
    return password_.hexdigest()


# this function is use to CSRF token
def csrf_token():
    return uuid.uuid4()


# This Function is Used To Match the Encrypted Passwords.
def match_password(string, hashed):
    password = hashlib.md5(string.encode())
    if password == hashed:
        return True
    else:
        return False


if __name__ == "__main__":
    s = csrf_token()
    print(s)
