from flask import Flask

import os

# Engineering tradeoff: I REALLY don't want to read these files from disk every
# time that I need to serve a page, so I'm going to load the files at app
# initialization.
def load_templates(template_directory):
    templates = {}
    templates['user'] = open(template_directory + os.sep + 'user.jinja').read()
    templates['post'] = open(template_directory + os.sep + 'post.jinja').read()
    templates['container'] = open(template_directory + os.sep +
        'container.jinja').read()
    templates['comment'] = open(template_directory + os.sep + 
        'comment.jinja').read()
    templates['comment_box'] = open(template_directory + os.sep +
        'comment_box.jinja').read()
    return templates

def load_css(css_directory):
    css_dictionary = {}
    # TODO Switch this based on cmd line flag
    css_dictionary['bootstrap.css'] = open('css' + os.sep +
        'bootstrap.css').read()
    css_dictionary['bootstrap-reactive.css'] = open('css' + os.sep +
        'bootstrap-reactive.css').read()

def load_js(js_directory):
    pass

app = Flask(__name__)

@app.route("/css/<css_file_name>")
def load_css_file(css_file_name):
    return css_dictionary['css_file_name']

@app.route("/js/<js_file_name>")
def load_js_file(js_file_name):
    return js_dictionary['js_file_name']

@app.route("/#")
@app.route("/")
def get_main():
    return "Hello World!"

if __name__ == "__main__":
    template_dictionary = load_templates()
    css_dictionary = load_css()
    js_dictionary = load_js()
    app.run()
