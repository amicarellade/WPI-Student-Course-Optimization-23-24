import user_functions as usr

#file_upload_mode = False

# program keys input: a list containing either "MATH_MAJOR", "OIE_MAJOR", or both
# program_keys = ['MATH_MAJOR', 'OIE_MAJOR']
program_keys = ['DS_DS_BSMS']

# must be in the format DEPT_NUM, ex "OIE_2081"
# program does not check for course validity, unrecognized courses assumed to be 3 credits
#courses_taken = ['MA_1021', 'DS_3010', 'ENV_130X', 'PH_1110', 'DS_1010', 'SP_1524', 'DS_2010', 'ETR_1100', 'BUS_2080', 'CS_2102', 'MA_1023', 'ES_1020', 'CS_2022', 'CS_2223', 'HU_3900', 'MA_2611', 'MA_1024', 'WR_1010', 'MA_2621', 'PY_2731', 'WR_253X', 'WR_3210', 'MA_1022', 'MA_2071', 'CS_1101']

#no grad here!

# **** NO TAKEN DCS ****
# courses_taken = ['PH_1110', 'MA_1024', 'MA_2621', 'ECE_2010', 'OIE_2081', 'EN_2225', 'MA_3631', 'BUS_1010', 'PY_1731',
#                  'FIN_1250', 'CS_3043',  'MA_1022', 'DS_1010', 'DS_2010',
#                  'MA_2612', 'HU_3910', 'BUS_3020', 'IQP_OFF_CAMPUS', 'WR_1020', 'CS_3431', 'MA_2611', 'MA_2071', 'ID_2050',
#                  'CS_2103', 'MA_2201',  'MA_2051', 'MA_1023',  'DS_3010', 'WR_2210',
#                  'CS_1101', 'MA_1021', 'CS_2223',   'ECON_1120', 'WR_1011',  'CS_1000', 'CS_584', 'MA_2073', 'MA_2431', 'MA_1033', 'MA_3231', 'MA_3233', 'MA_3627']#, 'PH_1111', 'PH_1121', 'PH_2101', "MA_4213", "MA_4214", "MA_4222", "MA_4235", "MA_4237", "MA_4631", "MA_4632"]

courses_taken = ['PH_1110', 'MA_1024', 'MA_2621', 'ECE_2010', 'OIE_2081', 'EN_2225', 'MA_3631', 'BUS_1010', 'PY_1731',
                 'FIN_1250', 'CS_3043',  'MA_1022', 'DS_1010', 'DS_2010',
                 'MA_2612', 'HU_3910', 'BUS_3020', 'IQP_OFF_CAMPUS', 'WR_1020', 'CS_3431', 'MA_2611', 'MA_2071', 'ID_2050',
                 'CS_2103', 'MA_2201',  'MA_2051', 'MA_1023',  'DS_3010', 'WR_2210',
                 'CS_1101', 'MA_1021', 'CS_2223',   'ECON_1120', 'WR_1011',  'CS_1000', 'CS_584',
                 'MIS_4084',  'CS_4432', 'CS_4342']

#'CS_4341', 'MA_3233', 'MA_1033', 'MA_3231', 'MA_3627', 'MA_2073', 'MA_2431', 'CS_4445', 'DS_4635',
    # 'CS_4804', 'MIS_4084',
#'CS_547', 'DS_551', 'DS_598',
#grad courses in this one
# courses_taken = ['PH_1110', 'MA_1024', 'MA_2621', 'ECE_2010', 'OIE_2081', 'EN_2225', 'MA_3631', 'BUS_1010', 'PY_1731',
#                  'FIN_1250',  'CS_3043', 'CS_4432', 'MA_1022', 'DS_1010', 'DS_2010', 'DS_504',
#                  'MA_2612', 'HU_3910', 'BUS_3020', 'IQP_OFF_CAMPUS', 'WR_1020', 'CS_3431', 'MA_2611', 'MA_2071', 'ID_2050',
#                    'CS_2103', 'MA_2201', 'CS_1000', 'MA_2051', 'MA_1023', 'CS_4341', 'DS_3010', 'WR_2210',
#                  'CS_1101',  'MA_1021', 'CS_2223', 'DS_4635',  'ECON_1120', 'WR_1011', 'DS_503', 'CS_4342', 'CS_541'] #'

