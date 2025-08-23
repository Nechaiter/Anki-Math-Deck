import genanki
import os
import json
import re


# python -m PyInstaller --onefile CreateDeck.py

import Courses_list


my_model = genanki.Model(
    1607392319,
    'Simple Model',
    fields=[
        {'name': 'Front'},
        {'name': 'Back'},
    ],
    templates=[
        {
            'name': 'Tarjeta 1',
            'qfmt': '{{Front}}',  # Formato del anverso
            'afmt': '{{Back}}',   # Formato del reverso
        },
    ],
)


back='''<div><div style="text-align: center;"><span style="color: rgb(0, 0, 0);"><b>again: (Fail once) I forgot, wrong answer (memory interference), lucky guess, or partial recall (I consider not enough to be a pass)</b></span></div><div style="text-align: center;"><span style="color: rgb(0, 0, 0);"><b>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; hard: successful but effortful recall</b></span></div><div style="text-align: center;"><span style="color: rgb(0, 0, 0);"><b>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; good: default pass grade</b></span></div><div style="text-align: center; "><span style="color: rgb(0, 0, 0);"><b>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; easy: quick and easy, feeling that the review was not needed, even a waste of time</b></span></div></div>'''

def ask_user_option():
    print("What do you want to do?")
    print("1. Generate deck without removing duplicates (main and secondary)")
    print("2. Remove duplicates only from the main deck")
    print("3. Remove duplicates only from the secondary deck")
    print("4. Remove duplicates from both decks")
    while True:
        opt = input("Choose an option (1-4): ").strip()
        if opt in {"1", "2", "3", "4"}:
            return int(opt)
        print("Invalid option. Please try again.")

option = ask_user_option()



#Courses_list.Other
#Course_list.main

file_name="main_courses.json"
with open(os.getcwd()+"/json_files/"+file_name, 'r',encoding='utf-8') as file:
    main_data = json.load(file)

file_name="side_courses.json"
with open(os.getcwd()+"/json_files/"+file_name, 'r',encoding='utf-8') as file:
    side_data = json.load(file)

main_courses = main_data["courses"]
side_courses = side_data["courses"]



import FilteringFunctions



if option == 2:
    main_courses = FilteringFunctions.filter_duplicates(main_courses)
elif option == 3:
    side_courses = FilteringFunctions.filter_duplicates(side_courses)
    
elif option == 4:
    # Main way to filter
    main_courses, side_courses = FilteringFunctions.filter_duplicates_both(main_courses, side_courses)
    # For testing purposes
    # from testing import saveduplicates
    # main_courses, side_courses = saveduplicates.filter_duplicates_both(main_courses, side_courses)

# Export filtered main_courses and side_courses if they were filtered
if option in [2, 4]:
    with open(os.getcwd() + "/json_files/main_courses_filtered.json", "w", encoding="utf-8") as f:
        json.dump({"courses": main_courses}, f, ensure_ascii=False, indent=2)

if option in [3, 4]:
    with open(os.getcwd() + "/json_files/side_courses_filtered.json", "w", encoding="utf-8") as f:
        json.dump({"courses": side_courses}, f, ensure_ascii=False, indent=2)







all_decks = []


# Generate the main deck
course_counter = 1
for course in main_courses:
    course_name = f"{str(course_counter).zfill(2)} {course['courseName']}"
    course_counter += 1
    for unit in course["units"]:
        unit_name = unit["unitName"]
        unit_name=re.sub(r'^(Unit )(\d)(:)', r'\g<1>0\g<2>\g<3>', unit_name)
        deck_name = f"Mathematics::{course_name}::{unit_name}"
        deck_id = abs(hash(deck_name)) % (10 ** 10)
        deck = genanki.Deck(deck_id, deck_name)
        try:
            for exercise in unit["exercises"]:
                front=f'<div style="text-align: center;"><h1><a href="{exercise['link']}">{exercise['exerciseName']}</a></h1></div>'
                note = genanki.Note(model=my_model, fields=[front, back])
                deck.add_note(note)
        except Exception as e:
            print(f"Error adding unit {unit["unitName"]}")
            continue
        all_decks.append(deck)

# Generate the side deck
for idx, course in enumerate(side_courses):
    letter = chr(ord('A') + idx)
    course_name = f"{letter}: {course['courseName']}"
    for unit in course["units"]:
        unit_name = unit["unitName"]
        unit_name=re.sub(r'^(Unit )(\d)(:)', r'\g<1>0\g<2>\g<3>', unit_name)
        deck_name = f"Mathematics::{course_name}::{unit_name}"
        deck_id = abs(hash(deck_name)) % (10 ** 10)
        deck = genanki.Deck(deck_id, deck_name)
        try:
            for exercise in unit["exercises"]:
                front=f'<div style="text-align: center;"><h1><a href="{exercise['link']}">{exercise['exerciseName']}</a></h1></div>'
                note = genanki.Note(model=my_model, fields=[front, back])
                deck.add_note(note)
        except Exception as e:
            print(f"Error adding unit {unit["unitName"]}")
            continue
        all_decks.append(deck)


option_names = {
    1: "raw",
    2: "main_no_duplicates",
    3: "side_no_duplicates",
    4: "both_no_duplicates"
}

file_name = f"Mathematics_{option_names[option]}"
export_path = os.getcwd()+"/decks"+'/'+file_name+'.apkg'
genanki.Package(all_decks).write_to_file(export_path)

