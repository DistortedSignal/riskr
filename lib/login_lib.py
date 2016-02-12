import bcrypt

def create_new_user(user_name, email_address, password, db_conn):
    salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(password, salt)
    # TODO Figure out how to id (either auto-generate or other)
    cursor = db_conn.cursor()
    cursor.execute("INSERT INTO user " +
        "(display_name, email_address, password_hash, salt) VALUES" +
        "(%s,           %s,            %s,            %s)",
        ( user_name,    email_address, pw_hash,       salt))
    db_conn.commit()
    cursor.close()

    return attempt_login(email_address, password, db_conn)

def attempt_login(email_address, password, db_conn):
    # TODO Database code to lookup user by email address, get id, salt, pw hash
    cursor = db_conn.cursor()
    cursor.execute("SELECT id, password_hash, salt FROM user WHERE " +
        "email_address = %s", (email_address))
    row_tuples = cursor.fetchall()

    if row_tuples == []:
        # There were no users in the db with that email address
        return False

    if bcrypt.hashpw(password, salt) == pw_hash:
        # TODO Generate a temporary token and embed it in the return value
        return user_id
    return False

def verify_logged_in_user(email_address, token):
    # TODO Get user id and token from database based on email address
    if token == stored_token: # TODO and $now < token_expire_date
        # TODO Generate a new temporary token and embed it in the return value
        return user_id