#courses_taken  = ['CS_4445', 'CS_4341', 'CS_4342', 'DS_4635', 'CS_541']

#from jen
# courses_taken = ['PH_1110', 'MA_1024', 'MA_2621', 'ECE_2010', 'OIE_2081', 'EN_2225', 'MA_3631', 'BUS_1010', 'PY_1731',
#                  'FIN_1250','CS_3043', 'CS_4432', 'MA_1022', 'DS_1010', 'DS_2010', 'MA_2612', 'HU_3910', 'WR_1020', 'CS_3431',
#                  'MA_2611', 'MA_2071', 'ID_2050', 'CS_2103', 'MA_2201', 'MA_2051', 'MA_1023', 'CS_4341', 'DS_3010', 'WR_2210',
#                  'CS_1101', 'MA_1021', 'CS_2223', 'DS_4635', 'ECON_1120', 'WR_1011', "CS_4342", "MIS_3720"]

#kendall
# courses_taken = ['MA_1020', 'CS_4341', 'MA_2621', 'MIS_4084', 'CS_2223', 'DS_3010', 'DS_4635', 'MIS_4720', 'EN_1000', 'CS_4445',
#                  'CS_3043', 'SP_3521', 'CS_4433', 'MA_2612', 'PH_1110', 'MIS_3720', 'MKT_3650', 'OIE_3460', 'GE_2341', 'MA_1120',
#                  'SP_2522', 'ECON_1110', 'SP_2521', 'DS_1010', 'DS_2010', 'ID_2050', 'PSY_1400', 'CS_2102', 'BUS_2080', 'ETR_1100',
#                  'CS_3431', 'MA_2611', 'SP_1523', 'SP_3522', 'CS_1101', 'CS_4804', 'IQP_OFF_CAMPUS']#, 'GOV_2314', 'MA_2071', 'SP_3532']

#courses_taken = ["DS_1010"]
#, "MA_1022", "MA_1023", "PH_1110", "CH_1010", "ES_2001", "MA_2001", "MA_1010", "MA_1010", "GOV_2315", "CS_2022"]
#"CS_4432", "CS_4445", "MA_4603", "MA_4635", 'MA_2631', 'MA_3233', 'MA_3627', 'MA_3631'
# output will be a txt, do not add .txt to the end
# output name can be basically anything (probably don't use weird symbols....)
if "_BSMS" not in program_keys[0]:
    print(usr.run_model(program_keys, courses_taken, write_output=True, output_name="my_schedule"))
else:
    first_solve = usr.run_model(program_keys, courses_taken, write_output=True, output_name="my_schedule_firstsolve")
    print(first_solve[program_keys[0]])

    num_unused_firstsolve = len(first_solve["ALL_MAJORS"]["Not used"])
    nottaken_doubles = [course for course in first_solve[program_keys[0]]["Double Counting "] if course[0] == '[']
    num_nottaken_doubles = len(nottaken_doubles)

    double_counts = first_solve[program_keys[0]]["Double Counting "]
    grad_credits = first_solve[program_keys[0]]["Total MS Credits Req"]

    grad_courses = []
    #undergrad_courses = []
    #courses_taken_copy = courses_taken.copy()

    # figure out what you've already taken - split taken grad and taken undergrad
    for course in grad_credits:
        if course[0] != '[':
            grad_courses.append(course.split(' OR ')[0].split(', ')[0].replace(' ', '_'))
    undergrad_courses = [course for course in courses_taken if course not in grad_courses]

    #named as such because it is a list of the actually taken UG courses, not the recs we are treating as taken
    actually_takens = [course for course in courses_taken if course not in grad_courses]

    # append all untaken DC courses to UG courses, and then append all DC courses to grad.
    # why do these differently? because the UG course list already contains the taken DC courses from the line above,
    # but the G course list doesn't
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

    int_ug_solve = usr.run_model([ug_program], actually_takens, write_output=True, output_name="int_ug_solve_test")

    num_unused_int_ugsolve = len(int_ug_solve["ALL_MAJORS"]["Not used"])

    if (num_unused_firstsolve - num_unused_int_ugsolve) == 0:
        pass
        # step 1: get the X's that i'm interested in, and the taken flags for their respective buckets
        # step 2: make new constraints
        #we could potentially double-count more
    else:
        #our taken double-counts pushed some taken stuff out
        #resolve making sure DCs appear as taken?
        pass

