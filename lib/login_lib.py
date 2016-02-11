import bcrypt

def create_new_user(user_name, password, email_address):
    salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(password, salt)
    # TODO Make actual database call that stores user name, salt, pw hash,
    # and email address

    return login_attempt(email_address, password)

def login_attempt(email_address, password):
    # TODO Database code to lookup user by email address, get id, salt, pw hash
    if bcrypt.hashpw(password, salt) == pw_hash:
        # TODO Generate a temporary token and embed it in the return value
        return user_id
    return False

def verify_logged_in_user(email_address, token):
    # TODO Get user id and token from database based on email address
    if token == stored_token: # TODO and $now < token_expire_date
        # TODO Generate a new temporary token and embed it in the return value
        return user_id

