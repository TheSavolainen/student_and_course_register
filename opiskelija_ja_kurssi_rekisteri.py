import os
import time
import json
import sys
from datetime import date

#INTRODUCTION
#This program allows user to save courses, with their course id and names into a dictionary
#and also allows user to add students to a given course, grade the students and see a table
#of the students attending the course and also can see list of the courses saved into the
#program.
#
# NOTES
# 12.12.2023
# -I just realized that it would be computationally less taxing to separate the if conditions
# -In the print_dictionary_data_as_table(name_of_menu,course_key="") and 
# -input_checker(user_input,error_message,course_key="") into their own 
# functions,so there would be less
# computation to be done to check for some input or data printing needs, but its
# -Easier for now atleast for the programmer to build the program, cause there isn't 
# -ten different functions for checking user input that need to be called. 
# -Now only need to add new if condition into one function, if 
# new user input scenarios OR dictionary data printing situations arise
# -Maybe in future projects split those functions into smaller functions and put them into
# -their own file, i don't really know at this point yet. 
#
#
#
#
#DATA STRUCTURES OF courses & students_dict_n dictionaries 

#courses = {
#    course_id_0 : [course_name_0, grading_system_0, students_dict_0]
#    course_id_1 : [course_name_1, grading_system_1, students_dict_1]
#    .
#    .
#    .
#    course_id_n : [course_name_n, grading_system_n, students_dict_n]
#}


#This is inside the courses dictionary,(this here only for visualization)
#This actually exists in the courses[course_key][2]
#students_dict_n = {
#    student_id_0 : [first_name_0, last_name_0, grade_0, grade_evaluation_date_0]
#    student_id_1 : [first_name_1, last_name_1, grade_1, grade_evaluation_date_1]
#    .
#    .
#    .
#    student_id_n : [first_name_n, last_name_n, grade_n, grade_evaluation_date_n]
#}

#This is the main data storage during program runtime.
courses = {}

def clear_ui():
    """
    This clears the user interface terminal, does not take any arguments.
    """
#This function is the reason why os module was imported, so that the terminal window can 
#be cleaned of the "UI garbage" that accumulates over time of usage
    os.system('cls' if os.name == 'nt' else 'clear') 


