from sys import argv
from cs50 import SQL
from csv import reader

db = SQL("sqlite:///students.db")

if len(argv) != 2:
    print("usage error, import.py students.csv")
    exit()

with open(argv[1], newline='') as studf:
    students= reader(studf)
    for student in students:
        if student[0] == 'name':
            continue
        name = student[0].split()
        if len(name) < 3:
            db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",name[0], None, name[1], student[1], student[2])

        else:
            db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",name[0], name[1], name[2], student[1], student[2])