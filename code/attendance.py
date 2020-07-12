import pandas as pd


def attendance(file_name, n_min=3):
    f = open("..\\data\\%s" % file_name, encoding='utf-8', mode="r")
    f.readline()
    f.readline()

    file = f.read().title()
    f.close()

    teachers = set(get_teachers().Nicknames).union(set(get_teachers().Nomes))

    file = file.replace("\n", ",").split(",")
    current_students = {}
    for person in file:
        if person not in teachers and len(person) > 0:
            if person not in current_students.keys():
                current_students[person] = 1
            else:
                current_students[person] += 1
    valid_students = []
    for person in current_students:
        if current_students[person] >= n_min:
            valid_students.append(person)
    valid_students.sort()
    for student in valid_students:
        print(student)


def format_names(roles=['alunos', 'professores']):
    for role in roles:
        f = open("..\\data\\%s.csv" % role, encoding='utf-8', mode="r")
        f.readline()
        formatted = f.read().title()
        f.close()
        f = open("..\\data\\%s.csv" % role,  encoding='utf-8', mode="w")
        f.write(formatted)
        f.close()


def get_students():
    students = pd.read_csv("..\\data\\alunos.csv")
    students = students[students.Status != 'Nok']
    students.pop('Status')
    students.Nicknames = students.Nicknames.fillna(students.Nomes)
    return students


def get_teachers():
    teachers = pd.read_csv("..\\data\\professores.csv")
    teachers.Nicknames = teachers.Nicknames.fillna(teachers.Nomes)
    return teachers


attendance('Meet Attendance - Attendance.csv')

