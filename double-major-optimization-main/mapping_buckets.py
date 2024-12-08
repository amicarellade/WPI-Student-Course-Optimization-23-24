import json
import basic_data_funcs as bd

# # Example JSON data and dictionary

# course_dict = {' Tracking Sheet ': {'General Education and Projects': {'MQP': [['MQP', False], ['MQP', False], ['MQP', False], ['MQP', False]], 'Physical Education': [['PE', False], ['PE', False], ['PE', False], ['PE', False]], 'Humanities': [['HU_3900 OR HU_3910', False], ['Humanities', False], ['Humanities', False], ['Humanities', False], ['Humanities', False], ['Humanities', False]], 'IQP': [['IQP Off Campus', False]], 'Social Science': [['ID_2050', False], ['Social Science', False]], 'Free Electives': [], 'Not used': []}, 'Computer Science': {'CS Core': [['CS 2223', False], ['CS 4342', False], ['CS 4445', False], ['CS Grad Level Electives', False], ['CS Grad Level Electives', False], ['CS_1101, CS_1102', False], ['CS_2102, CS_2103', False], ['CS_3043', False], ['CS_3133', False], ['Grad CS', False]], 'General Math': [['4000 Level Math Disciplinary Electives', False], ['4000 Level Math Disciplinary Electives', False], ['4000 Level Math Disciplinary Electives', False], ['MA 2611', False], ['MA_2071 OR MA_2072', False]], 'General Science': [['Biology', False], ['Biology', False], ['Biology', False]], 'Probability': [], 'Science/Engineering Electives': [['Natural and Engineering Sciences', False], ['Natural and Engineering Sciences', False]], 'Statistics': [['MA 2612', False]]}, 'Data Science': {'Algorithms': [['CS 2223', False]], 'Business Analysis': [['BUS_2080 OR OIE_2081', False]], 'Core': [['DS 1010', False], ['DS 2010', False], ['DS 3010', False]], 'Computer Science': [['CS_1101, CS_1102', False], ['CS_2102, CS_2103', False]], 'Disciplinary Electives': [['4000 Level Math Disciplinary Electives', False], ['CS 4342', False], ['CS 4445', False], ['CS Grad Level Electives', False], ['CS Grad Level Electives', False], ['CS_3043', False], ['CS_3133', False]], 'Entrepreneurship and Innovation': [], 'Linear Algebra': [['MA_2071 OR MA_2072', False]], 'Mathematical Sciences': [['4000 Level Math Disciplinary Electives', False], ['4000 Level Math Disciplinary Electives', False]], 'Natural or Engineering Sciences': [['Biology', False], ['Biology', False]], 'Applied Statistics': [['MA 2611', False], ['MA 2612', False]]}}}  # Replace with your actual JSON
# programs_ref = bd.get_dict_from_json("Data/JSONs/programs_ref.json")
# json_data = programs_ref["CS_DS_DOUBLE"]
# # print (json_data)

# # Create a mapping of buckets to their courses
# bucket_mapping = {
#     details["Bucket Description"]: details["Bucket Contents"]
#     for bucket, details in json_data["Buckets"].items()
# }

# print (bucket_mapping)
# Function to update the dictionary
def augment_courses_with_buckets(course_dict, json_data):
    bucket_mapping = {
        details["Bucket Description"]: details["Bucket Contents"]
        for bucket, details in json_data["Buckets"].items()
    }
    for subcategories in course_dict.values():
        for requirement_area in subcategories.values():
            for courses in requirement_area.values():
                for i, course in enumerate(courses):
                    print("wordking")
                    if course[0] in bucket_mapping:
                        # Append the bucket's courses
                        print ("appending bucket courses")
                        courses[i] = [course[0], course[1], bucket_mapping[course[0]]]
    return course_dict

# # Augment the course dictionary
# augmented_course_dict = augment_courses_with_buckets(course_dict, bucket_mapping)

# # Output the result
# print(json.dumps(augmented_course_dict, indent=4))