def print_dictionary_data_as_table(name_of_menu,course_key=""):
    """
    Prints dictionary data in table format and when calling this function, one should 
    specify the name of the menu here as condition and in the spesific function call as an argument.
    course_key= is optional and is used in course_menu sub-functions
    """

    if name_of_menu == "courses_table_menu":
        print(f'{"ID":15} {"COURSE":31}{"GRADING":23}{"NUMBER OF STUDENTS":10}')

        for course_id,courses_list in courses.items():
            if courses_list[1] == "Numerical(0-5)":
                print(f'{course_id:15} {courses_list[0]:30}' 
                      f'{courses_list[1]:10}{len(courses_list[2]):10}')
            elif courses_list[1] == "Pass/Fail":
                print(f'{course_id:15} {courses_list[0]:30}{courses_list[1]:14}'
                      f'{len(courses_list[2]):10}')

    elif name_of_menu == "search_defined_courses":
        print(f'{"ID":15} {"COURSE":31}')
        for course_id,courses_list in courses.items():
            print(f'{course_id:15} {courses_list[0]:30}')

    elif name_of_menu == "grading_menu":
        list_of_first_letters = lastnames_first_letter_shorter(courses,course_key)

        print(f'{"ID":15} {"NAME":30}')

        for character in list_of_first_letters:
            for student_id,students_data in courses[course_key][2].items():
                if character == students_data[1][0] and len(students_data) == 2:
                    students_name_as_list = [students_data[0],students_data[1]]
                    student_name = " ".join(students_name_as_list)
                    print(f'{str(student_id):15} {student_name:31}')
    
    elif name_of_menu == "all_students_list_of_course_students":
        list_of_first_letters = lastnames_first_letter_shorter(courses,course_key)

        print(f'{"ID":15} {"NAME":30} {"GRADE":15} {"EVALUATION DATE":15}')        
        for character in list_of_first_letters:
            for student_id, students_data in courses[course_key][2].items():
                if character == students_data[1][0] and len(students_data) == 2:
                    students_name_as_list = [students_data[0],students_data[1]]
                    student_name = " ".join(students_name_as_list)
                    print(f'{str(student_id):15} {student_name:30}')
                elif character == students_data[1][0] and len(students_data) > 2:
                    students_name_as_list = [students_data[0],students_data[1]]
                    student_name = " ".join(students_name_as_list)
                    print(f'{str(student_id):15} {student_name:30}' 
                          f' {str(students_data[2]):15} {students_data[3]:15}')

    elif name_of_menu == "non_graded_students_list_of_course_students":
        list_of_first_letters = lastnames_first_letter_shorter(courses,course_key)

        print(f'{"ID":15} {"NAME":30} {"GRADE":15} {"EVALUATION DATE":15}')
        for character in list_of_first_letters:
            for student_id,students_data in courses[course_key][2].items():
                if character == students_data[1][0] and len(students_data) == 2:
                    students_name_as_list = [students_data[0],students_data[1]]
                    student_name = " ".join(students_name_as_list)
                    print(f'{str(student_id):15} {student_name:31}')

    elif name_of_menu == "graded_students_list_of_course_students":
        list_of_first_letters = lastnames_first_letter_shorter(courses,course_key)

        print(f'{"ID":15} {"NAME":30} {"GRADE":15} {"EVALUATION DATE":15}')        
        for character in list_of_first_letters:
            for student_id, students_data in courses[course_key][2].items():
                if character == students_data[1][0] and len(students_data) > 2:
                    students_name_as_list = [students_data[0],students_data[1]]
                    student_name = " ".join(students_name_as_list)
                    print(f'{str(student_id):15} {student_name:30}' 
                          f' {str(students_data[2]):15} {students_data[3]:15}')


def lastnames_first_letter_shorter(dict,course_key):
    """
    Saves the lastnames of all students and creates 
    a list that contains only the first character of every students
    lastname. Removes duplicates via converting list to set and back
    to list.
    """
    lastnames_first_letter = [] 
    for data_about_student in dict[course_key][2].values():
        lastnames_first_letter.append(data_about_student[1][0])
    lastnames_first_letter = list(set(lastnames_first_letter))
    lastnames_first_letter.sort()

    return lastnames_first_letter





def json_data_file_reader():
    """
    Opens a file and moves data to a variable from that file
    and that variable is the return
    """
    with open("course_and_student_data.json", "r") as openfile:
        course_and_student_data_dict = json.load(openfile)
        return course_and_student_data_dict


def json_data_file_writer(course_and_student_data_dict):
    with open("course_and_student_data.json", "w") as outfile:
        json.dump(course_and_student_data_dict, outfile)
        
        
def save_and_quite_menu():
    """
    calls function that moves data to json file and 
    closes the program
    """
    json_data_file_writer(courses)
    print("Session data was saved into 'course_and_student_data.json'")
    time.sleep(2)
    print("Program is closing now.")
    time.sleep(2)
    sys.exit()


def list_of_courses_menu():
    """
    This is the menu for COURSE REGISTRY 
    """

    clear_ui()
    print("COURSE REGISTRY \n\n" 
        "Here you can see all the courses that are\n"
        "currently in the registry.\n")
    print_dictionary_data_as_table("courses_table_menu")

    print("\na) Main menu")
    user_input = input_checker(": ", "Only 'a' is valid input!")
    if user_input == 'a':
        main_menu()


