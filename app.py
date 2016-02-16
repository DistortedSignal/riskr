from __future__ import print_function
import traceback
import time
import sys
import os

# This is some bullshit.
sys.path.append(os.sep.join(__file__.split(os.sep)[:-1]) + os.sep +
    os.sep.join(['venv', 'lib', 'site-packages']))

from flask import Flask, Response

import lib.template_lib as tl
import lib.login_lib as login
import lib.init_lib as init
import lib.post_lib as post

# TODO Write function that gets headers from request since that's where I'm
# going to be putting the user id/token.

def get_size_of_dict(dict_to_size):
    size_in_bytes = sys.getsizeof(dict_to_size)
    for a in dict_to_size.keys():
        size_in_bytes += sys.getsizeof(dict_to_size[a])
    return size_in_bytes

def render_main_no_user():
    return template_dictionary['container'].render(
        page_content=tl.render_front_page_without_user(template_dictionary, 
            db_conn), nav_bar=tl.render_nav_bar('home', template_dictionary))

def render_main_with_user(user_token):
    return template_dictionary['container'].render(
        page_content=tl.render_front_page_with_user(user_token['user_id'], 
            template_dictionary, db_conn), 
        nav_bar=tl.render_nav_bar('home', template_dictionary))

def render_login():
    return template_dictionary['container'].render(
        page_content=tl.render_login(template_dictionary),
        nav_bar=tl.render_nav_bar('login', template_dictionary))

app = Flask(__name__)

@app.route("/css/<css_file_name>")
def load_css_file(css_file_name):
    return Response(css_dictionary[css_file_name], mimetype='text/css')

@app.route("/js/<js_file_name>")
def load_js_file(js_file_name):
    return Response(js_dictionary[js_file_name], mimetype='text/javascript')

@app.route("/")
def index():
    try:
        # new_key = login.verify_logged_in_user(1, 'a', db_conn)
        return render_main_no_user()
    except Exception as e:
        print(str(traceback.format_exc()))
        # TODO Create a better error message than HTTP 500.

# TODO Merge login_page() and attempt_user_login, switch on HTTP method so I can
# have only one method that looks like a login.
@app.route("/login")
def login_page():
    try:
        # new_key = login.verify_logged_in_user('user_id', 'a', db_conn)
        # TODO Whatever this is.
        return render_login()
        if new_key:
            pass
        else:
            return render_login()
    except e:
        print(str(traceback.format_exc()))
        # TODO Create a better error message than HTTP 500.

@app.route("/login_user", methods=['POST'])
def attempt_user_login():
    token = login.attempt_login('user_email', 'password', db_conn)
    if token:
        return render_main_with_user(token)
    else:
        return ('', 403, ('',))

@app.route("/create_user", methods=['POST'])
def create_user():
    if 'password' == 'confirm password':
        token = login.create_new_user('display_name', 'email_address',
            'password', db_conn)
        # TODO Redirect the user to the main form.

@app.route("/post", methods=['POST'])
def post():
    try:
        new_key = login.verify_logged_in_user('user_id', 'a', db_conn)
        if new_key:
            post.post('user_id', 'This is title', 'This is body', db_conn)
            return ('', 201, new_key)
        else:
            # TODO Ask the user to login, then re-attempt to post the message.
            pass
    except e:
        print(str(traceback.format_exc()))

    return ('', 404, ('',))

@app.route("/comment", methods=['POST'])
def comment():
    try:
        new_key = login.verify_logged_in_user('user_id', 'token', db_conn)
        if new_key:
            post.comment('post_id', 'user_id', 'comment_body', db_conn)
            return ('', 201, new_key)
        else:
            # TODO Ask the user to login, then re-attempt to post the message.
            pass
    except e:
        print(str(traceback.format_exc()))

    return ('', 404, ('',))

if __name__ == "__main__":
    file_path = os.sep.join(__file__.split(os.sep)[:-1])
    print(file_path)
    template_dictionary = init.load_templates(file_path + os.sep +
        'templates')
    css_dictionary = init.load_css(file_path + os.sep + 'css')
    js_dictionary = init.load_js(file_path + os.sep + 'js')
    db_conn = init.create_db_conn(file_path + os.sep + 'db.properties')
    print("Estimated size of cached objects: " +
        str(get_size_of_dict(template_dictionary) +
            get_size_of_dict(css_dictionary) +
            get_size_of_dict(js_dictionary)) +
        " bytes")
    print("Tom, if you haven't profiled this yet, I'm gonna haunt your ass.")
    app.run()
