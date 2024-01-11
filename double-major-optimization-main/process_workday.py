import pandas as pd

def courses_from_excel(df):
    df = df.fillna(0)
    course_list = []
    for index, row in df.iterrows():
        course = str(row["Remaining"])
        #print(course[4:7])
        #text
        #please work
        if any(char.isdigit() for char in course[:8]) or course[3:7].strip() == "IQP":
            #print("true!")
            continue
        else:
            print(course)

columns = ["Requirement","Status","Remaining","Registrations Used","Academic Period","Credits","Grade"]

test = pd.read_excel("studentdata/View_My_Academic_Progress.xlsx", names=columns)
courses_from_excel(test)