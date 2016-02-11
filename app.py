from __future__ import print_function
from flask import Flask, Response

import sys
import os

# This is some bullshit.
sys.path.append(os.sep.join(__file__.split(os.sep)[:-1]) + os.sep +
    os.sep.join(['venv', 'lib']))
sys.path.append(os.sep.join(__file__.split(os.sep)[:-1]) + os.sep +
    os.sep.join(['venv', 'lib', 'plat-win']))
sys.path.append(os.sep.join(__file__.split(os.sep)[:-1]) + os.sep +
    os.sep.join(['venv', 'lib', 'lib-tk']))
sys.path.append(os.sep.join(__file__.split(os.sep)[:-1]) + os.sep + 'venv')
sys.path.append(os.sep.join(__file__.split(os.sep)[:-1]) + os.sep +
    os.sep.join(['venv', 'lib', 'site-packages']))

import lib.template_lib as tl
import lib.login_lib as login
import lib.init_lib as init

def get_size_of_dict(dict_to_size):
    size_in_bytes = sys.getsizeof(dict_to_size)
    for a in dict_to_size.keys():
        size_in_bytes += sys.getsizeof(dict_to_size[a])
    return size_in_bytes

def render_main():
    return template_dictionary['container'].render(
        page_content=tl.render_front_page(1, template_dictionary))

app = Flask(__name__)

@app.route("/css/<css_file_name>")
def load_css_file(css_file_name):
    return Response(css_dictionary[css_file_name], mimetype='text/css')

@app.route("/js/<js_file_name>")
def load_js_file(js_file_name):
    return Response(js_dictionary[js_file_name], mimetype='text/javascript')

@app.route("/#")
@app.route("/")
def index():
    return render_main()

if __name__ == "__main__":
    # TDOD Use the file dir, not the cwd
    template_dictionary = init.load_templates(os.getcwd() + os.sep +
        'templates')
    css_dictionary = init.load_css(os.getcwd() + os.sep + 'css')
    js_dictionary = init.load_js(os.getcwd() + os.sep + 'js')
    print("Estimated size of cached objects: " +
        str(get_size_of_dict(template_dictionary) +
            get_size_of_dict(css_dictionary) +
            get_size_of_dict(js_dictionary)) +
        " bytes")
    app.run()
