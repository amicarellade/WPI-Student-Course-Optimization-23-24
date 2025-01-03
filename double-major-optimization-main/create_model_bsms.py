import math

from pulp import *


def setup_x_y_vars(model, base_dict, program_keys, taken_courses):
    gen_ed = base_dict["ALL_MAJORS"]
    applies_to_gen_ed = []
    x = {}
    y = {}
    z = {}
    print("BASE DICT BUCKETS WAHOO: "+str(base_dict["Buckets"]))
    print("THE COURSES YOU HAVE TAKEN ARE HERE! YIPPEE!! "+str(taken_courses))
    for buck_key, buck_attrs in base_dict["Buckets"].items():
        buck_count = buck_attrs["Bucket Size"]
        num_taken = taken_courses[buck_key]["Taken"]
        y[buck_key] = LpVariable(lowBound=0.0, upBound=buck_count - num_taken, cat='Integer',
                                 name='y(' + str(buck_key) + ')')
        all_applic_reqs = buck_attrs["Req Keys"]

        gen_rel_reqs = []
        for each_req in all_applic_reqs:
            if each_req in base_dict["ALL_MAJORS"]["Reqs"].keys():
                gen_rel_reqs.append(each_req)
                x[(buck_key, each_req)] = LpVariable(lowBound=0.0, upBound=buck_count, cat='Integer',
                                                     name='x(' + str(buck_key) + ')(' + str(each_req) + ')')
        for each_req in all_applic_reqs:
            if each_req in base_dict["ALL_MAJORS"]["Reqs"].keys():
                #gen_rel_reqs.append(each_req)
                z[(each_req)] = LpVariable(lowBound = 0.0, cat = 'LpContinuous', name='z('+str(each_req)+')')

        prog_counter = 0
        for prog_key in program_keys:
            prog_counter += 1
            prog_name = prog_key[:-6]

            relevant_reqs = []
            for each_req in buck_attrs["Req Keys"]:
                if each_req in base_dict[prog_key]["Reqs"].keys():
                    relevant_reqs.append(each_req)
                    x[(buck_key, each_req)] = LpVariable(lowBound=0.0, upBound=buck_count, cat='Integer',
                                                         name='x(' + str(buck_key) + ')(' + str(each_req) + ')')
            for each_req in buck_attrs["Req Keys"]:
                if each_req in base_dict[prog_key]["Reqs"].keys():
                    # relevant_reqs.append(each_req)
                    z[(each_req)] = LpVariable(lowBound=0.0, cat='LpContinuous', name='z(' + str(each_req) + ')')

            total_rel_reqs = relevant_reqs + gen_rel_reqs
            if len(total_rel_reqs) > 0:
                model += lpSum(x[(buck_key, r)] for r in total_rel_reqs) <= y[buck_key] + taken_courses[buck_key][
                    "Taken"], 'setY%s(%s)' % (str(prog_counter), buck_key)

    vars_dict = {"X": x, "Y": y, "Z":z}
    return vars_dict


def add_requirement_constraints(model, x, z, program_keys, base_dict, taken_courses):
    buckets_dict = base_dict["Buckets"]
    for prog_key in program_keys:
        for each_req in base_dict[prog_key]["Reqs"].keys():
            min_creds = base_dict[prog_key]["Reqs"][each_req]["Credits"]
            applic_buckets = base_dict[prog_key]["Reqs"][each_req]["Buckets"]
            model += lpSum(
                buckets_dict[b]["Credits Each"] * x[b, each_req] for b in applic_buckets) - z[each_req] == min_creds, 'reqMin(%s)' % (
                         each_req)

    for each_req in base_dict["ALL_MAJORS"]["Reqs"].keys():
        min_creds = base_dict["ALL_MAJORS"]["Reqs"][each_req]["Credits"]
        applic_buckets = base_dict["ALL_MAJORS"]["Reqs"][each_req]["Buckets"]
        model += lpSum(
            buckets_dict[b]["Credits Each"] * x[b, each_req] for b in applic_buckets) - z[each_req] == min_creds, 'reqMin(%s)' % (
                     each_req)
    #model += lpSum(0.00001 * ecks for ecks in x.values() if "DS_DOUBLE" in str(ecks))
    #print(taken_courses["1000_CS"]["Taken"])
    model += lpSum(x[b, program_keys[0].split("_")[0]+"_DOUBLE"] * base_dict["Buckets"][b]["Credits Each"] * math.ceil(taken_courses[b]["Taken"]/(taken_courses[b]["Taken"]+1)) for b in base_dict["Buckets"] if program_keys[0].split("_")[0]+"_DOUBLE" in base_dict["Buckets"][b]["Req Keys"]) <= 18, 'MAXIMIZE DOUBLE COUNTS'
    return model


