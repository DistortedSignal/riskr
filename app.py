from jinja2 import Template
from flask import Flask, Response

import sys
import os

def get_size_of_dict(dict_to_size):
    size_in_bytes = sys.getsizeof(dict_to_size)
    for a in dict_to_size.keys():
        size_in_bytes += sys.getsizeof(dict_to_size[a])
    return size_in_bytes

def add_template_to_dict(template_dir, template_name, template_dict):
    template_dict[template_name] = Template(open(template_dir + os.sep +
        template_name + '.jinja').read())

# Engineering tradeoff: I REALLY don't want to read these files from disk every
# time that I need to serve a page, so I'm going to load the files at app
# initialization.
def load_templates(template_directory):
    template_dictionary = {}
    add_template_to_dict(template_directory, 'user', template_dictionary)
    add_template_to_dict(template_directory, 'post', template_dictionary)
    add_template_to_dict(template_directory, 'container', template_dictionary)
    add_template_to_dict(template_directory, 'comment', template_dictionary)
    add_template_to_dict(template_directory, 'comment_box', template_dictionary)
    add_template_to_dict(template_directory, 'main', template_dictionary)
    return template_dictionary

# Yes, this function uses side effects of adding items to a dict to influence
# global state. Sue me
def load_raw_file(file_dir, file_name, file_dict):
    file_dict[file_name] = unicode(open(file_dir + os.sep + file_name).read())

def load_css(css_directory):
    css_dictionary = {}
    # TODO Switch this based on cmd line flag
    load_raw_file(css_directory, 'bootstrap.css', css_dictionary)
    load_raw_file(css_directory, 'bootstrap-responsive.css', css_dictionary)
    return css_dictionary

def load_js(js_directory):
    js_dictionary = {}
    # TODO Switch this based on cmd line flag
    load_raw_file(js_directory, 'bootstrap.js', js_dictionary)
    load_raw_file(js_directory, 'bootstrap-alert.js', js_dictionary)
    load_raw_file(js_directory, 'bootstrap-button.js', js_dictionary)
    load_raw_file(js_directory, 'bootstrap-carousel.js', js_dictionary)
    load_raw_file(js_directory, 'bootstrap-collapse.js', js_dictionary)
    load_raw_file(js_directory, 'bootstrap-dropdown.js', js_dictionary)
    load_raw_file(js_directory, 'bootstrap-modal.js', js_dictionary)
    load_raw_file(js_directory, 'bootstrap-popover.js', js_dictionary)
    load_raw_file(js_directory, 'bootstrap-scrollspy.js', js_dictionary)
    load_raw_file(js_directory, 'bootstrap-tab.js', js_dictionary)
    load_raw_file(js_directory, 'bootstrap-tooltip.js', js_dictionary)
    load_raw_file(js_directory, 'bootstrap-transition.js', js_dictionary)
    load_raw_file(js_directory, 'bootstrap-typeahead.js', js_dictionary)
    load_raw_file(js_directory, 'custom.js', js_dictionary)
    load_raw_file(js_directory, 'ie10-viewport-bug-workaround.js',
        js_dictionary)
    load_raw_file(js_directory, 'jquery.js', js_dictionary)
    return js_dictionary

def get_static_file(content, mime_type):
    resp = Response(content, mimetype=mime_type)
    return resp

def render_main():
    user = {'name': 'Tom Kelley'}
    comment = {'user': user, 'text': 'This is comment text'}
    post = {'user': user, 'title': 'This is post title', 
    'body': 'This is the post body, which can be quite long.', 
    'comments': [comment]}
    context = {'user': user, 'posts': [post]}
    return template_dictionary['container'].render(
        page_content=template_dictionary['main'].render(context=context))

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
    return render_main()

if __name__ == "__main__":
    template_dictionary = load_templates(os.getcwd() + os.sep + 'templates')
    css_dictionary = load_css(os.getcwd() + os.sep + 'css')
    js_dictionary = load_js(os.getcwd() + os.sep + 'js')
    print "Estimated size of cached objects: " + str(
        get_size_of_dict(template_dictionary) + 
        get_size_of_dict(css_dictionary) + get_size_of_dict(js_dictionary)) + \
    " bytes"
    app.run()
