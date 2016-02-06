from flask import Flask

import os

def load_templates(template_directory):
    templates = {}
    templates['user'] = open(template_directory + os.sep +
        'user.jinja').read()
    templates['post'] = open(template_directory + os.sep +
        'post.jinja').read()
    templates['container'] = open(template_directory + os.sep +
        'container.jinja').read()
    templates['comment'] = open(template_directory + os.sep +
        'comment.jinja').read()
    templates['comment_box'] = open(template_directory + os.sep +
        'comment_box.jinja').read()
    return templates

def load_css(css_directory):
    pass

def load_js(js_directory):
    pass

app = Flask(__name__)

@app.route("/#")
@app.route("/")
def get_main():
    return "Hello World!"

@app.route("/css/")

if __name__ == "__main__":
    template_dictionary = load_templates()
    css_dictionary = load_css()
    js_dictionary = load_js()
    app.run()
