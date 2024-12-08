import setup_model as sm
#import process_solution_masters as ps
import write_solution as ws
import basic_data_funcs as bd
import time as t


def run_model(program_keys, courses_taken, programs_ref_path = "Default", config_path= "config.json", write_output=False, output_name= "solve", write_LP=False, ISPs = None):

    if "_MASTER" in program_keys[0]:
        import process_solution_masters as ps
    elif "_BSMS" in program_keys[0]:
        import process_solution_bsms as ps
    else:
        import process_solution as ps
    config_file = bd.get_dict_from_json(config_path)
    if programs_ref_path == "Default":
        programs_ref_path = config_file["PROGRAM_REF_PATH"]
    T_START = t.perf_counter()
    programs_ref = bd.get_dict_from_json(programs_ref_path).copy()
    base_dict = programs_ref[sm.get_program_run_name(program_keys)].copy()
    if ISPs != None:
        for isp in ISPs:
            print(isp["sreqs"])
            print("WHAT THE FLIP!!")
            if isp['substitution'] != '':
                print("THIS IS WHAT WE HAVE FOR ISP SUB: "+str(isp['substitution']))
                courses_taken.append(isp['substitution'])
            else:
                print("THIS IS TRUE!!!! I WANT TO GO TO BED LOLOL")
                if isp["req"] != "None":
                    print(isp['req'])
                    print("THIS IS ALSO TRUE!!!! WAHOOOOOO")
                    #print(eval(isp["req"])[0].split("_")[0]+"_MAJOR")
                    try:
                        base_dict[eval(isp["req"])[0].split("_")[0]+"_MAJOR"]["Reqs"][eval(isp["req"])[0]]["Credits"] -= eval(isp["credits"])
                        if base_dict[eval(isp["req"])[0].split("_")[0] + "_MAJOR"]["Reqs"][eval(isp["req"])[0]][
                            "Credits"] <= 0:
                            del base_dict[eval(isp["req"])[0].split("_")[0] + "_MAJOR"]["Reqs"][eval(isp["req"])[0]]
                    except KeyError:
                        #this has already been deleted - we're good
                        pass
                if isp["sreqs"] != []:
                    for sreq in isp["sreqs"]:
                        #print(eval(isp[sreq])[0])
                        try:
                            base_dict[eval(sreq)[0].split("_")[0]+"_MAJOR"]["Sreqs"][eval(sreq)[0]]["Credits"] -= eval(isp["credits"])
                            if base_dict[eval(sreq)[0].split("_")[0]+"_MAJOR"]["Sreqs"][eval(sreq)[0]]["Credits"] <= 0:
                                base_dict[eval(sreq)[0].split("_")[0]+"_MAJOR"]["Sreqs"][eval(sreq)[0]]["Credits"] = 0
                        except KeyError:
                            pass

    courses_taken_result = sm.setup_courses_taken(courses_taken, base_dict["Buckets"])
    courses_taken_dict = courses_taken_result["Taken Ref"]
    credits_taken = courses_taken_result["Credits Taken"]

    vars_dict = sm.run_model(program_keys, courses_taken_dict, base_dict, output_name, write_LP= write_LP)
    added_credits = vars_dict["Objectives"]["Stage I"]
    print("VARS DICT: " + str(vars_dict))
    applied = ps.format_solution(vars_dict["X"], vars_dict["Y"], base_dict, program_keys, courses_taken_dict, ISPs)

    #NEW PRINT STATEMENT 
    print("APPLIED")
    print("!!!!!!!")
    print("@@@@@@@")
    print("#######")
    print("$$$$$$")
    print("&&&&&&&")
    print(applied)
    print("        ")
    print("       ")

    results = applied["Results"]
    new_counts = applied["Credit Counts"]
    print("APPLIED: "+str(applied))
    counts_dict = ps.calc_credit_metrics(added_credits, credits_taken, new_counts["Credits Used"], program_keys)
    
    T_FINISH = t.perf_counter()
    solve_times = vars_dict["Solve Times"]
    run_times = {"Stage I Solve": solve_times["Stage I"], "Stage II Solve": solve_times["Stage II"], "Entire Run Total": T_FINISH - T_START}

    print("Run Complete!")
    if write_output:
        ws.write_output_file(output_name, results, program_keys, run_times, counts_dict, config_file["MAJOR_NAMES"])
    
    return results