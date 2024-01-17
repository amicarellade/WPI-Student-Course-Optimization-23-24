import pandas as pd

#TODO: independent studies
def courses_from_excel(df):
    df = df.fillna("NaN")
    course_list = []
    on_campus = True
    iqp = False
    for index, row in df.iterrows():
        course = str(row["Remaining"]).replace('/', '  ')[:9].replace("-", " ").strip()
        #print(course[4:7])
        # check if column entry is actually a course (that isnt a project)
        if any(char.isdigit() for char in course[:6]) and "PE" not in course[:3] and "Requ" not in course:
            course_list.append(course.replace(" ", "_"))
            if course == "ID 2050":
                on_campus = False
        elif course[3:7].strip() == "IQP":# and not iqp:
            if on_campus:
                course_list.append("IQP_ON_CAMPUS")
            else:
                course_list.append("IQP_OFF_CAMPUS")
            iqp = True
    course_list = set(course_list)
    course_list = list(course_list)
    #print(course_list)
    return course_list

columns = ["Requirement","Status","Remaining","Registrations Used","Academic Period","Credits","Grade"]

test = pd.read_excel("studentdata/View_My_Academic_Progress.xlsx", names=columns)
print(courses_from_excel(test))