import csv
from os import system
from time import sleep


# datafile class for the file. with methods to read and write and display the contents
class dataFile:
    def __init__(self, fileName):
        self.filename = fileName

    # read the file and return the contents as a list
    def readFile(self):
        tasklist = []
        with open(self.filename, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                tasklist.append(row)
        return tasklist

    # accepts tasklist as arguement then formats it to display on screen
    def displayFile(self, tasklist):
        iteration = 0
        numberOfCompleteTasks = 0
        numberWork = 0
        numberPersonal = 0
        numberStudy = 0
        totalNumberofTasks = 0
        percentageCompletedTasks = 0.00
        percentageWork = 0.00
        percentagePersonal = 0.00
        percentageStudy = 0.00
        for row in tasklist:
            print(
                f"{row[0]:>3} {row[1]:<20} {row[2]:<50} {row[3]:<20} {row[4]:<15}", end="\n")
            if iteration == 0:
                print(f"_"*3, "_"*20, "_"*50, "_"*20, "_"*15, end="\n")
            if row[4].lower() == "completed":
                numberOfCompleteTasks += 1
            if row[3] == "Work":
                numberWork += 1
            if row[3] == "Personal":
                numberPersonal += 1
            if row[3] == "Study":
                numberStudy += 1
            iteration += 1
        totalNumberofTasks = iteration - 1
        percentageCompletedTasks = (
            numberOfCompleteTasks/totalNumberofTasks)*100
        percentageWork = (numberWork/totalNumberofTasks)*100
        percentagePersonal = (numberPersonal/totalNumberofTasks)*100
        percentageStudy = (numberStudy/totalNumberofTasks)*100
        print("Statistics:")
        print(
            f"Tasks: {totalNumberofTasks}, " 
            f"Completed: {numberOfCompleteTasks}, ({percentageCompletedTasks:.2f}%)")
        print(
            f"Work: {numberWork} ({percentageWork:.2f}%), "
            f"Study: {numberStudy} ({percentageStudy:.2f}%), "
            f"Personal: {numberPersonal} ({percentagePersonal:.2f}%)")

    # writes contents to the file.
    # to add new line. open the file as append
    # to delete or modify the line. open the file with truncate mode first to write
    # then open it in append mode to add lines
    def writeFile(self, details, mode, rownumber):
        with open(self.filename, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            rowcount = len(list(csvreader))
        if mode == "add":
            with open(self.filename, "a+", newline="\n") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(
                    [rowcount, details[0], details[1], details[2], details[3]])
        elif mode == "truncate":
            with open(self.filename, "w", newline="\n") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(
                    ["No.", "TaskName", "Description", "Category", "Status"])
        return

# function to get user input. used to add new tasks or modify tasks
def getInput():
    taskName = input(f"Task Name: ")
    taskDescription = input(f"Description: ")
    while True:
        taskCategory = input(f"Category: (Work, Personal, Study) ")
        if taskCategory == "Work" or taskCategory == "Personal" or taskCategory == "Study":
            break
        else:
            print("Please choose from (Work, Personal, Study)")
            continue
    taskStatus = "In Progress"
    return [taskName, taskDescription, taskCategory, taskStatus]

# function to add new tasks


def addTask(csvfileparam):
    taskDetails = getInput()
    csvfileparam.writeFile(taskDetails, "add", None)
    print(
        f"{taskDetails[0]}, {taskDetails[1]}, {taskDetails[2]}, {taskDetails[3]}")
    print("Was Succesfully Added!")
    return

# function to update tasks. used in both deleting and modifying tasks.
# accepts the following arguments
# csvfileparam - csv file
# tasklist - list of tasks
# taskDetails - details of specific tasks to update. used only in modify mode
# rowNumber - row number to delete or modify
# mode - delete or modify
def updateTask(csvfileparam, tasklist, taskDetails, rowNumber, mode):
    iteration = -1
    for row in tasklist:
        iteration += 1
        if iteration == rowNumber and mode == "delete":
            continue
        elif iteration == rowNumber and mode == "modify":
            csvfileparam.writeFile(
                [taskDetails[0], taskDetails[1], taskDetails[2], taskDetails[3]], "add", rowNumber)
        elif iteration == 0:
            csvfileparam.writeFile(
                [row[1], row[2], row[3], row[4]], "truncate", rowNumber)
        else:
            csvfileparam.writeFile(
                [row[1], row[2], row[3], row[4]], "add", rowNumber)

# function to delete tasks
def deleteTask(csvfileparam, rowNumber):
    iteration = -1
    tasklist = csvfileparam.readFile()
    if int(rowNumber) > len(list(tasklist)):
        return -1
    for row in tasklist:
        iteration += 1
        if iteration == int(rowNumber):
            oldtaskName = row[1]
            oldtaskDescription = row[2]
            oldtaskCategory = row[3]
            oldtaskStatus = row[4]
            break
    print("Are you sure you want to delete:")
    print(f"{oldtaskName}, {oldtaskDescription}, {oldtaskCategory}, {oldtaskStatus}")
    while True:
        choice = input("press (y) continue, (x) to cancel: ")
        if choice.lower() == "y":
            updateTask(csvfileparam, tasklist, None, int(rowNumber), "delete")
            print("Succefully Deleted!")
            break
        elif choice.lower() == "x":
            print("Delete Cancelled!")
            break
        else:
            continue
    return 0

# function to modify tasks
def modifyTask(csvfileparam, markComplete, rowNumber):
    iteration = -1
    tasklist = csvfileparam.readFile()
    if int(rowNumber) > len(list(tasklist)):
        return -1
    for row in tasklist:
        iteration += 1
        if iteration == int(rowNumber):
            oldtaskName = row[1]
            oldtaskDescription = row[2]
            oldtaskCategory = row[3]
            oldtaskStatus = row[4]
            # print(f"{row[1]}, {row[2]}, {row[3]}, {row[4]}")
            break
    if markComplete == True:
        taskDetails = ["", "", "", ""]
        taskDetails[0] = oldtaskName
        taskDetails[1] = oldtaskDescription
        taskDetails[2] = oldtaskCategory
        taskDetails[3] = "Completed"
        print("Do you want to mark complete:")
        print(
            f"{taskDetails[0]}, {taskDetails[1]}, {taskDetails[2]}, {taskDetails[3]}")
    else:
        print(
            f"Modifying: {oldtaskName}, {oldtaskDescription}, {oldtaskCategory}, {oldtaskStatus}")
        print("Press Enter to Retain")
        taskDetails = getInput()
        if taskDetails[0] == "":
            taskDetails[0] = oldtaskName
        if taskDetails[1] == "":
            taskDetails[1] = oldtaskDescription
        if taskDetails[2] == "":
            taskDetails[2] = oldtaskCategory
        taskDetails[3] = oldtaskStatus
        print("do you want to change:")
        print(
            f"{oldtaskName}, {oldtaskDescription}, {oldtaskCategory}, {oldtaskStatus}")
        print("to")
        print(
            f"{taskDetails[0]}, {taskDetails[1]}, {taskDetails[2]}, {taskDetails[3]}")
    while True:
        choice = input("press (y) continue, (x) to cancel: ")
        if choice.lower() == "y":
            updateTask(csvfileparam, tasklist, taskDetails,
                       int(rowNumber), "modify")
            print("Succefully Updated!")
            break
        elif choice.lower() == "x":
            print("Updated Cancelled!")
            break
        else:
            continue
    return 0


# Main function
csvfile = dataFile("DataFile.csv")
while True:
    system("cls")
    errorNumber = -1
    tasklist = csvfile.readFile()
    csvfile.displayFile(tasklist)
    choice = input(
        f"Press (a) to add, (m) to modify, (d) to delete, (c) to mark completed (x) to exit: ")
    if choice.lower() == "a":
        addTask(csvfile)
    elif choice.lower() == "m":
        while errorNumber != 0:
            rowchoice = input(f"Enter row: ")
            errorNumber = modifyTask(csvfile, False, rowchoice)
            if errorNumber == -1:
                print(f"Invalid Row Number")
                sleep(2)
                system("cls")
    elif choice.lower() == "c":
        while errorNumber != 0:
            rowchoice = input(f"Enter row: ")
            errorNumber = modifyTask(csvfile, True, rowchoice)
            if errorNumber == -1:
                print(f"Invalid Row Number")
                sleep(2)
                system("cls")
    elif choice.lower() == "d":
        rowchoice = input(f"Enter row: ")
        errorNumber = deleteTask(csvfile, rowchoice)
        if errorNumber == -1:
            print(f"Invalid Row Number")
    elif choice.lower() == "x":
        print(f"Exiting...")
        break
    else:
        print("Invalid Choice")
    sleep(3)
