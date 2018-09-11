# Create by Dev Kapupara. Please do not distribute.
# Script made for CS46B class managed by Dr. Philip Heller
# For any bugs or clarification, email me at devkapupara@gmail.com with subject CS46B Script.py
# Made it because I was lazy to unzip each student's jar file and run it from the terminal.

import subprocess as sp
import os
import glob
import shutil
import re
import requests

access_token = '12~RxG1tLwuimVxW2XRoqOIU1SvJWgzygwQ6629Qg4Fyb998Ou40jvD2wQzqh4VJNFC'
course_id = 1271170
header = {'Authorization': 'Bearer ' + access_token}
base = 'https://sjsu.instructure.com/api/v1/courses/'

# base_dir is your downloaded submissions folder. Change it accordingly if paths keep changing.
base_dir = '/Users/devkapupara/Desktop/submissions'

grades_dict = {}  # id:(score, comments)
roster = {}       # id:name


def open_url(url):
    return requests.get(url, headers=header).json()


def fetch_roster():
    get_students_link = base + '{}/students'.format(course_id)
    user_list = open_url(get_students_link)
    for user in user_list:
        roster[str(user['id'])] = user['name']


def grade_submissions():

    script_created_objects = []                                 # For cleanup purposes after running the script.

    cleanup = True if input("Clean up after extracting and running programs? [Y/N]: ").lower() == 'y' else False
    package_name = input("Enter package name for the assignment: ")             # Package name. Very Important
    main_file_name = input("Enter the class name with the main method: ")       # Tester file containing the main function. Very Important

    os.chdir(base_dir)                      # Navigate to the base_dir

    detailed_grades = open('detailed_grades.txt', 'w')        # Setup grades.txt file

    # SMH! Some students will submit .zip even if instructions ask for .jar. So an additional check for them
    for file in glob.glob('*.zip'):
        user_id = file.split('_')[1]
        sp.run('unzip -p {} > x_{}_hw.jar'.format(file, user_id), shell=True)
        script_created_objects.append(os.path.join(base_dir, 'x_{}_hw.jar'.format(user_id)))

    print("Following students found...")
    separator = '-'*20
    # Now that we have all the jar files, lets start working.
    for file in glob.glob('*.jar'):
        user_id = file.split('_')[1]                # Get the student name
        print(roster[user_id])                              # Print it to look nice.
        if user_id not in os.listdir(os.getcwd()):  # If folder created previously, which SHOULD NOT be the case, don't create it.
            script_created_objects.append(os.path.join(base_dir,user_id))
            os.mkdir(user_id)
        extract_path = os.path.join(base_dir,user_id)               # Go the extracted folder.
        os.chdir(extract_path)
        sp.run('jar -xf ' + os.path.join(base_dir, file), shell=True)
        try:
            sp.run('javac ' + os.path.join(extract_path, package_name, '*.java'), stderr=sp.PIPE, shell=True, check=True)
        except sp.CalledProcessError as e:
            grades_dict[user_id] = (0, e.stderr.decode())
            os.chdir(base_dir)
            continue
        try:
            # Try to run the program, pipe the error and output to python shell, decode the output and split at new
            # lines to build comments. The last line contains points, so I grab it using regex. Comments include
            # grader bot output or if a compile/runtime error occur, we use the JVM error output as comments.
            result = list(filter(lambda x: x != '', sp.run('java {}.{}'.format(package_name,main_file_name), shell=True,
                                        stdout=sp.PIPE, stderr=sp.PIPE, check=True).stdout.decode('ascii').split('\n')))
            comments = '\n'.join(result[:-1])
            points = re.findall('\d+', result[-1])[0]
            grades_dict[user_id] = (points, comments)
        except sp.CalledProcessError as e:
            grades_dict[user_id] = (0, e.stderr.decode())
            continue
        finally:
            os.chdir(base_dir)

    for uid in roster:
        if uid not in grades_dict:
            grades_dict[uid] = (0, "No submission made.")
        detailed_grades.write("Name: {}\nScore:{}\nComments:\n{}\n{}\n".format(roster[uid], grades_dict[uid][0],
                                                                               grades_dict[uid][1], separator))

    if cleanup:                 # If user wanted cleanup, then only shall I clean. Some people like messy stuff.
        for path in script_created_objects:
            if os.path.isdir(path):                                 # Clean up directories after
                shutil.rmtree(path, ignore_errors=True)
            else:
                os.remove(path)
    detailed_grades.close()              # Why are you still open? Time to close bud, our work is done.
    print("All done here! Please check the grades.txt and detailed_grades.txt file for the scores.")


def get_assignment_id():
    """Fetches the assignment id from canvas. Needed for uploading grades."""
    name = "Assignment " + input("Enter assignment number: ")
    get_assignment = base + '{}/assignments'.format(course_id)
    assignment_details = open_url(get_assignment)
    aid = None
    for assignment_dict in assignment_details:
        if assignment_dict['name'] == name:
            aid = assignment_dict['id']
    return aid


def upload_grades():
    """Uploads grade to canvas using the assignment id, student id and course id."""
    assignment_id = get_assignment_id()
    if assignment_id:
        for student_id in grades_dict:
            grade_link = base + '{}/assignments/{}/submissions/{}'.format(course_id, assignment_id, student_id)
            data = {'comment[text_comment]': grades_dict[student_id][1], 'submission[posted_grade]': grades_dict[student_id][0]}
            requests.put(grade_link, params=data, headers=header)
        print("Successfully upload grades to Canvas.")
    else:
        print("Assignment not found. Exiting...")
        quit()


if __name__ == '__main__':
    fetch_roster()
    grade_submissions()
    upload_grades()