def input_checker(user_input,error_message,course_key=""):
    """
    Checks that user did correct input, usefull in many
    situations where user input is to be expected.
    """

    if error_message == "Only 'a' and 'b' are valid inputs!":
        while True:
            input_test = input(user_input)
            if input_test == 'a' or input_test == 'b':
                return input_test
            else:
                print("\n",error_message)

    elif error_message == "Only 'a' 'b' and 'c' are valid inputs!":
        while True:
            input_test = input(user_input)
            if input_test == 'a' or input_test == 'b' or input_test == 'c':
                return input_test
            else:
                print("\n",error_message)

    elif error_message == "Only 'a' is valid input!":
        while True:
            input_test = input(user_input)
            if input_test == 'a':
                return input_test
            else:
                print("\n",error_message)

    elif error_message == "Given course_id does not exist. Try again":
        while True:
            input_test = input(user_input)
            is_correct_course_id = False

            for course_id in courses.keys():
                if input_test == course_id:
                    is_correct_course_id = True
            if is_correct_course_id:
                return input_test
            else:
                print("\n",error_message)
    
    elif error_message == "Only 'a' 'b' 'c' and 'd' are valid inputs!":
        while True:
            input_test = input(user_input)
            if input_test == 'a' or input_test == 'b' or input_test == 'c' or input_test == 'd':
                return input_test
            else:
                print("\n",error_message)    

    elif error_message == "Student id can only contain numbers!":
        while True:
            try:
                number_test = int(input(user_input))
            except ValueError:
                print(error_message)
            else:
                return number_test
            
    elif error_message == "Name can only contain letters!":
        while True:
            input_test = input(user_input)
            input_test = input_test.lstrip()
            input_test = input_test.rstrip()
            contains_number = False
            for element in input_test:
                if element.isnumeric():
                    contains_number = True
                    continue
            if contains_number:
                print("\n",error_message)
                continue

            try:
                if input_test[input_test.index(" ") + 1].isalpha() and input_test.count(" ") == 1:
                    input_test = input_test.title()
                    return input_test
            except ValueError:
                print("You had a typo! make sure you put firstname & lastname separated by space.")
                continue
            else:
                print("You had a typo! make sure you put firstname & lastname separated by space.")


    elif error_message == "Incorrect student id!": 
        while True:
            try:
                input_test = int(input(user_input))
            except ValueError:
                print(error_message)
                continue
            else:
                for student_id in courses[course_key][2].keys():
                    if input_test == student_id:
                        return input_test
                print("\n",error_message)

    elif error_message == "The grade must be a number between 0-5!": 
        while True:
            try:
                input_test = int(input(user_input))
            except ValueError:
                print("\n",error_message)
            else:
                if input_test <= 5 and input_test >= 0:
                    return input_test
                else:
                    print("\n",error_message)

    elif error_message == "Evaluation date must be in correct form!":
        while True:
            input_test = input(user_input)
            input_test.rstrip()
            input_test.lstrip()
            if input_test.count(" ") > 0:
                input_test = input_test.replace(" ", "")

            date_month_year = input_test.split(".") 
            #This list expects that the date was given as "dd.mm.yy" and then gives out
            # a list that is [date,month,year]

            #This if structure checks that given date is of a correct form and 
            #that there are no nonsensical data
            if not input_test.count(".") == 2:
                print("\n",error_message)
                continue

            elif int(date_month_year[0]) > 31 or int(date_month_year[0]) < 1:
                print("given day cannot exist!")
                continue
            elif int(date_month_year[1]) > 12 or int(date_month_year[1]) < 1:
                print("Given month cannot exist!")
                continue

            elif int(date_month_year[2]) > date.today().year:
                print("given year cannot exists!")
                continue

            if int(date_month_year[0]) < 10 and len(date_month_year[0]) == 1: 
                date_month_year[0] = date_month_year[0].zfill(2)

            if int(date_month_year[1]) < 10 and len(date_month_year[1]) == 1:
                date_month_year[1] = date_month_year[1].zfill(2)

            input_test = ".".join(date_month_year)
            return input_test
        
    elif error_message == "Course_id must be atleast 7 alphanumerics long & contain one or more letters!":
        while True:
            input_test = input(user_input)
            input_test = input_test.replace(" ","")
            for symbol in input_test:
                if symbol.isalpha() and len(input_test) >= 7:
                    return input_test
            print("\n",error_message)


