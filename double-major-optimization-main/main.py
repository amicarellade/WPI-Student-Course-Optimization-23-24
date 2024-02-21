import user_functions as usr

#file_upload_mode = False

# program keys input: a list containing either "MATH_MAJOR", "OIE_MAJOR", or both
# program_keys = ['MATH_MAJOR', 'OIE_MAJOR']
program_keys = ['CS_MASTER']

# must be in the format DEPT_NUM, ex "OIE_2081"
# program does not check for course validity, unrecognized courses assumed to be 3 credits
courses_taken = []
#["MA_1021", "MA_1022", "MA_1023", "MA_1024", "MA_2071", "MA_2631", "MA_2073", "CS_1101", "CS_2102", "MA_2611", "MA_2612", "CS_3043", "CS_4445", "CS_4342", "CS_3733", "MIS_4084", "OIE_4430", "CS_3431", "MA_4631", "MA_4632", "MKT_3650", "MA_2201", "MIS_3720"]
#REMINDER TO FIX CS_558 PROBLEM AT SOME POINT (AND ACTUALLY DETERMINE IF IT IS A PROBLEM)

##['PH_1110', 'MA_1024', 'MA_2621', 'ECE_2010', 'OIE_2081', 'EN_2225', 'MA_3631', 'BUS_1010', 'PY_1731', 'FIN_1250','CS_3043', 'CS_4432', 'MA_1022', 'DS_1010', 'DS_2010', 'MA_2612', 'HU_3910', 'WR_1020', 'CS_3431', 'MA_2611', 'MA_2071', 'ID_2050', 'CS_2103', 'MA_2201', 'MA_2051', 'MA_1023', 'CS_4341', 'DS_3010', 'WR_2210','CS_1101', 'MA_1021', 'CS_2223', 'DS_4635', 'ECON_1120', 'WR_1011', "CS_4342", "MIS_3720", "CS_539", "CS_542"]
#["MA_1021", "MA_1022", "MA_1023", "MA_1024", "CS_1101", "CS_2102", "OIE_4430", "MIS_4084", "MKT_3650", "CS_3431", "MA_4635", "MA_2631", "MA_3631", "CS_3043", "CS_4804", "MA_2201"]
##['PH_1110', 'MA_1024', 'MA_2621', 'ECE_2010', 'OIE_2081', 'EN_2225', 'MA_3631', 'BUS_1010', 'PY_1731', 'FIN_1250', 'DS_551', 'DS_598','CS_3043', 'OIE_559', 'CS_4432', 'CS_586', 'MA_1022', 'DS_1010', 'DS_2010', 'MA_2612', 'HU_3910', 'BUS_3020', 'IQP_OFF_CAMPUS', 'WR_1020', 'CS_3431', 'MA_2611', 'MA_2071', 'ID_2050','CS_547', 'CS_2103', 'MA_2201', 'CS_1000', 'MA_2051', 'MA_1023', 'CS_4341', 'DS_3010', 'WR_2210', 'CS_541','CS_1101', 'MIS_584', 'MA_1021', 'CS_2223', 'DS_4635', 'CS_4342', 'ECON_1120', 'WR_1011']
##['MA_1021', 'DS_3010', 'ENV_130X', 'PH_1110', 'DS_1010', 'SP_1524', 'DS_2010', 'ETR_1100', 'BUS_2080', 'CS_2102', 'MA_1023', 'ES_1020', 'CS_2022', 'CS_2223', 'HU_3900', 'MA_2611', 'MA_1024', 'WR_1010', 'MA_2621', 'PY_2731', 'WR_253X', 'WR_3210', 'MA_1022', 'MA_2071', 'CS_1101']
##

#no grad here!
# courses_taken = ['PH_1110', 'MA_1024', 'MA_2621', 'ECE_2010', 'OIE_2081', 'EN_2225', 'MA_3631', 'BUS_1010', 'PY_1731',
#                  'FIN_1250', 'CS_3043', 'CS_4432', 'MA_1022', 'DS_1010', 'DS_2010',
#                  'MA_2612', 'HU_3910', 'BUS_3020', 'IQP_OFF_CAMPUS', 'WR_1020', 'CS_3431', 'MA_2611', 'MA_2071', 'ID_2050',
#                  'CS_2103', 'MA_2201', 'CS_1000', 'MA_2051', 'MA_1023', 'CS_4341', 'DS_3010', 'WR_2210',
#                  'CS_1101', 'OIE_559', 'MA_1021', 'CS_2223', 'DS_4635', 'CS_4342', 'ECON_1120', 'WR_1011']

#grad courses in this one
 


#, "MA_1022", "MA_1023", "PH_1110", "CH_1010", "ES_2001", "MA_2001", "MA_1010", "MA_1010", "GOV_2315", "CS_2022"]
#"CS_4432", "CS_4445", "MA_4603", "MA_4635", 'MA_2631', 'MA_3233', 'MA_3627', 'MA_3631'
# output will be a txt, do not add .txt to the end
# output name can be basically anything (probably don't use weird symbols....)
if "_BSMS" not in program_keys[0]:
    print(usr.run_model(program_keys, courses_taken, write_output=True, output_name="my_schedule"))
else:
    first_solve = usr.run_model(program_keys, courses_taken, write_output=True, output_name="my_schedule_firstsolve")
    print(first_solve[program_keys[0]])
    double_counts = first_solve[program_keys[0]]["Double Counting "]
    grad_credits = first_solve[program_keys[0]]["Total MS Credits Req"]

    grad_courses = []
    #undergrad_courses = []
    #courses_taken_copy = courses_taken.copy()

    # figure out what you've already taken - split taken grad and taken undergrad
    for course in grad_credits:
        if course[0] != '[':
            grad_courses.append(course)
    undergrad_courses = [course for course in courses_taken if course not in grad_courses]

    #
    for course in double_counts:
        if course[0] == '[':
            #courses_taken_copy.append(course.strip('[').strip(']'))
            undergrad_courses.append(course.split(' OR ')[0].split(', ')[0].strip('[').strip(']').replace(' ', '_'))
        #grad_courses.append(course.strip('[').strip(']'))
        grad_courses.append(course.split(' OR ')[0].split(', ')[0].strip('[').strip(']').replace(' ', '_'))

    ug_program = program_keys[0].split('_')[0]+'_MAJOR'
    g_program = program_keys[0].split('_')[1]+'_MASTER'

    print("UG PROGRAM: "+str(ug_program))
    print("UG COURSES: "+str(undergrad_courses))

    ug_solve = usr.run_model([ug_program], undergrad_courses, write_output=True, output_name="ug_solve")
    print(ug_solve)
