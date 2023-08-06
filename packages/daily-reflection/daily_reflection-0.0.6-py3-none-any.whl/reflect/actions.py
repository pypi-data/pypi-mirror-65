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
from os.path import join as join_path


def today():
    return datetime.datetime.now().strftime("%Y%m%d")

def clear_screen():
    os.system('cls')
    os.system('clear')

def get_pos(questions, question_text ):
    for i,q in enumerate(questions):
        if question_text==q["text"]:
            return i

def do_reflection(time, data_base):
    # load questions from database
    Questions = Query()
    questions = get_questions(time, data_base)
    # TODO check for empty questions
    if len(questions)==0:
        clear_screen()
        print("No questions for %s reflection. Add some questions.\n"%time )
        return

    #load answers for today if they are there
    Answers = Query()
    today = datetime.date.today().strftime("%Y%m%d")
    old_answers = data_base.search( (Answers.time == time) & (Answers.date==today) & (Answers.type=="reflection") )
    old_answers = (old_answers[0] if len(old_answers)>0 else {})

    # store answers for today in database
    ref_qs = []
    for i, q in enumerate(questions):
        ref_qs.append({
            'type': 'input',
            'name': q["id"],
            'default':  old_answers[q["id"]] if q["id"] in old_answers else "",#TODO load existing answers
            'message': q["text"].replace("?","") +  "?"
        })

    res = prompt(ref_qs)
    res["time"]=time
    res["type"]="reflection"
    res["date"]=today

    if len(old_answers)==0:
        data_base.insert(res)
    else:
        data_base.update(res, (Answers.time == time) & (Answers.date==today) & (Answers.type=="reflection") )
    print("%s-reflection stored.\n"%time)

def get_questions(time, data_base):
    Questions = Query()
    questions = data_base.search( Questions.time == time)
    if len(questions)==0:
        data_base.insert({'questions':questions, "time":time})
        questions=[]
    else:
        questions=[q for q in questions[0]["questions"] if not q["deleted"]]

    # todo add sort order
    return questions


def add_questions(time, data_base):
    # load existing questions
    action=""
    while True:
        clear_screen()
        # get old questions
        questions=get_questions(time, data_base)
        print("Existing questions:")
        [print("\t"+q["text"]) for q in questions]
        print()

        # get new question
        new_question_text=prompt(add_question_ary(time))["new_question"]
        if len(new_question_text)==0:
            clear_screen()
            print("Empty text, no question added.")
            return


        if not new_question_text[-1]=="?":
            new_question_text=new_question_text+"?"

        for q in questions:
            if new_question_text==q["text"]:
                clear_screen()
                print("Duplicate question '%s' not added."%new_question_text)
                return

        new_question={"text":new_question_text, "id":str(uuid.uuid4()), "deleted":False }
        questions += [ new_question ]
        #store new question
        Questions=Query()
        data_base.update({'questions':questions}, Questions.time == time)
        # prompt if you want to add more questions?

        clear_screen()
        action = prompt(continue_add_question)["action"]
        if action=="Back":
            return

def delete_questions(time, data_base):
    # load existing questions
    action=""
    while True:
        clear_screen()
        # get old questions
        questions=get_questions(time, data_base)
        if (len(questions)==0):
            clear_screen()
            print("No questions for %s stored."%time )
            return
        # get new question

        delete_action=prompt(delete_questions_ary(time, questions))["action"]

        if delete_action == "Abort":
            clear_screen()
            print("Aborted deleting.\n")
            return

        # delete data
        for q in questions:
            if q["text"] == delete_action:
                q["deleted"]=True

        Questions = Query()
        data_base.update({'questions':questions}, Questions.time == time)
        clear_screen()
        print("Question for %s reflection deleted .\n"%time)

        # prompt if you want to add more questions?

        action = prompt(continue_delete_question)["action"]
        if action=="Back":
            return