def course_selection_menu():
    """
    This is used for selecting the correct course.
    """
    clear_ui()
    print("COURSE SELECTION MENU\n\n")

    if len(courses) == 0:
        print("There are no courses that could be selected, yet!\nSending back to main menu.")
        time.sleep(4)
        main_menu()

    print("Look for the correct course from the\n table below and type it's course id.\n")
    print_dictionary_data_as_table("search_defined_courses")

    print("\nCourse id")
    selected_course_id = input_checker(": ","Given course_id does not exist. Try again")

    print(f'\nSuccesfully selected {selected_course_id} {courses[selected_course_id][0]}')
    time.sleep(2)

    course_menu(selected_course_id)


def define_course_menu():
    """
    This function creates a menu where user 
    can define a new course 
    """
    clear_ui()
    print("STUDENT REGISTRY COURSE DEFINER\n\n"
          "To define a course, you must first\n"
          "input the course identification\n"
          "number,second you must input the\n" 
          "name of the course, and third\nthing" 
          "to do is to choose the type of \ngrading " 
          "used in the course")

    print("\nType the course_id")
    course_id = input_checker(": ","Course_id must be atleast 7 alphanumerics long & contain one or more letters!")
    print("\nType the name of the course.")
    course_name = input(": ")
    #Here i did not see a reason to check user input, because something like course name can 
    #be practically anything, in terms of computing.

    print("\nWhat type of grading is used in the course?\n"
          "a) Numerical(0-5)\n"
          "b) Pass/Fail")
    
    grading_type = input_checker(": ","Only 'a' and 'b' are valid inputs!")

    if grading_type.lower() == "a":
        grading_type = "Numerical(0-5)"
    elif grading_type.lower() == "b":
        grading_type = "Pass/Fail"

    clear_ui()

    print("\nDo you want to save the course\n"
          "With the following information?\n\n"
          f'{course_id.upper()}, {course_name.capitalize()}, {grading_type} grading\n\n'
          "a) yes\nb) no")
    
    save_course = input_checker(": ","Only 'a' and 'b' are valid inputs!")

    course_id.upper()
    course_name.capitalize()

    if save_course == 'a':
        courses[course_id] = [course_name, grading_type, {}]
        print("Data was saved succesfully")
        time.sleep(1)
        main_menu()

    elif save_course == 'b':
        print("Data was not saved")
        time.sleep(1)
        main_menu()


def add_student_to_course_menu(course_key):
    """
    This Saves users input of the students Name and student_id 
    into courses[course_key][2][n,n+1] n=0
    """

    clear_ui()
    print(f'Add student to, {course_key} {courses[course_key][0]}\n'
          'Enter the student id')
    student_id = input_checker(": ","Student id can only contain numbers!")

    print("\n Student name(Firstname & lastname separated by space)")
    student_name = input_checker(": ","Name can only contain letters!")

    clear_ui()
    print("Do you want  to add the student to the" 
          f'course with the following info?\n{student_id}, {student_name}\n'
          'a) yes\nb) no')
    save_choice = input_checker(": ","Only 'a' and 'b' are valid inputs!")

    if save_choice == 'a':
        courses[course_key][2][student_id] = student_name.split(" ")
        print("Data was saved succesfully!")
        time.sleep(1)
        clear_ui()
        print("What next?\n"
          f'\na) Add another student\nb) Give grade to {student_name}\n'
            'c) Back to course menu')

        user_input = input_checker(": ", "Only 'a' 'b' and 'c' are valid inputs!")
        if user_input == "a":
            add_student_to_course_menu(course_key)
        elif user_input == "b":
            grade_student(course_key, student_id)
            course_menu(course_key)
        elif user_input == "c":
            course_menu(course_key)

    elif save_choice == 'b': 
        del student_id
        del student_name
        print("Data was not saved.")
        time.sleep(1)
        clear_ui()
        print(f'What next?\n'
          f'\na) Add a student\n'
            'b)Back to course menu')        
        user_input = input_checker(": ","Only 'a' and 'b' are valid inputs!")
        
        if user_input == "a":
            add_student_to_course_menu(course_key)

        elif user_input == "b":
            course_menu(course_key) 


