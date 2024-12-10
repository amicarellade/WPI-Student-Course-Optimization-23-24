from itertools import tee


def parse_template(text):
    data = {}
    current_section = None
    current_category = None
    current_requirement_area = None
    current_requirement_course = None

    lines1, lines2 = tee(text.splitlines(), 2)

    # Advance the second iterator by one step
    next(lines2, None)

    for current_line, next_line in zip(lines1, lines2):
        current_line = current_line.strip()
        next_line = next_line.strip()

        if current_line.startswith("_") or "No Unused Courses" in current_line:
            continue

        # Skip empty lines
        if not current_line:
            print("Skipping empty line")
            continue

        # Detect section headers
        if current_line.startswith("<<<<") and not (("Credits" in current_line) or ("Run Time" in current_line)):
            print(f"Detected Section Header: {current_line}")
            current_section = current_line.strip("<>")
            data[current_section] = {}
            current_category = None
            current_requirement_area = None
            current_requirement_course = None

        #Detect Requirement Category headers
        if next_line.startswith("_"):
            print(f"Detected Requirement Category Header: {current_line}")
            current_category = current_line
            data[current_section][current_category] = {}
            current_requirement_area = None
            current_requirement_course = None
            
        #Detect Requirement Area headers
        elif next_line.startswith("-") and current_category:
            print(f"Detected Requirement Area Header: {current_line}")
            current_requirement_area = current_line
            data[current_section][current_category][current_requirement_area] = []
            current_requirement_course = None

        #Detect Requirement Course headers
        #courses are like this [course, true/false]
        # if line contains "[" then add False
        # if line not contains then add True
        elif current_requirement_area and not "-" in current_line:
            print(f"Detected Requirement Course: {current_line}")
            if "[" in current_line:
                current_requirement_course = [current_line.strip("[]"), False]
            else:
                current_requirement_course = [current_line, True]
            data[current_section][current_category][current_requirement_area].append(current_requirement_course)




        # Detect subsection titles (not just dashes)
        # elif line and not line.startswith("-") and not line.startswith("[") and not ("Stage" in line) and not (line[0].isdigit() and ("Academic Courses" in line or "Free Electives" in line or "Applied" in line or "Excess" in line or "MQP" in line or "PE" in line)) and current_section:
        #     print(f"Detected Subsection Title: {line}")
        #     current_subsection = line
        #     data[current_section][current_category][current_subsection] = []
        #     current_list = data[current_section][current_subsection]

        # # Detect dashed separators
        # elif line.startswith("-") and line.endswith("-"):
        #     print(f"Detected Separator: {line}")
        #     # Do nothing, just ignore separators for better parsing

        # # Detect items in a subsection
        # elif current_section and current_subsection:
        #     if line.startswith("[") and line.endswith("]"):
        #         print(f"Detected List Item: {line}")
        #         current_list.append(line.strip("[]"))
        #     elif "Stage" in line:
        #         print(f"Detected Stage: {line}")
        #         current_list.append(line.strip("{}"))
        #     elif ":" in line:
        #         print(f"Detected Key-Value Pair: {line}")
        #         key, value = map(str.strip, line.split(":", 1))
        #         current_list.append({key: value})
        #     elif line.replace('.', '', 1).isdigit():
        #         print(f"Detected Numeric Value: {line}")
        #         current_list.append(float(line))
        #     else:
        #         print(f"Detected Plain Text: {line}")
        #         current_list.append(line)

    return data


