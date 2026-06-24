def get_grade(mark):

    mark = float(mark)


    if mark >= 90:
        return "O",10

    elif mark >= 80:
        return "A+",9

    elif mark >= 70:
        return "A",8

    elif mark >= 60:
        return "B+",7

    elif mark >= 50:
        return "B",6

    else:
        return "F",0