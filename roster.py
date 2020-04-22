from sys import argv
from cs50 import SQL

if len(argv) != 2:
    print("usage error, roster.py HouseName")
    exit()
db = SQL("sqlite:///students.db")
students = db.execute("select * from students where house = (?) order by last,first desc", argv[1])
for student in students:
    if student['middle'] == None:
        print(f"{student['first']} {student['last']} , born {student['birth']}")
    else:
        print(f"{student['first']} {student['middle']} {student['last']}, born {student['birth']}")