import pandas as pd

#TODO: independent studies
def courses_from_excel(df, courses, removed_courses):
    df = df.fillna("NaN")
    course_list = []
    on_campus = True
    for index, row in df.iterrows():

        if str(row["Registrations Used"]).find("(Dropped)") != -1:
            continue

        course = str(row["Registrations Used"]).replace('/', '  ')[:9].replace("-", " ").strip()
        #print(course[4:7])
        # check if column entry is actually a course (that isnt a project)
        if any(char.isdigit() for char in course[:6]) and "PE" not in course[:3] and "Requ" not in course:
            course_list.append(course.replace(" ", "_"))
            if course == "ID 2050":
                on_campus = False
        elif course[3:7].strip() == "IQP":
            if on_campus:
                course_list.append("IQP_ON_CAMPUS")
            else:
                course_list.append("IQP_OFF_CAMPUS")
    #print("COURSE LIST BEFORE EVERYTHING: "+str(course_list))
    course_list += courses
    #print("COURSE LIST WITH ADDED: " + str(course_list))
    course_list = list(filter(lambda i: i not in removed_courses, course_list))
    #print("COURSE LIST WITH DELETED: " + str(course_list))
    course_list = set(course_list)
    course_list = list(course_list)
    #print("COURSE LIST FROM PROCESS WORKDAY: "+str(course_list))
    #print(course_list)
    return course_list

# columns = ["Requirement","Status", "Registrations Used", "Remaining", "Academic Period","Credits","Grade"]
#
# test = pd.read_excel("studentdata/View_My_Academic_Progress.xlsx", header=9)
# print(test.head(10))
# print(test.columns)
# print(courses_from_excel(test))