def add_sreqs(model, x, program_keys, base_dict):
    track_SRs = {}
    for prog_key in program_keys:
        for sreq_key, sreq_attr in base_dict[prog_key]["Sreqs"].items():
            num_sublists = sreq_attr["Sublists Count"]

            if num_sublists == 0:
                applic_buckets = base_dict[prog_key]["Sreqs"][sreq_key]["Buckets"]
                sreqs_type1(model, x, sreq_key, sreq_attr, applic_buckets, base_dict["Buckets"])
            else:
                list_of_lobs = base_dict[prog_key]["Sreqs"][sreq_key]["Buckets"]
                sreqs_type2(model, x, sreq_key, sreq_attr, list_of_lobs, base_dict["Buckets"], track_SRs)

    for sreq_key, sreq_attr in base_dict["ALL_MAJORS"]["Sreqs"].items():
        num_sublists = sreq_attr["Sublists Count"]
        if num_sublists == 0:
            applic_buckets = base_dict["ALL_MAJORS"]["Sreqs"][sreq_key]["Buckets"]
            sreqs_type1(model, x, sreq_key, sreq_attr, applic_buckets, base_dict["Buckets"])

        else:
            list_of_lobs = base_dict["ALL_MAJORS"]["Sreqs"][sreq_key]["Buckets"]
            sreqs_type2(model, x, sreq_key, sreq_attr, list_of_lobs, base_dict["Buckets"], track_SRs)

    return track_SRs


def sreqs_type1(model, x, sreq_key, sreq_attr, applic_buckets, buckets_dict):
    applic_reqs = sreq_attr["Applicable Reqs"]
    num_credits = sreq_attr["Credits"]

    reqs_per_bucket = {}
    for bucket in applic_buckets:
        reqs_per_bucket[bucket] = []
        for req in applic_reqs:
            if req in buckets_dict[bucket]["Req Keys"]:
                reqs_per_bucket[bucket].append(req)

    direct_const = 1
    if sreq_attr["Sreq Type"] == "1b":
        direct_const = -1

    model += lpSum(direct_const * buckets_dict[b]["Credits Each"] * x[b, r] for b in applic_buckets for r in
                   reqs_per_bucket[b]) >= direct_const * num_credits, 'SR(%s)' % (sreq_key)

    return model


def sreqs_type2(model, x, sreq_key, sreq_attr, list_of_lobs, buckets_dict, track_SRs):
    corr_factor = 0.1
    num_credits = sreq_attr["Credits"]
    applic_req = sreq_attr["Applicable Reqs"][0]
    num_sublists = sreq_attr["Sublists Count"]
    sublist_index = 0
    for current_sublist in list_of_lobs:
        track_SRs[(sreq_key, sublist_index)] = LpVariable(cat='Binary',
                                                          name='SR2(' + str(sreq_key) + '_' + str(sublist_index) + ')')
        model += lpSum(buckets_dict[b]["Credits Each"] * x[b, applic_req] for b in current_sublist) >= num_credits * \
                 track_SRs[(sreq_key, sublist_index)] - corr_factor, 'SR2(%s)(C%s)' % (sreq_key, str(sublist_index))
        sublist_index += 1

    model += lpSum(track_SRs[(sreq_key, i)] for i in range(num_sublists)) >= 1, 'SR2_total(%s)' % sreq_key

    return track_SRs


def set_objective(model, x, y, z, buckets_dict, model_stage, program_keys, taken_courses, max_credits=0):
    print("HERE IS THE BUCKETS DICT: "+str(buckets_dict))
    #print("HERE ARE THE TAKEN COURSES: "+str(taken_courses))
    if model_stage == 1:
        #DOESNT WORK - x includes taken AND not taken, so it has no incentive to place a taken course there (as written).
        #model += lpSum(buckets_dict[b]["Credits Each"] * y[b] for b in buckets_dict.keys()) + lpSum(0.01 * zee for zee in z.values()) - lpSum(0.00001 * ecks for ecks in x.values() if "DS_DOUBLE" in str(ecks))
        model += lpSum(buckets_dict[b]["Credits Each"] * y[b] for b in buckets_dict.keys()) + lpSum(
            0.01 * zee for zee in z.values()) - lpSum(1e-5 * x[b, program_keys[0].split("_")[0]+"_DOUBLE"] * buckets_dict[b]["Credits Each"] * math.ceil(taken_courses[b]["Taken"]/(taken_courses[b]["Taken"]+1)) for b in buckets_dict.keys() if program_keys[0].split("_")[0]+"_DOUBLE" in buckets_dict[b]["Req Keys"])


    elif model_stage == 2:
        model += lpSum(-1 * buckets_dict[b]["Choice Weight"] * y[b] for b in buckets_dict.keys())
        model += lpSum(buckets_dict[b]["Credits Each"] * y[b] for b in buckets_dict.keys()) + lpSum(
            0.01 * zee for zee in z.values()) - lpSum(1e-5 * x[b, program_keys[0].split("_")[0]+"_DOUBLE"] * buckets_dict[b]["Credits Each"] * math.ceil(taken_courses[b]["Taken"]/(taken_courses[b]["Taken"]+1)) for b in buckets_dict.keys() if program_keys[0].split("_")[0]+"_DOUBLE" in buckets_dict[b]["Req Keys"]) == max_credits, 'credMax' #- lpSum(0.00001 * ecks for ecks in x.values() if "DS_DOUBLE" in str(ecks)) == max_credits, 'credMax'

    return model