def count_not_graded_students(course_key):
    """
    Counts the amount of non graded students in 
    the courses[course_key][2] aka students_dict of the given course
    """
    amount_not_graded_students = 0
    for students_data in courses[course_key][2].values():
        if len(students_data) < 3:
            amount_not_graded_students += 1
    return amount_not_graded_students


def  student_grading_menu(course_key):
    """
    This function creates a menu where user can 
    grade students and also prints a table of non-graded
    students for convinience
    """ 
    clear_ui()

    print("\nSTUDENT GRADING MENU")    
    if len(courses[course_key][2]) == 0:
        print("\nThis course does not have any students that" 
              "you can grade, yet!\nSending back to course menu.")
        time.sleep(4)
        course_menu(course_key)
    elif count_not_graded_students(course_key) == 0:
        print("All the students in this course have being graded!\nSending back to course menu.")
        time.sleep(4)
        course_menu(course_key)


    print("Students that have not yet being graded")
    print_dictionary_data_as_table("grading_menu",course_key)

    print("\ntype the student's id that you want to grade")
    student_id = input_checker(": ", "Incorrect student id!",course_key)
    grade_student(course_key, student_id)
    clear_ui()
    print("Do you want to. \na) Grade another student.\nb) Go back to course menu.")
    user_action = input_checker(": ", "Only 'a' and 'b' are valid inputs!")
	
    if user_action == "a":
        student_grading_menu(course_key)
    elif user_action == "b":
        course_menu(course_key)


def grade_student(course_key, student_id):
    clear_ui()
    if courses[course_key][1] == "Numerical(0-5)":
        print(f'Courses grading type is {courses[course_key][1]}')
        print(f'What grade will be given to {courses[course_key][2][student_id][0]}' 
            f' {courses[course_key][2][student_id][1]}\nfor the {courses[course_key][0]} course?')
        grade = input_checker(": ", "The grade must be a number between 0-5!")
        courses[course_key][2][student_id].append(grade)

    elif courses[course_key][1] == "Pass/Fail":
        print(f'Courses grading type is {courses[course_key][1]}')
        print(f'Did {courses[course_key][2][student_id][0]} {courses[course_key][2][student_id][1]} Pass or fail\nthe {courses[course_key][0]} course?')
        print(f'a) Pass\nb) Fail')
        grade = input_checker(": ", "Only 'a' and 'b' are valid inputs!")
        if grade == 'a':
            courses[course_key][2][student_id].append("Pass")
        elif grade == 'b':
            courses[course_key][2][student_id].append("Fail")

    print(f'When was {courses[course_key][2][student_id][0]} {courses[course_key][2][student_id][1]} graded? Give in the format of "dd.mm.yy" ex -> "18.12.2023"')
    eval_date = input_checker(": ", "Evaluation date must be in correct form!")
    courses[course_key][2][student_id].append(eval_date)

    print("data was succesfully saved!")
    time.sleep(1)


