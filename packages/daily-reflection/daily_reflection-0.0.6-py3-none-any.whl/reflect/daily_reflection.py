#!/usr/bin/python3


# https://codeburst.io/building-beautiful-command-line-interfaces-with-python-26c7e1bb54df

from __future__ import print_function, unicode_literals
from PyInquirer import prompt, style_from_dict, Token, Separator, print_json
from examples import custom_style_2
from pprint import pprint
from tinydb import TinyDB, where, Query
from reflect.encrypted_json_storage import EncryptedJSONStorage
from reflect.menus import *
from reflect.actions import *
import sys
import os
import datetime
import uuid # creating unique id's for storage
from pathlib import Path # for finding user's home

VERSION="0.0.6"

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


# get password
clear_screen()
print("Daily Reflection, v%s"%VERSION)
encryption_key = prompt(pwd_questions, style=custom_style_2)["password"]

try:
    from os.path import join as join_path
    db = TinyDB(encryption_key=encryption_key, path=join_path(str(Path.home()),".reflect.db"), storage=EncryptedJSONStorage)
except:
    print("Error loading DB, probably wrong encryption key",sys.exc_info()[0], sys.exc_info()[1])
    sys.exit(0)

def reflection_menu():
    action = "" # action has to be the same as the name of the action TODO refactor
    while True:
        action = prompt(main_menu_questions)["mm_action"]
        clear_screen()
        if action=="Quit": break
        if action=="Change Password":
            change_password(db)
            continue
        if action== "Export":
            export(db)
            continue


        # Time based questions
        time = prompt(time_questions)["time"]
        if time=="Back":
            continue

        if action=="Reflection":
            do_reflection(time, db)
        elif action=="Add Questions":
            add_questions(time, db)
        elif action=="Modify Questions":
            modify_questions(time, db)
        elif action=="Change Question Order":
            change_order(time, db)
        elif action=="Delete Questions":
            delete_questions(time, db)
