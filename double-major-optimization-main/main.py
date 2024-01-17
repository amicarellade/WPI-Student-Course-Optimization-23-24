import user_functions as usr

file_upload_mode = False

# program keys input: a list containing either "MATH_MAJOR", "OIE_MAJOR", or both
program_keys = ['DS_MAJOR']

# must be in the format DEPT_NUM, ex "OIE_2081"
# program does not check for course validity, unrecognized courses assumed to be 3 credits
courses_taken = ["CS_1101", "CS_1102"]#, "MA_1022", "MA_1023", "PH_1110", "CH_1010", "ES_2001", "MA_2001", "MA_1010", "MA_1010", "GOV_2315", "CS_2022"]
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

    for course in grad_credits:
        if course[0] != '[':
            grad_courses.append(course)
    undergrad_courses = [course for course in courses_taken if course not in grad_courses]

    for course in double_counts:
        if course[0] == '[':
            #courses_taken_copy.append(course.strip('[').strip(']'))
            undergrad_courses.append(course.split(' OR ')[0].split(', ')[0].strip('[').strip(']').replace(' ', '_'))
        grad_courses.append(course.strip('[').strip(']'))

    ug_program = program_keys[0].split('_')[0]+'_MAJOR'
    g_program = program_keys[0].split('_')[1]+'_MASTER'

    print("UG PROGRAM: "+str(ug_program))
    print("UG COURSES: "+str(undergrad_courses))

    ug_solve = usr.run_model([ug_program], undergrad_courses, write_output=True, output_name="ug_solve")
    print(ug_solve)
