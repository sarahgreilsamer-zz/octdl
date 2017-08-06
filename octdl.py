# Must be at the beginning of the file

from __future__ import print_function

# FOLLOWING CODE TO USE GOOGLE API AND GSPREAD

import gspread
from oauth2client.service_account import ServiceAccountCredentials


# STANDARD FLASK IMPORT

from os import chdir
from os.path import dirname, realpath, expanduser

from flask import Flask, render_template, send_from_directory

# JUSTIN'S SUBITIZE IMPORTS

from collections import namedtuple
from datetime import datetime
from os.path import exists as file_exists, join as join_path

from flask import Flask, render_template, abort, request, send_from_directory, url_for, redirect
from sqlalchemy.sql.expression import asc, desc

from models import create_session
from models import Semester
from models import TimeSlot, Building, Room, Meeting
from models import Core, Department, Course
from models import Person
from models import OfferingMeeting, OfferingCore, OfferingInstructor, Offering
from models import CourseInfo
from subitizelib import filter_study_abroad, filter_by_search
from subitizelib import filter_by_semester, filter_by_department, filter_by_number, filter_by_instructor
from subitizelib import filter_by_units, filter_by_core, filter_by_meeting, filter_by_openness
from subitizelib import sort_offerings

# FOLLOWING CODE TO USE GOOGLE API

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


app = Flask(__name__)

FILE_NAME = "Stories Library"


# data has to be on sheet 1, if not change sheet number
def get_data(file_name):
    # Use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    # Find a workbook by name and open the first sheet
    sheet = client.open(file_name).sheet1
    # Extract and print all of the values
    # List of lists
    table = sheet.get_all_values()
    stories = table[1:]
    # Sort in alphabetical order of title
    stories.sort(key=lambda story: story[0])
    return stories  # list of lists


def get_options(stories_list):  # use list of lists from get_data
    stories_dict = {}
    for each_story in stories_list:
        stories_dict['titles'] = each_story[0]
        stories_dict['books'] = each_story[1]
        stories_dict['origins'] = each_story[2]
    return stories_dict  # return dictionary of stories


#def get_results(options_dict):
    #


@app.route('/')
def view_page():
    stories = get_data(FILE_NAME)  # list of lists
    dropdown_options = get_options(stories)  # dictionary of stories
    parameters = request.args.to_dict()  # user's input
    return render_template('template.html', stories=stories)


class Story:
    def __init__(self, title, origin, book, link2pdf):
        self.title = title
        self.origin = origin
        self.book = book
        self.link2pdf = link2pdf


# CODE NOT TO BE CHANGED #

@app.route('/css/<file>')
def view_css(file):
    return send_from_directory('css', file)

if __name__ == '__main__':
    chdir(dirname(realpath(expanduser(__file__))))
    app.run(debug=True)