def change_order(time, data_base):
    # load existing questions
    action=""
    clear_screen()
    while True:

        # get old questions
        questions=get_questions(time, data_base)
        if (len(questions)<=1):
            clear_screen()
            print("No or too few questions for %s reflection stored. Add more reflections to change the order."%time )
            return
        # get new question

        move_from=prompt(move_question_from(questions))["action"]
        if move_from == "Abort":
            clear_screen()
            print("Aborted order change.\n")
            return

        # get new question

        move_to=prompt(move_question_to(questions))["action"]

        if move_to == "Abort":
            clear_screen()
            print("Aborted order change.\n")
            return
        # move question
        from_index = get_pos(questions,move_from)
        to_index = get_pos(questions,move_to)
        questions.insert(to_index, questions.pop(from_index))

        # update in database
        Questions=Query()
        data_base.update({'questions':questions}, Questions.time == time)
        clear_screen()
        print("Question moved.\n")

def change_password(data_base): ##TODO  Move to encrypted file storage
    from os.path import join as join_path
    action=""

    new_encryption_key1 = prompt(new_pwd_questions, style=custom_style_2)["password"]
    new_encryption_key2 = prompt(repeat_new_pwd_questions, style=custom_style_2)["password"]

    if not (new_encryption_key1==new_encryption_key2):
        print("New passwords don't match, aborting.")
        return

    if data_base.storage.change_encryption_key(new_encryption_key1):
        print("Password successfully changed\n")
    else:
        print("Error, password was not changed.\n")

def modify_questions(time, data_base):
    # load existing questions
    action=""
    while True:
        clear_screen()
        # get old questions
        Questions = Query()
        questions = get_questions(time, data_base)
        if (len(questions)==0):
            clear_screen()
            print("No questions for %s reflection stored."%time )
            return

        # get new question
        mod_action=prompt(mod_question(time, questions))["action"]

        if mod_action == "Abort":
            clear_screen()
            print("Aborted modification.\n")
            return

        # modify data
        # get new question
        modified_question_text=prompt(mod_question_to(mod_action))["new_question"]

        if len(modified_question_text)==0:
            clear_screen()
            print("Empty text, question not modified. If you want to delete a question, use the delete menu.")
            return

        if not modified_question_text[-1]=="?":
            modified_question_text=modified_question_text+"?"

        for q in questions:
            if modified_question_text==q["text"]:
                clear_screen()
                print("Duplicate question, question not changed."%new_question_text)
                return

        for q in questions:
            if q["text"]==mod_action:
                q["text"]=modified_question_text

        data_base.update({'questions':questions}, Questions.time == time)
        clear_screen()
        #TODO proper messageb
        print("Question for %s reflection has been updated.\n"%time)

        # prompt if you want to add more questions?
        action = prompt(continue_mod_question)["action"]
        if action=="Back":
            return
"""
    Exports all answers to a text file
"""
def export(data_base):
    outfile = join_path(join_path(str(Path.home()),"exported_reflections_%s.txt"%today()) )
    questions = {}
    questions["Morning"] = get_questions("Morning", data_base)
    questions["Evening"] = get_questions("Evening", data_base)

    # get all answer
    Answers = Query()
    answers = data_base.search( Answers.type=="reflection")
    dates = sorted(set([a['date'] for a in answers] ))

    # create a dictionary [date][time] answers
    answers_by_date = {}
    for a in answers:
        if not a["date"] in answers_by_date:
            answers_by_date[a["date"]]={}
        answers_by_date[a["date"]][a["time"]]=a


    with open(outfile, "w+") as f:
        for d  in dates:
            if not d in answers_by_date:
                continue

            f.write(d[0:4]+"-"+d[4:6]+"-"+d[6:]+"\n")
            f.write("==========\n")

            for t in ["Morning","Evening"]:
                if t in answers_by_date[d]:
                    f.write("\t%s:\n"%(t))
                    for q in questions[t]:
                        if q["id"] in answers_by_date[d][t]:
                            f.write("\t\t")
                            f.write(q["text"]+"\t\t")
                            f.write(answers_by_date[d][t][q["id"]]+"\n")
                    f.write("\n")

            f.write("\n\n")


    print("Your reflections were exported to '%s'\n"%outfile)
    pass
