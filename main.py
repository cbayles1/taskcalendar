import os, csv, datetime
from settings import *

allTasks = []

def addTaskToArr(newTask,arr=allTasks):
    index = 0
    for task in allTasks:
        if (task["date"] >= newTask["date"]): break
        index += 1
    arr.insert(index,newTask)

def fillArrFromFile(arr=allTasks, csvFile=INPUT_FILE):
    filepath = os.path.join(MAIN_DIR, csvFile)
    if not os.path.exists(filepath): 
        print("File not found. Array is now empty.")
        return arr
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if (len(row) < 1): continue
            newTask = {
                "date": datetime.datetime.strptime(row[0], '%Y-%m-%d').date(),
                "desc": row[1]
            }
            arr.append(newTask)
    return arr

def saveArrToFile(arr=allTasks, csvFile=INPUT_FILE):
    filepath = os.path.join(MAIN_DIR, csvFile)
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, ['date','desc'])
        for task in arr:
            writer.writerow(task)

def printArr(arr=allTasks):
    for task in arr:
        month = task["date"].month
        day = task["date"].day
        print("{m:>2}/{d:<2}    {desc}".format(m=str(month),d=str(day),desc=task["desc"]))

def getTaskFromInput():
    year = input("Enter the year: ")
    month = input("Enter the month: ")
    day = input("Enter the day: ")

    if len(year) < 1: year = str(CURRENT_DATE.year)
    if len(month) < 1: month = str(CURRENT_DATE.month)
    if len(day) < 1: day = str(CURRENT_DATE.day)
    date = datetime.date(int(year), int(month), int(day))

    desc = input("Enter a description: ")
    newTask = {
        "date": date,
        "desc": desc
    }
    return newTask

def deleteTaskFromArr(taskToDelete, arr=allTasks):
    for task in arr:
        if (task["date"] == taskToDelete['date'] and task["desc"] == taskToDelete['desc']):
            arr.remove(task)

def migrateOldTasks(arr=allTasks, current_date=CURRENT_DATE):
    for task in arr:
        if (task["date"] < current_date):
            task["date"] = current_date

#MAIN
if __name__ == "__main__":
    fillArrFromFile()
    migrateOldTasks()
    printArr()
    running = True
    while (running):
        print("A: Add task")
        print("D: Delete task")
        print("V: View planner")
        print("X: Exit")
        choice = input("Your selection: ").lower()
        print()
        if (choice == 'a'):
            addTaskToArr(getTaskFromInput())
        elif (choice == 'd'):
            descStr = input("Enter the description: ")
            for task in allTasks:
                if (task["desc"] == descStr): deleteTaskFromArr(task)
        elif (choice == 'v'):
            printArr()
        elif (choice == 'x'):
            running = False
        else:
            print("Try that again.")
        saveArrToFile()
        print("Changes saved.\n")