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

from flask import Flask, render_template, request, send_from_directory

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
    stories_list = []
    stories_title = []
    stories_book = []
    stories_origin = []
    stories_link2pdf = []
    for each_story in stories_list:
        stories_title.append(each_story[0])
        stories_book.append(each_story[1])
        stories_origin.append(each_story[2])
        stories_link2pdf.append(each_story[3])
    stories_list.append(stories_title)
    stories_list.append(stories_book)
    stories_list.append(stories_origin)
    stories_list.append(stories_link2pdf)
    return stories_list  # return list of stories characteristics


def get_userinput():
    user_input = request.args.to_dict()  # output one string
    user_inputlist = []
    user_inputlist.append(user_input['title'])
    user_inputlist.append(user_input['origin'])
    user_inputlist.append(user_input['book'])
    return user_inputlist


def get_results(stories_list, user_inputlist):
    query_result = []
    for each_story in stories_list:
        if (str.split(str.lower(user_inputlist[0])) in str.lower(each_story[0]) or str.split(str.lower(user_inputlist[0])) == '') and (str.split(str.lower(user_inputlist[1])) in str.lower(each_story[1]) or str.split(str.lower(user_inputlist[1])) == '') and (str.split(str.lower(user_inputlist[2])) in str.lower(each_story[2]) or str.split(str.lower(user_inputlist[2])) == ''):
            query_result.append(each_story)
    return query_result  # should be a list of lists where list is a story that fits the criteria


@app.route('/')
def view_page():
    stories = get_data(FILE_NAME)  # list of lists [[story 1],[story 2],...]
    stories_list = get_options(stories)  # all options, list of lists [[all titles],[all books],...]
    user_input = get_userinput()  # user's input in a list [title, book, origin]
    query_results = get_results(stories_list, user_input)  #results of the query
    return render_template('template.html', stories=stories, query_results=query_results)


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
    stories = get_data(FILE_NAME)  # list of lists [[story 1],[story 2],...]
    stories_list = get_options(stories)  # all options, list of lists [[all titles],[all books],...]
    user_input = get_userinput()  # user's input in a list [title, book, origin]
    results = get_results(stories_list, user_input)  #results of the query