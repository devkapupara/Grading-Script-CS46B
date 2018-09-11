# Grading-Script-CS46B
Grading Script that compiles and runs student submissions, uses the Grader Bot to get the scores, builds comments and uploads them back to the Canvas.

**NOTE: This script won't work on Windows due to unavailibility of Bash Shell commands.**

#### Instructions:
1) You need to have python 3.x to run this. I used 3.7 when developing it, so if some error occurs, please update your python setup to 3.7.

2) The first thing you should do is generate a Token from Canvas. To do this, click on your Account in the top-left corner, choose Settings -> Under Approved Integrations, click on New Token. Give any name you want and leave the expire part empty. Note down the token it generates. **You won't be able to copy this token once you close the window.** Paste this token in the access_token variable in the script.

2) Download the submissions from canvas, unzip it and note down its path. If you are on Mac, the easiest way to get the path is to left-click on the folder, press Command-C, open terminal, and press Command-V. It should paste the path of your submission folder.

3) After copying the path, open up the grading.py file and paste that path in the variable base_dir. 

4) Fire up the terminal, navigate to where you saved the grading script and type the following command: ```python3 grading.py```

5) The second will ask you if you want to clean up the folder after the script ends, which basically cleans all the extracted folder and .class, .java files. Next one will ask you the package name, which is very essential. Last one will ask you for the class name containing the main function, which will basically be a tester file provided by Dr. Heller to test your code.

6) Failure to do step 5 and 6 correctly will result in wrong results, possibly errors. I am counting on you so no error checking has been implemented.

7) It will run and do its job, printing out the names of students as it finds.

8) Once it finished grabbing id, scores and comments, it will ask you to enter the Assignment number. This is needed to fetch the assignment_id on canvas and upload the grades to the right destination. Please make sure about the number you enter here.

9) Once it's done uploading, it will print out a confirmation message, and you should be good.

10) A detailed_grades.txt file will be generated in your submission folder which contains detailed report of each student. It will mention the name of the student, points scored and the comments made for that submission.

###### Please email me at devkapupara@gmail.com for any clarification about the code or for reporting any bugs.
