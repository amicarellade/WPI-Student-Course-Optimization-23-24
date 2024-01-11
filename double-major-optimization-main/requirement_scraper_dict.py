import pandas as pd
import numpy as np

reqs = pd.DataFrame(columns=['major', 'req_name', 'req_courses'])

# majors = {}
# reqs = {}
#
# test = "CS 525 -"
# test = test.replace('-', '').strip().replace(" ", "_")
# print(test)
#


df4 = pd.read_csv('studentdata/2023.csv')
df3 = pd.read_csv('studentdata/2022.csv')
df2 = pd.read_csv('studentdata/2021.csv')
df1 = pd.read_csv('studentdata/2020.csv')

dfs = [df4, df3, df2, df1]
#dfs = [df4, df3]
#dfs = [df4]

for i in range(len(dfs)):
    data = dfs[i]
    print("data sheet "+str(i)+" started")
    for index, row in data.iterrows():
        req = row['Academic Requirement']
        # "2023" LOGIC - IF REQ NOT IN THE 2023 SHEET, SKIP IT
        if i > 0 and req not in reqs['req_name'].values:
            continue
        # IGNORE UNUSED COURSES:
        if "Unused Courses" in req or "Minor APR" in req:
            continue
        major = row['Program of Study']
        #IF COURSE IS MISSING, CONTINUE:
        try:
            course = row['Course'][:9].replace('-', '').strip().replace(" ", "_")
        except TypeError:
            if "Not Satisfied" in row["Requirement Completion Status"] and req not in reqs['req_name'].values:
                reqs.loc[len(reqs.index)] = [major, req, {}]
            # what would this else case be - we already ignore the minor APRs thing
            else:
                continue
        #print(index, course)
        #IGNORE GRAD COURSES:
        if "_5" in course:
            continue



        #print(row['Course'])
        if major not in reqs['major'].values or req not in reqs['req_name'].values:
            # print(reqs["major"])
            # print(major)
            reqs.loc[len(reqs.index)] = [major, req, {course: 1}]
            #reqs = pd.concat([reqs, pd.DataFrame([[major, req, [course]]], columns=['major', 'req_name', 'req_courses'])], ignore_index=False)
            # reqs = reqs.append(pd.concat([[major, req, [course]]], columns=['major', 'req_name', 'req_courses']),
            #                    ignore_index=True)
            #reqs = reqs.append([major, req, [course]], ignore_index=True)
        # elif req not in reqs['req_name']:
        #     reqs = reqs.append(pd.DataFrame([major, req, [course]], columns=['major', 'req_name', 'req_courses']), ignore_index=True)
        #     #reqs[reqs['major'] == major]['req'] = req
        #IF COURSE NOT ALREADY IN LIST OF COURSES:



        elif course not in list(reqs[reqs['req_name'] == req]['req_courses'])[0]:
            #print(course)
            #print(list(reqs[reqs['req_name'] == req]['req_courses'])[0])
            #reqs[reqs['req_name'] == req]['req_courses'] = [2, 3, 5]
            reqs.at[reqs.index[reqs['req_name'] == req][0], 'req_courses'][course] = 1
            #reqs.at[reqs.index[reqs['req_name'] == req][0], 'counts'] = list(reqs[reqs['req_name'] == req]['counts'])[0] + [1]
            # print(list(reqs[reqs['req_name'] == req]['req_courses']) + [course])
            # reqs[reqs['req_name'] == req]['req_courses'] = list(reqs[reqs['req_name'] == req]['req_courses']) + [course]
        else:
            #print('true')
            reqs.at[reqs.index[reqs['req_name'] == req][0], 'req_courses'][course] += 1

            #reqs.at[reqs.index[reqs['req_name'] == req][0], 'req_courses'] = list(reqs[reqs['req_name'] == req]['req_courses'])[0] + course
reqs = reqs.reset_index()
reqs = reqs.drop(["index"], axis=1)
#print(reqs['req_name'])
print(reqs)
reqs.to_csv('studentdata/reqs_all_dicts.csv')
    # if major not in majors:
    #     pass
    # else:
    #     if req not in majors[major]:
    #         majors[major][req] =
    #
    # if req not in reqs:
    #     reqs[req] = [course]
    # else:
    #     reqs[req].append(course)
    # majors[major] = reqs