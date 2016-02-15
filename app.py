from __future__ import print_function
import traceback
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

def render_nav_bar(current_page):
    # TODO Make this better
    if current_page == 'home':
        return template_dictionary['nav_bar'].render(home='class="active"', login='',
            contact='')
    elif current_page == 'login':
        return template_dictionary['nav_bar'].render(home='', login='class="active"',
            contact='')
    elif current_page == 'contact':
        return template_dictionary['nav_bar'].render(home='', login='',
            contact='class="active"')
    else:
        raise LookupError('Page lookup was outside expected values ' +
            '[home, main, contact]')

def render_main():
    return template_dictionary['container'].render(
        page_content=tl.render_front_page('user_id', template_dictionary, 
            db_conn), nav_bar=render_nav_bar('home'))

def render_login():
    return template_dictionary['container'].render(
        page_content=tl.render_login(template_dictionary),
        nav_bar=render_nav_bar('login'))

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
        # TODO At some point, generating the response will have to be moved back
        # here so we can use the login lib to keep track of users by id and
        # temporary token.
        return render_main()
    except Exception as e:
        print(str(traceback.format_exc()))
        # TODO Create a better error message than HTTP 500.

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


@app.route("/post", methods=['POST'])
def post():
    print("Caught a post request")
    try:
        new_key = login.verify_logged_in_user('user_id', 'a', db_conn)
        print("Got new key")
        if new_key:
            print("New Key was valid")
            post.post('user_id', 'This is title', 'This is body', db_conn)
            print("Posted post")
            return ('', 201, new_key)
        else:
            # TODO Ask the user to login, then re-attempt to post the message.
            pass
    except e:
        print('Caught exception')
        print(str(traceback.format_exc()))

    print('After try block, returning 404.')
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
        print('Caught exception')
        print(str(traceback.format_exc()))

    print('After try block, returning 404.')
    return ('', 404, ('',))

if __name__ == "__main__":
    # TDOD Use the file dir, not the cwd
    template_dictionary = init.load_templates(os.getcwd() + os.sep +
        'templates')
    css_dictionary = init.load_css(os.getcwd() + os.sep + 'css')
    js_dictionary = init.load_js(os.getcwd() + os.sep + 'js')
    db_conn = init.create_db_conn()
    print("Estimated size of cached objects: " +
        str(get_size_of_dict(template_dictionary) +
            get_size_of_dict(css_dictionary) +
            get_size_of_dict(js_dictionary)) +
        " bytes")
    print("Tom, if you haven't profiled this yet, I'm gonna haunt your ass.")
    app.run()
