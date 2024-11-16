def parse_template(text):
    data = {}
    current_section = None
    current_subsection = None
    current_list = None

    for line in text.splitlines():
        line = line.strip()

        if line.startswith("_"):
            continue

        # Skip empty lines
        if not line:
            print("Skipping empty line")
            continue

        # Detect section headers
        if line.startswith("<<<<"):
            print(f"Detected Section Header: {line}")
            current_section = line.strip("<>")
            data[current_section] = {}
            current_subsection = None
            current_list = None


        # Detect subsection titles (not just dashes)
        elif line and not line.startswith("-") and not line.startswith("[") and not ("Stage" in line) and not (line[0].isdigit() and ("Academic Courses" in line or "Free Electives" in line or "Applied" in line or "Excess" in line or "MQP" in line or "PE" in line)) and current_section:
            print(f"Detected Subsection Title: {line}")
            current_subsection = line
            data[current_section][current_subsection] = []
            current_list = data[current_section][current_subsection]

        # Detect dashed separators
        elif line.startswith("-") and line.endswith("-"):
            print(f"Detected Separator: {line}")
            # Do nothing, just ignore separators for better parsing

        # Detect items in a subsection
        elif current_section and current_subsection:
            if line.startswith("[") and line.endswith("]"):
                print(f"Detected List Item: {line}")
                current_list.append(line.strip("[]"))
            elif "Stage" in line:
                print(f"Detected Stage: {line}")
                current_list.append(line.strip("{}"))
            elif ":" in line:
                print(f"Detected Key-Value Pair: {line}")
                key, value = map(str.strip, line.split(":", 1))
                current_list.append({key: value})
            elif line.replace('.', '', 1).isdigit():
                print(f"Detected Numeric Value: {line}")
                current_list.append(float(line))
            else:
                print(f"Detected Plain Text: {line}")
                current_list.append(line)

    return data

# # Example usage:
# template_text = """
# <<<<<<<<<<< Credits >>>>>>>>>>>>>

# 135 TOTAL
# -------------------------------
# 135 REMAINING 
#     61 Academic Courses 
#     0.5 Free Electives 
#     9.0 MQP 
#     3.0 PE
 
# 0.0 TAKEN
#     0 Applied
#     0 Excess


# <<<<<<<<<<<<< Run Time >>>>>>>>>>>>>

# TOTAL RUN TIME: 0.8254401000449434
# ----------------------------------------
#     Stage I solve: 0.4060478210449219
#     Stage II solve: 0.10938310623168945


# <<<<<<<<<<<<< Tracking Sheet >>>>>>>>>>>>>
# [Brackets indicate courses that have yet to be taken] 
 
# General Education and Projects
# ____________________________________
 
# MQP
# ----------------------------
#     [MQP]
#     [MQP]
#     [MQP]

# Physical Education
# ----------------------------
#     [PE]
#     [PE]
#     [PE]
#     [PE]

# Humanities
# ----------------------------
#     [HU 3900 or 3910]
#     [Humanities]
#     [Humanities]
#     [Humanities]
#     [Humanities]
#     [Humanities]
# """

# parsed_data = parse_template(template_text)
# print(parsed_data)
# for section in parsed_data:
#     print(section)
#     for subsection in parsed_data[section]:
#         print(f"  {subsection}")
#         for item in parsed_data[section][subsection]:
#             print(f"    {item}")