# Example usage:
template_text = """
<<<<<<<<<<< Credits >>>>>>>>>>>>>

135 TOTAL
-------------------------------
135 REMAINING 
    61 Academic Courses 
    0.5 Free Electives 
    9.0 MQP 
    3.0 PE
 
0.0 TAKEN
    0 Applied
    0 Excess


<<<<<<<<<<<<< Run Time >>>>>>>>>>>>>

TOTAL RUN TIME: 0.8254401000449434
----------------------------------------
    Stage I solve: 0.4060478210449219
    Stage II solve: 0.10938310623168945


<<<<<<<<<<<<< Tracking Sheet >>>>>>>>>>>>>
[Brackets indicate courses that have yet to be taken] 
 
General Education and Projects
____________________________________
 
MQP
----------------------------
    [MQP]
    [MQP]
    [MQP]

Physical Education
----------------------------
    [PE]
    [PE]
    [PE]
    [PE]

Humanities
----------------------------
    [HU 3900 or 3910]
    [Humanities]
    [Humanities]
    [Humanities]
    [Humanities]
    [Humanities]
"""

# parsed_data = parse_template(template_text)


# # use text.txt file to test
# with open('test.txt', 'r') as file:
#     template_text = file.read()

# parsed_data = parse_template(template_text)
# print(parsed_data)



# parsed_data = parse_template(template_text)
# print(parsed_data)
# for section in parsed_data:
#     print(section)
#     for subsection in parsed_data[section]:
#         print(f"  {subsection}")
#         for item in parsed_data[section][subsection]:
#             print(f"    {item}")


def divide_dict(input_dict):
    # Keys to include in the first dictionary (Credits, Run Time)
    keys_to_include = ['Credits', 'TOTAL', 'REMAINING', 'TAKEN', 'Applied', 'Excess', 'Run Time', 'TOTAL RUN TIME', 'Stage I solve', 'Stage II solve']
    
    dict_1 = {}
    dict_2 = {}

    # Iterate over the top-level keys in the input dictionary
    for key, value in input_dict.items():
        # If the key matches one of the 'keys_to_include', add to dict_1
        if key.strip() in keys_to_include:
            dict_1[key] = value
        else:
                dict_2 = input_dict[' Tracking Sheet ']

    return dict_1, dict_2

# # Example usage
# input_dict = {
#     'Algorithms': ['[CS 2223]'],
#     'Business Analysis ': ['[BUS_2080 OR OIE_2081]'],
#     'Core': ['[DS 1010]', '[DS 2010]', '[DS 3010]'],
#     'Computer Science': ['[CS_1004, CS_1101, CS_1102]', '[CS_2102, CS_2103, CS_2119]'],
#     'Disciplinary Electives': ['[4000-Level Disciplinary Electives]', '[4000-Level Disciplinary Electives]', '[Business Modeling and Prediction - MIS_4084, OIE_4430]',
#                                '[Data Access and Management - CS_3431, MIS_3720, CS_4432, CS_4433/DS_4433]', '[Data Mining and Machine Learning - CS_4342, CS_4445]',
#                                '[Disciplinary Electives]', '[Disciplinary Electives]', '[Disciplinary Electives]', '[Disciplinary Electives]', '[Disciplinary Electives]',
#                                '[Disciplinary Electives]', '[Disciplinary Electives]'],
#     'Entrepreneurship and Innovation': ['[Entrepreneurship and Innovation - BUS_1010, ETR_1100, BUS_3010, ETR_3633, OBC_1010, MIS_3010]'],
#     'Linear Algebra': ['[MA_2071 OR MA_2072]'],
#     'Mathematical Sciences': ['[Disciplinary Electives]', '[Disciplinary Electives]'],
#     'Natural or Engineering Sciences': ['[Natural and Engineering Sciences]', '[Natural and Engineering Sciences]'],
#     'Applied Statistics': ['[MA 2611]', '[MA 2612]'],
#     'Credits': '135',
#     'TOTAL': '135',
#     'REMAINING': '114',
#     'TAKEN': '0',
#     'Applied': '0',
#     'Excess': '0',
#     'Run Time': 'TOTAL RUN TIME: 0.3025236999965273',
#     'TOTAL RUN TIME': '0.3025236999965273',
#     'Stage I solve': '0.11654090881347656',
#     'Stage II solve': '0.07163286209106445'
# }

# dict_1, dict_2 = divide_dict(input_dict)
# print("Dict 1:", dict_1)
# print("Dict 2:", dict_2)