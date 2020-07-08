
def attendance(file_name):
    f = open("..\\data\\%s" % file_name, "r")
    f.readline()
    f.readline()

    file = f.read()
    f.close()

    file = file.replace("\n", ",").split(",")
    students = {}
    for person in file:
        if len(person) > 0:
            if person not in students.keys():
                students[person] = 1
            else:
                students[person] += 1
    for person in students:
        if students[person] >= 3:
            print(person)
