from jinja2 import Template
from flask import Flask, Response

import os

# Engineering tradeoff: I REALLY don't want to read these files from disk every
# time that I need to serve a page, so I'm going to load the files at app
# initialization.
def load_templates(template_directory):
    template_dictionary = {}
    template_dictionary['user'] = Template(open(template_directory + os.sep +
        'user.jinja').read())
    template_dictionary['post'] = Template(open(template_directory + os.sep +
        'post.jinja').read())
    template_dictionary['container'] = Template(open(template_directory +
        os.sep + 'container.jinja').read())
    template_dictionary['comment'] = Template(open(template_directory + os.sep +
        'comment.jinja').read())
    template_dictionary['comment_box'] = Template(open(template_directory + 
        os.sep + 'comment_box.jinja').read())
    return template_dictionary

def load_css(css_directory):
    css_dictionary = {}
    # TODO Switch this based on cmd line flag
    css_dictionary['bootstrap.css'] = unicode(open(css_directory + os.sep +
        'bootstrap.css').read())
    css_dictionary['bootstrap-responsive.css'] = unicode(open(css_directory +
        os.sep + 'bootstrap-responsive.css').read())
    return css_dictionary

def load_js(js_directory):
    js_dictionary = {}
    # TODO Switch this based on cmd line flag
    return js_dictionary

def get_static_file(content, mime_type):
    resp = Response(content, mimetype=mime_type)
    return resp

app = Flask(__name__)

@app.route("/css/<css_file_name>")
def load_css_file(css_file_name):
    return get_static_file(css_dictionary[css_file_name], 'text/css')

@app.route("/js/<js_file_name>")
def load_js_file(js_file_name):
    return get_static_file(js_dictionary[js_file_name], 'text/javascript')

@app.route("/#")
@app.route("/")
def index():
    return template_dictionary['container'].render()

if __name__ == "__main__":
    template_dictionary = load_templates(os.getcwd() + os.sep + 'templates')
    css_dictionary = load_css(os.getcwd() + os.sep + 'css')
    js_dictionary = load_js(os.getcwd() + os.sep + 'js')
    app.run()
