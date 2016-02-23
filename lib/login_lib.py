import bcrypt
import os

# TODO Should we pass in connections or cursors? Investigate.
# TODO Figure out how to id (either auto-generate or other)

def create_and_store_tmp_token(user_id, db_conn):
    # Get 32 BYTES (256 BITS) of cryptographically random data to use as a 
    # session key. Since OWASP recommends 64 bits 
    # (https://www.owasp.org/index.php/Session_Management_Cheat_Sheet#Session_ID_Entropy), 
    # this seems fine.
    # NOTE: The amount of data that can be generated here can be changed at any
    # time without affecting the overall algorithm. Please ensure that the 
    # database is changed to accommodate the change before pushing to prod.
    token = str(os.urandom(32).encode('hex'))

    # Store the temporary token and the time the token will expire
    cursor = db_conn.cursor()
    # TODO Figure out how to dates with python, psycopg2, and Postgres
    cursor.execute("UPDATE riskr.user SET token=%(token)s, " + 
        "token_expire_date=%(token_expire_date)s " +
        "WHERE id=%(user_id)s",
        {
            'token': token, 
            'token_expire_date': now, # TODO now + 5 minutes
            'user_id': user_id}
        )
    db_conn.commit()
    cursor.close()

    # Return the temporary token
    return {'user_id': user_id,
        'session_token': create_and_store_tmp_token(user_id, db_conn)}

def create_new_user(user_name, email_address, password, db_conn):
    salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(password, salt)
    cursor = db_conn.cursor()

    # TODO Wrap this in a try/except to ensure that email address is unique.
    # TODO How is id formed?
    cursor.execute("INSERT INTO riskr.user " +
        "(display_name, email_address, password_hash, salt) VALUES" +
        "(%(name)s,     %(email)s,     %(pw_hash)s,   %(salt)s)",
        {
            'name': user_name,
            'email': email_address,
            'pw_hash': pw_hash,
            'salt':salt
        }
    )
    db_conn.commit()
    cursor.close()

    return attempt_login(email_address, password, db_conn)

def attempt_login(email_address, password, db_conn):
    cursor = db_conn.cursor()
    cursor.execute("SELECT id, password_hash, salt FROM riskr.user WHERE " +
        "email_address=%(email)s",
        {'email': email_address})
    row_tuples = cursor.fetchall()
    cursor.close()
    # TODO Lots of stuff here

    if row_tuples == []:
        # There were no users in the db with that email address
        return False

    if bcrypt.hashpw(password, salt) == pw_hash:
        return create_and_store_tmp_token(user_id, db_conn)
    return False

def verify_logged_in_user(user_id, token, db_conn):
    cursor = db_conn.cursor()
    cursor.execute("SELECT token, token_expire_date FROM riskr.user " +
        "WHERE id=%(user_id)s",
        {'user_id': user_id})
    results = db_conn.fetchall()
    cursor.close()

    if token == stored_token: # TODO and $now < token_expire_date
        return create_and_store_tmp_token(user_id, db_conn)
    return False