'''
    # solve only undergrad to compare to first solve - looking for difference in unused courses to see if
    # optimal double-counting is possible (without increasing number of unused courses)
    ug_solve = usr.run_model([ug_program], undergrad_courses, write_output=True, output_name="ug_solve")
    print(ug_solve)

    num_unused_ugsolve = len(ug_solve["ALL_MAJORS"]["Not used"])

    # if moving the double-counted courses back into the normal UG schedule causes more courses to become unused than before,
    # optimal double-counting is not possible, and we need to adjust our recommendation of which/how many courses to double count.

    # if the already taken double-counts are causing courses to become unused, there's nothing we can do in this case - all the courses
    # in question are already taken (i.e. those courses would be unused in a completely normal, non-BSMS solve of the UG schedule anyways).
    # we DELETE the future double counts - see below
    # we want the double-counts to appear as used in the schedule over the other courses.

    # if the future double-counts we're recommending (i.e. the courses in the double counting section that haven't been taken yet)
    # are causing already taken courses to become not used, WE'VE DECIDED that this is bad, and that we need to eliminate
    # some (or all) of these courses.
        # an alternative option is to allow users to take these courses regardless - this effectively would have no impact
        # on their undergrad degree (since the 3 credits they're earning from that course are bumping out 3 credits they already
        # had applied to the degree), but since they're not yet maximally double-counting, they will advance their grad
        # degree by 2 credits. WE'VE DECIDED that it's better for students to just start taking grad classes (to earn 3 credits
        # vs 2), although since in one semester's worth of time a student could earn 4 credits (with two double counts) instead
        # of 3, we might want to give the option of taking double-countable courses for no additional undergraduate benefit
        # to the user

    # if the number of not taken double counts is less than or equal to the number of courses that became unused due to
    # putting the double counts back into the UG solve, the fix is easy: delete all the future double counts
    # (i.e. concede that optimal double-counting isn't possible in this case), and keep the already taken double-counts
    # (see second comment in this section)

    #BUG: should be by credits
    if (num_unused_ugsolve - num_unused_firstsolve) >= num_nottaken_doubles:
        for course in nottaken_doubles:
            undergrad_courses.remove(course.split(' OR ')[0].split(', ')[0].strip('[').strip(']').replace(' ', '_'))
        final_ug_solve = usr.run_model([ug_program], undergrad_courses, write_output=True, output_name="final_ug_solve")

    # if the number of not taken double counts is greater than the number of courses that become unused, we only need to
    # remove SOME of those courses
    #
    # WRONG (choice weights only apply to y's):
    # - i think we can do this with choice weights. if we have our optimal ordering in place
    # for which courses are the best for double counting*, we can set all of the non-double-countable courses to have higher
    # choice weights than all the DC-able courses (so that the model chooses as few DC's to apply as possible), but we keep the
    # relative order of the courses intact
        # might this fiddling with the choice weights have unintended effects on the model in terms of filling in the other
        # (non-DC) reqs and sreqs? does this break the above thing where if there are already taken DCs causing courses to
        # become not used (second comment block in this section), we want the double-counts to appear and have
            # *this methodology will be documented somewhere - essentially we rank courses based on which/how many sreqs they
            # fill between both degrees, how many other options there are in both degrees to fill those requirements, etc
    else:
        intermediate_ug_solve = usr.run_model([ug_program], actually_takens, write_output=True, output_name="int_ug_solve_test")
'''