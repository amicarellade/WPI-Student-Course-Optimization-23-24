import pandas as pd

all_programs = []
xls = pd.ExcelFile("Data/Sheets/Requirements.xlsx")
sreqs = pd.read_excel(xls, 'Sreqs')
masters = True

# first pass - get list of all Masters programs
for index, row in sreqs.iterrows():
    if row["Program Key"] == "ALL_MAJORS_REST" and "C_REST_G_" in row["Sreq Key"] and pd.notnull(sreqs['Applicable Reqs'][index]):
        for program in eval(row["Applicable Reqs"]):
            course_code = program[:4].split("_")[0]
            if course_code not in all_programs and len(course_code.strip()) > 0:
                all_programs.append(course_code)

# for every Masters program, find which sreqs belong to that Masters program.
# Change the Program Key of each requirement to be "[DEPT CODE]_MASTER", and delete
# each other dept from the Applicable Reqs. Remember that we've distinguished between _M and _BSMS.
    # need to exclude "UGG" sreqs for masters
new_sreqs = pd.DataFrame()
for index, row in sreqs.iterrows():
    for program in all_programs:
        #print(program)
        #print(program)
        new_reqs = []
        if pd.notnull(sreqs['Applicable Reqs'][index]):
            #print("APPLICABLE REQS: "+str(row["Applicable Reqs"]))
            #make it a list
            row["Applicable Reqs"] = str(row["Applicable Reqs"])
            for req in eval(row["Applicable Reqs"]):
                #print("PROGRAM: "+str(program))
                print("REQ: "+str(req))
                if masters:
                    s = program+"_M_"
                else:
                    s = program+"_BSMS_"
                if s in req:
                    new_reqs.append(req)
                    print("NEW REQS: "+str(new_reqs))
            if len(new_reqs) > 0:
                copy = row.copy()
                copy["Program Key"] = str(program)+"_MASTER"
                copy["Applicable Reqs"] = new_reqs
                new_sreqs = new_sreqs.append(copy)
print(new_sreqs)
with pd.ExcelWriter('Data/Sheets/Requirements.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    new_sreqs.to_excel(writer, sheet_name='TEST_SREQS')