def  list_of_course_students_menu(course_key,viewing_mode="all"):
    if viewing_mode == "all":
        clear_ui()
        print(f'\nLIST OF STUDENTS, {course_key} {courses[course_key][0]}')
        print(f'\nHere you can see all the registered students of {courses[course_key][0]} course.'
              '\n\nALL STUDENTS\n')
        print_dictionary_data_as_table("all_students_list_of_course_students",course_key)

        print("\na) Show only non-graded\nb) Show only graded \nc) Back to course menu")
        user_input = input_checker(": ","Only 'a' 'b' and 'c' are valid inputs!")
        if user_input == 'a':
            list_of_course_students_menu(course_key,"non-graded")
        elif user_input == 'b':
            list_of_course_students_menu(course_key,"graded")
        elif user_input == 'c':
            course_menu(course_key)


    elif viewing_mode == "non-graded":
        clear_ui()
        print(f'\nLIST OF STUDENTS, {course_key} {courses[course_key][0]}')
        print(f'\nHere you can see all the students of {courses[course_key][0]} course \nthat have not being graded yet.'
              '\n\nNON-GRADED STUDENTS\n')
        print_dictionary_data_as_table("non_graded_students_list_of_course_students",course_key)

        print("\na) Show all students\nb) Show only graded students \nc) Back to course menu")
        user_input = input_checker(": ","Only 'a' 'b' and 'c' are valid inputs!")
        if user_input == 'a':
            list_of_course_students_menu(course_key,"all")
        elif user_input == 'b':
            list_of_course_students_menu(course_key,"graded")
        elif user_input == 'c':
            course_menu(course_key)

    elif viewing_mode == "graded":
        clear_ui()
        print(f'\nLIST OF STUDENTS, {course_key} {courses[course_key][0]}')
        print(f'\nHere you can see all the students of {courses[course_key][0]} course \nThat have being graded'
              '\n\nGRADED STUDENTS\n')    
        print_dictionary_data_as_table("graded_students_list_of_course_students",course_key)

        print("\na) Show all students\nb) Show only non-graded \nc) Back to course menu")
        user_input = input_checker(": ","Only 'a' 'b' and 'c' are valid inputs!")
        if user_input == 'a':
            list_of_course_students_menu(course_key,"all")
        elif user_input == 'b':
            list_of_course_students_menu(course_key,"non-graded")
        elif user_input == 'c':
            course_menu(course_key)        


def main_menu():
    """
    This is the first menu that opens when program has being started
    Lets user define a new course, search for courses and see the 
    list of courses
    """
    try:
        file_from_dict = dict(json_data_file_reader())
        courses.update(file_from_dict)
    except FileNotFoundError:
        print("It's your first time using the app!")
        time.sleep(1)
    clear_ui()
    print("\nSTUDENT AND COURSE REGISTRY.\n"
        "Main Menu\n"
        "This program is used for defining courses,\n"
        "registering students to these courses and grading the students\n"
        "course performance.\n\n"
        "You can operate the menus by either typing the letter that corres-\n"
        "ponds to your desired action and pressing enter OR by following \n"
        "the instructions, if no letters are present in the menu. \n\n"
        "You must first define a course, and after that you can start \n"
        "adding students to it and start adding grades.\n\n"
        "a) Define a new course.\nb) Search for existing course"
        "\nc) Table of saved courses\nd)Save and exit")

    user_input = input_checker(": ","Only 'a' 'b' 'c' and 'd' are valid inputs!")

    if user_input == 'a':
        define_course_menu()

    elif user_input == 'b':
        course_selection_menu()

    elif user_input == 'c':
        list_of_courses_menu()
    
    elif user_input == 'd':
        save_and_quite_menu()


def course_menu(course_key):
    clear_ui()
    print(f'\nSTUDENT REGISTER, {course_key} {courses[course_key][0]}\n')
    print(f'By selecting "add student" you can add a new student to {courses[course_key][0]}\n'
          "course, selecting 'Grade student' you can grade the student"
          f' on {courses[course_key][1].casefold()}\n'
          "scale. By selecting 'Students list' you can see all the students that are attending"
          " the\n"
          "course and their grades, and also filter to see only the students that have a grade\n"
          "or those that dont have a grade. selecting 'main menu' will take you back to"
          " main menu\n")

    print("a) Add student\nb) Grade student\nc) Students list\nd) Main menu\n")
    user_input = input_checker(": ","Only 'a' 'b' 'c' and 'd' are valid inputs!")

    if user_input == 'a':
        add_student_to_course_menu(course_key)
    elif user_input == 'b':
        student_grading_menu(course_key)
    elif user_input == 'c':
        list_of_course_students_menu(course_key)
    elif user_input == 'd':
        main_menu()


if __name__ == "__main__":
    main_menu()
    