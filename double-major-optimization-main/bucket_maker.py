import pandas as pd

#step 1: get list of unique courses by major
#reqs = pd.read_csv("studentdata/reqs_all_lists.csv")
#reqs = pd.read_excel()
all_courses = {}
xls = pd.ExcelFile("Data/Sheets/Requirements.xlsx")
reqs = pd.read_excel(xls, 'Reqs')
sreqs = pd.read_excel(xls, 'Sreqs')

programs = ["ECE_MAJOR"]
masters = False
course_code = None

for p in programs:
    if "_MASTER" in p[0]:
        #assume no more than 1 masters program in the "programs" input
        course_code = programs[0][:4].strip("_M")
        masters = True
        print(course_code)

#regular reqs
for index, row in reqs.iterrows():
    #only doing DS for now
    if row['Program Key'] == "ALL_MAJORS" or row['Program Key'] in programs: #or row["Program Key"] == "ALL_MAJORS_REST"
        courses = row['Courses that fill req']
        #print(courses)
        for course in eval(courses):
            #print(course)
            #print(all_courses)
            if str(course) not in all_courses:
                all_courses[str(course)] = [row['Req Key']]
            else:
                all_courses[str(course)].append(row['Req Key'])
#super reqs
sl_iterator = 0
for index, row in sreqs.iterrows():
    if row['Program Key'] == "ALL_MAJORS"  or  row['Program Key'] in programs: #or row["Program Key"] == "ALL_MAJORS_REST":
        courses = row['Applicable Courses']
        #print(courses)
        #if we don't have a type 2 sreq:
        if type(eval(courses)[0]) == str:
            for course in eval(courses):
                #print(course)
                #print(all_courses)
                if course not in all_courses:
                    all_courses[course] = [row['Sreq Key']]
                else:
                    all_courses[course].append(row['Sreq Key'])
        else:
            #we found one that has sublists (type 2 sreq) - we need to append [req_name]_SL_num for each sublist
            for i in range(len(eval(courses))):
                s = str(row['Sreq Key']) + "_SL_" + str(i)
                course_sl = eval(courses)[i]
                for course in course_sl:
                    if str(course) not in all_courses:
                        #s = str(row['Sreq Key'])+"_SL_"+str(i)
                        print(course)
                        all_courses[str(course)] = [s]
                        # s = "HUA_DEPTH_SL_"+str(i)
                        # print(s)
                        # all_courses[str(course)].append(s)
                    #should never happen
                    else:
                        (print(course))
                        all_courses[str(course)].append(s)
                        # s = "HUA_DEPTH_SL_" + str(i)
                        # print(s)
                        # all_courses[str(course)].append(s)

print("ALL COURSES: "+str(all_courses))
# step 1.5: if we have an MS program, drop all MS restriction reqs that aren't looking at the program we're looking at
# step 1.5 v2: if
# if masters:
#     for k, course_list in all_courses.items():
#         all_courses[k] = [x for x in course_list if course_code in x[:5].strip("_M_")]
#         #course_list =
#     print("ALL COURSES: "+str(all_courses))


#print(all_courses)
#step 2: for each course:
    #check which reqs this course belongs to
        #kinda done above...
all_reqs = {}
for course in all_courses:

    #if that combination of reqs is so far unseen:
        #create new bucket with that course and those reqs
    if str(all_courses[course]) not in all_reqs:
        all_reqs[str(all_courses[course])] = [course]
    #else:
        #add this course to the existing bucket with that combination of reqs
    else:
        all_reqs[str(all_courses[course])].append(course)
print(all_reqs)

#call them "DS_bucket1", "DS_bucket2", etc... will manually name them later
df = pd.DataFrame.from_dict(data=all_reqs, orient="index") #columns=["bucket_reqs", "bucket_courses"])

# Create a new column that contains lists of non-None values from previous columns
df['Bucket Contents'] = df.apply(lambda row: [item for item in row if item is not None], axis=1)

# Drop the original columns (0, 1, ..., 11)
df.drop(columns=list(range(len(df.columns)-1)), inplace=True)
#df = df['']

df.rename(columns={None: 'Req Keys'})
df['Bucket Key'] = None
df['Bucket Size'] = df.apply(lambda row: [len(item) for item in row if item is not None][0], axis=1)
df['Choice Weight'] = df.apply(lambda  row: [row["Bucket Size"]][0], axis=1)
df['Credits Each'] = df.apply(lambda row: [3 for item in row if item is not None][0], axis=1)
df['Bucket Description'] = None
df.index.names = ["Req Keys"]

#Credits Each

df = df.reindex(columns = ['Bucket Key', 'Bucket Size', 'Choice Weight', 'Credits Each', 'Bucket Description', 'Bucket Contents', 'Req Keys'])

with pd.ExcelWriter('Data/Sheets/Buckets.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name='ECE_MAJOR')
print(df)