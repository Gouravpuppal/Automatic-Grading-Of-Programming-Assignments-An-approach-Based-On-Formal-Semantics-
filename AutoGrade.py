from tkinter import *
import tkinter
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import numpy as np
import os
import subprocess
import os
import re

main = tkinter.Tk()
main.title("Automatic Grading of Programming Assignments")
main.geometry("1300x900")

global refrence_file, submission_file, incorrect, code_samples

def uploadReference():
    global refrence_file
    text.delete('1.0', END)
    refrence_file = filedialog.askdirectory(initialdir=".")
    text.insert(END,refrence_file+" loaded\n\n")
    tf1.insert(END,refrence_file)

def uploadSubmission():
    global submission_file
    submission_file = filedialog.askdirectory(initialdir=".")
    text.insert(END,submission_file+" loaded\n\n")
    tf2.insert(END,submission_file)

def executeSubmission():
    global submission_file, refrence_file, incorrect
    incorrect = []
    text.delete('1.0', END)
    expected = tf3.get()
    array = expected.split(",")
    parent_file = submission_file
    print(parent_file)
    submissions = os.listdir(submission_file)
    for i in range(len(submissions)):
        if '.class' not in submissions[i]:
            out = subprocess.run('javac '+parent_file+'/'+submissions[i], stderr = subprocess.PIPE, shell=True)
            msg = out.stderr.splitlines()
            if len(msg) == 0:
                exe_name = submissions[i].split(".")
                out = subprocess.check_output('java -classpath '+parent_file+' '+exe_name[0]+' '+array[1]+' '+array[2]+' '+array[3], shell=True)
                output = out.decode().strip("\r\n").strip()
                if output != array[0]:
                    incorrect.append(submissions[i])
                text.insert(END,"Submission file: "+submissions[i]+" Generated Output: "+output+" Expected Output: "+array[0]+"\n\n")    

def readFile(file_path):
    data = ""
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip('\n')
            line = line.strip()
            arr = line.split(" ")
            if len(arr) >= 2:
                if arr[0].strip() == 'if' or arr[1].strip() == 'if':
                    data += line+" "
    file.close()
    data = data.strip()
    return data

def calculateDiversePath(reference, submission):
    reference = re.sub('[()=]', '', reference)
    submission = re.sub('[()=]', '', submission)
    arr = submission.split(" ")
    return len(arr)

def autoGrader():
    global submission_file, refrence_file, code_samples
    code_samples = []
    text.delete('1.0', END)

    reference = readFile(refrence_file+"/Ref1.java")
    code_samples.append(reference)
    submissions = os.listdir(submission_file)
    for i in range(len(submissions)):
        if '.class' not in submissions[i]:
            code = readFile("Submission/"+submissions[i])
            code_samples.append(code)

    for i in range(1,len(code_samples)):
        diverse = calculateDiversePath(code_samples[0],code_samples[i])
        if diverse > 6:
            text.insert(END,submissions[i-1]+" is an Incorrect submission\n\n")
        else:
            text.insert(END,submissions[i-1]+" is a Correct submission\n\n")            


font = ('times', 16, 'bold')
title = Label(main, text='Automatic Grading of Programming Assignments: An Approach Based on Formal Semantics',anchor=W, justify=LEFT)
title.config(bg='black', fg='white')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)


font1 = ('times', 13, 'bold')

l1 = Label(main, text='Upload Reference File:')
l1.config(font=font1)
l1.place(x=50,y=100)

tf1 = Entry(main,width=35)
tf1.config(font=font1)
tf1.place(x=250,y=100)

referenceButton = Button(main, text="Upload Reference File", command=uploadReference)
referenceButton.place(x=620,y=100)
referenceButton.config(font=font1)

l2 = Label(main, text='Upload Submission File:')
l2.config(font=font1)
l2.place(x=50,y=150)

tf2 = Entry(main,width=35)
tf2.config(font=font1)
tf2.place(x=250,y=150)

submissionButton = Button(main, text="Upload Submission File", command=uploadSubmission)
submissionButton.place(x=620,y=150)
submissionButton.config(font=font1)

l3 = Label(main, text='Expected & Input Values')
l3.config(font=font1)
l3.place(x=50,y=200)

tf3 = Entry(main,width=35)
tf3.config(font=font1)
tf3.place(x=250,y=200)


executeButton = Button(main, text="Execute Submission", command=executeSubmission)
executeButton.place(x=250,y=250)
executeButton.config(font=font1)

autoButton = Button(main, text="Run AutoGrader", command=autoGrader)
autoButton.place(x=480,y=250)
autoButton.config(font=font1)

text=Text(main,height=20,width=120)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=300)
text.config(font=font1)

main.config(bg='chocolate1')
main.mainloop()
