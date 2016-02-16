from jinja2 import Template

import psycopg2

import json
import os

if not 'unicode' in dir(__builtins__):
    def unicode(argument):
        return argument

def add_template_to_dict(template_dir, template_name, template_dict):
    template_dict[template_name] = Template(unicode(open(template_dir + os.sep +
        template_name + '.jinja').read()))

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
    add_template_to_dict(template_directory, 'login', template_dictionary)
    add_template_to_dict(template_directory, 'nav_bar', template_dictionary)
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
    load_raw_file(css_directory, 'custom.css', css_dictionary)
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

def create_db_conn(db_file_location):
    # TODO Create a db_connection
    with open(db_file_location, 'r') as db_file:
        db_dict = json.loads(db_file.read())
        return psycopg2.connect(database=db_dict['database'],
            user=db_dict['user'], password=db_dict.get('password', 'password'),
            host=db_dict.get('host', 'localhost'),
            port=db_dict.get('port', 5432))

    return None