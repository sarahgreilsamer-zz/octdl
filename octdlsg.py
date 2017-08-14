# Must be at the beginning of the file

from __future__ import print_function

# FOLLOWING CODE TO USE GOOGLE API AND GSPREAD

import gspread
from oauth2client.service_account import ServiceAccountCredentials


# FLASK IMPORT

from os import chdir
from os.path import dirname, realpath, expanduser
from flask import Flask, render_template, request, send_from_directory


app = Flask(__name__)


FILE_NAME1 = "Stories Library"  # Workbook where story data was checked by Adam and Tristan
FILE_NAME2 = "Added Stories"  # Workbook where story data added by members of OCT through Google form


# This function grabs data from Google Sheets using the Sheets API
def get_data(file_name1, file_name2):
    # Use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    # Find a workbook by name and open the first sheet
    sheet1 = client.open(file_name1).sheet1  # Original story file verified by Adam and Tristan
    sheet2 = client.open(file_name2).sheet1  # Answers to form
    # Extract and print all of the values
    # List of lists
    table1 = sheet1.get_all_values()
    table2 = sheet2.get_all_values()
    del(table1[0])
    del(table2[0])
    for each_story in table2:
        del(each_story[0])
        del(each_story[0])
    stories=[]
    for each_story in table1:
        stories.append(each_story)
    for each_story in table2:
        stories.append(each_story)
    # Sort by alphabetical order of title
    stories.sort(key=lambda story: story[0])
    return stories  # list of lists


# This function converts user input into lists
def get_userinput(parameters):  # parameters is the result of args to dict
    user_inputlist = []
    user_inputlist.append(parameters['title'])
    user_inputlist.append(parameters['origin'])
    user_inputlist.append(parameters['book'])
    return user_inputlist


# This function gets results given user input and the existing library (Stories Library + Added Stories)
def get_results(stories_list, user_inputlist):
    query_result = []
    title_keywords = []
    book_keywords = []
    origin_keywords = []
    for each_string in user_inputlist[0].split():
        title_keywords.append(each_string)
    for each_string in user_inputlist[1].split():
        origin_keywords.append(each_string)
    for each_string in user_inputlist[2].split():
        book_keywords.append(each_string)
    if title_keywords != []:
        for each_story in stories_list:  # looking at list of all the stories where each story is a list  # for each key word entered by the user
            title = []
            for each_word in each_story[0].split():
                each_word = each_word.lower()
                title.append(each_word)
            for each_term in title_keywords:  # looking at all the key terms entered by the user
                if each_term in title:
                    query_result.append(each_story)
        stories_list = query_result
    query_result = []
    if origin_keywords != []:
        for each_story in stories_list:  # looking at list of all the stories where each story is a list  # for each key word entered by the user
            origin = []
            for each_word in each_story[1].split():
                each_word = each_word.lower()
                origin.append(each_word)
            for each_term in origin_keywords:  # looking at all the key terms entered by the user
                if each_term in origin:
                    query_result.append(each_story)
        stories_list = query_result
    query_result = []
    if book_keywords != []:
        for each_story in stories_list:  # looking at list of all the stories where each story is a list  # for each key word entered by the user
            book = []
            for each_word in each_story[2].split():
                each_word = each_word.lower()
                book.append(each_word)
            for each_term in book_keywords:  # looking at all the key terms entered by the user
                if each_term in book:
                    query_result.append(each_story)
        stories_list = query_result
    query_result = stories_list
    return query_result  # should be a list of lists where list is a story that fits the criteria


# Creates website page
@app.route('/')
def view_page():
    stories = get_data(FILE_NAME1, FILE_NAME2)  # list of lists [[story 1],[story 2],...]
    parameters = request.args.to_dict()  # args to dict, dictionary where keys name of field, and user input are values of keys
    if len(parameters) == 0:
        parameters['title'] = ''
        parameters['book'] = ''
        parameters['origin'] = ''
        query_results = stories
    else:
        user_input = get_userinput(parameters) # user's input in a list [title, book, origin]
        query_results = get_results(stories, user_input)  # results of the query
    return render_template('template.html', dictionary=str(parameters), query_results=query_results)


# Not currently used but to be used in future developments
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

@app.route('/images/<file>')
def view_images(file):
    return send_from_directory('images', file)

@app.route('/js/<file>')
def view_js(file):
    return send_from_directory('js', file)

if __name__ == '__main__':
    chdir(dirname(realpath(expanduser(__file__))))
    app.run(debug=True)