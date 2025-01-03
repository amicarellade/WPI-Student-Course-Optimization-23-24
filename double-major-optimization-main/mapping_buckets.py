import json
import basic_data_funcs as bd

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




import csv
import json

def csv_to_custom_json(file_path):
    result = {"courses": []}
    
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        course_dict = {}
        
        for row in reader:
            course_number = row["Course Number"]
            if course_number not in course_dict:
                course_dict[course_number] = {
                    "Course Number": course_number,
                    "Course Name": row["Course Name"].strip(),
                    "average_grade": row["average_grade"],
                    "hours": row["hours"],
                    "Professors": []
                }
            
            # Add professor details to the course
            course_dict[course_number]["Professors"].append({
                "Professor Name": row["Professor"].strip(),
                "Rating": row["Rating"].strip() if row["Rating"] else None,
                "Would Take Again": row["Would Take Again"].strip() if row["Would Take Again"] else None,
                "Difficulty": row["Difficulty"].strip() if row["Difficulty"] else None,
            })
        
        # Populate the result list
        result["courses"] = list(course_dict.values())
    
    return json.dumps(result, indent=4)

# # Example usage:
# file_path = "Oscar Data/merged_courses.csv"  # Replace with your file path
# json_result = csv_to_custom_json(file_path)


# # Save the JSON result to a file
# result_filename = "Data/Oscar+RP_Ddata/Merged_courses.json"
# with open(result_filename, 'w') as result_file:
#     result_file.write(json_result)

# Merge CSV files
import os
import pandas as pd

def merge_csv_files(input_folder, output_file):
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
    combined_csv = pd.concat([pd.read_csv(os.path.join(input_folder, f)) for f in csv_files])
    combined_csv.to_csv(output_file, index=False)

# # Example usage:
# input_folder = "Oscar Data"
# output_file = "Oscar Data/merged_courses.csv"
# merge_csv_files(input_folder, output_file)





dict = {' Tracking Sheet ': {'General Education and Projects': {'MQP': [['MQP', False], ['MQP', False], ['MQP', False]], 'Physical Education': [['PE', False], ['PE', False], ['PE', False], ['PE', False]], 'Humanities': [['Humanities Capstone', False, ['HU_3900', 'HU_3910']], ['Humanities', False, ['EN_DEPT', 'WR_DEPT']], ['Humanities', False, ['EN_DEPT', 'WR_DEPT']], ['Humanities', False, ['EN_DEPT', 'WR_DEPT']], ['Humanities', False, ['EN_DEPT', 'WR_DEPT']], ['Humanities', False, ['EN_DEPT', 'WR_DEPT']]], 'IQP': [['IQP Off Campus', False, ['IQP_A', 'IQP_B', 'IQP_C', 'IQP_D', 'IQP_OFF_CAMPUS']]], 'Social Science': [['ID_2050', False, ['ID_2050']], ['Social Science', False, ['ECON_DEPT', 'ENV_DEPT', 'GOV_DEPT', 'PSY_DEPT', 'SD_DEPT', 'SOC_DEPT', 'SS_DEPT', 'STS_DEPT', 'DEV_DEPT', 'GOV_2313']]], 'Free Electives': [['FREE ELECTIVE', False], ['FREE ELECTIVE', False], ['FREE ELECTIVE', False]], 'Not used': []}, 'Computer Science': {'CS Core': [['CS 3043', False], ['CS 3133', False], ['CS 4000+ Level Electives', False, ['BCB_4002', 'CS_4802', 'BCB_4003', 'CS_4803', 'CS_4099', 'CS_4100', 'IMGD_4100', 'CS_4241', 'CS_4300', 'IMGD_4300', 'CS_4341', 'CS_4342', 'CS_4401', 'CS_4404', 'CS_4432', 'CS_4433', 'DS_4433', 'CS_4445', 'CS_4518', 'CS_4731', 'CS_4732', 'CS_4804', 'BCB_502', 'CS_582', 'BCB_503', 'CS_583', 'CS_504', 'CS_513', 'CS_514', 'ECE_572', 'CS_521', 'CS_522', 'MA_510', 'CS_525', 'CS_526', 'RBE_526', 'CS_528', 'CS_529', 'ECE_581', 'CS_534', 'CS_538', 'CS_539', 'CS_540', 'CS_543', 'CS_545', 'ECE_545', 'CS_548', 'CS_549', 'RBE_549', 'CS_557', 'CS_558', 'CS_559', 'CS_563', 'CS_564', 'CS_571', 'CS_573', 'CS_577', 'ECE_577', 'CS_578', 'ECE_578', 'CS_585', 'DS_503', 'CS_586', 'DS_504', 'CS_673', 'ECE_673', 'CS_5008', 'CS_541', 'DS_541', 'CS_547', 'DS_547', 'CS_565', 'SEME_565', 'CS_566', 'SEME_566', 'CS_567', 'SEME_567', 'CS_568', 'SEME_568']], ['CS 4000+ Level Electives', False, ['BCB_4002', 'CS_4802', 'BCB_4003', 'CS_4803', 'CS_4099', 'CS_4100', 'IMGD_4100', 'CS_4241', 'CS_4300', 'IMGD_4300', 'CS_4341', 'CS_4342', 'CS_4401', 'CS_4404', 'CS_4432', 'CS_4433', 'DS_4433', 'CS_4445', 'CS_4518', 'CS_4731', 'CS_4732', 'CS_4804', 'BCB_502', 'CS_582', 'BCB_503', 'CS_583', 'CS_504', 'CS_513', 'CS_514', 'ECE_572', 'CS_521', 'CS_522', 'MA_510', 'CS_525', 'CS_526', 'RBE_526', 'CS_528', 'CS_529', 'ECE_581', 'CS_534', 'CS_538', 'CS_539', 'CS_540', 'CS_543', 'CS_545', 'ECE_545', 'CS_548', 'CS_549', 'RBE_549', 'CS_557', 'CS_558', 'CS_559', 'CS_563', 'CS_564', 'CS_571', 'CS_573', 'CS_577', 'ECE_577', 'CS_578', 'ECE_578', 'CS_585', 'DS_503', 'CS_586', 'DS_504', 'CS_673', 'ECE_673', 'CS_5008', 'CS_541', 'DS_541', 'CS_547', 'DS_547', 'CS_565', 'SEME_565', 'CS_566', 'SEME_566', 'CS_567', 'SEME_567', 'CS_568', 'SEME_568']], ['CS 4000+ Level Electives', False, ['BCB_4002', 'CS_4802', 'BCB_4003', 'CS_4803', 'CS_4099', 'CS_4100', 'IMGD_4100', 'CS_4241', 'CS_4300', 'IMGD_4300', 'CS_4341', 'CS_4342', 'CS_4401', 'CS_4404', 'CS_4432', 'CS_4433', 'DS_4433', 'CS_4445', 'CS_4518', 'CS_4731', 'CS_4732', 'CS_4804', 'BCB_502', 'CS_582', 'BCB_503', 'CS_583', 'CS_504', 'CS_513', 'CS_514', 'ECE_572', 'CS_521', 'CS_522', 'MA_510', 'CS_525', 'CS_526', 'RBE_526', 'CS_528', 'CS_529', 'ECE_581', 'CS_534', 'CS_538', 'CS_539', 'CS_540', 'CS_543', 'CS_545', 'ECE_545', 'CS_548', 'CS_549', 'RBE_549', 'CS_557', 'CS_558', 'CS_559', 'CS_563', 'CS_564', 'CS_571', 'CS_573', 'CS_577', 'ECE_577', 'CS_578', 'ECE_578', 'CS_585', 'DS_503', 'CS_586', 'DS_504', 'CS_673', 'ECE_673', 'CS_5008', 'CS_541', 'DS_541', 'CS_547', 'DS_547', 'CS_565', 'SEME_565', 'CS_566', 'SEME_566', 'CS_567', 'SEME_567', 'CS_568', 'SEME_568']], ['CS 4000+ Level Electives', False, ['BCB_4002', 'CS_4802', 'BCB_4003', 'CS_4803', 'CS_4099', 'CS_4100', 'IMGD_4100', 'CS_4241', 'CS_4300', 'IMGD_4300', 'CS_4341', 'CS_4342', 'CS_4401', 'CS_4404', 'CS_4432', 'CS_4433', 'DS_4433', 'CS_4445', 'CS_4518', 'CS_4731', 'CS_4732', 'CS_4804', 'BCB_502', 'CS_582', 'BCB_503', 'CS_583', 'CS_504', 'CS_513', 'CS_514', 'ECE_572', 'CS_521', 'CS_522', 'MA_510', 'CS_525', 'CS_526', 'RBE_526', 'CS_528', 'CS_529', 'ECE_581', 'CS_534', 'CS_538', 'CS_539', 'CS_540', 'CS_543', 'CS_545', 'ECE_545', 'CS_548', 'CS_549', 'RBE_549', 'CS_557', 'CS_558', 'CS_559', 'CS_563', 'CS_564', 'CS_571', 'CS_573', 'CS_577', 'ECE_577', 'CS_578', 'ECE_578', 'CS_585', 'DS_503', 'CS_586', 'DS_504', 'CS_673', 'ECE_673', 'CS_5008', 'CS_541', 'DS_541', 'CS_547', 'DS_547', 'CS_565', 'SEME_565', 'CS_566', 'SEME_566', 'CS_567', 'SEME_567', 'CS_568', 'SEME_568']], ['CS Electives', False, ['CS_2011', 'CS_2223', 'CS_3516']], ['CS Electives', False, ['CS_2011', 'CS_2223', 'CS_3516']], ['CS Electives', False, ['CS_2011', 'CS_2223', 'CS_3516']], ['CS Electives', False, ['CS_2011', 'CS_2223', 'CS_3516']], ['CS Electives', False, ['CS_2011', 'CS_2223', 'CS_3516']]], 'General Math': [['1000 Level Math', False, ['MA_1020', 'MA_1021', 'MA_1022', 'MA_1023', 'MA_1024', 'MA_1033', 'MA_1034', 'MA_1120', 'MA_1801', 'MA_1971']], ['1000 Level Math', False, ['MA_1020', 'MA_1021', 'MA_1022', 'MA_1023', 'MA_1024', 'MA_1033', 'MA_1034', 'MA_1120', 'MA_1801', 'MA_1971']], ['1000 Level Math', False, ['MA_1020', 'MA_1021', 'MA_1022', 'MA_1023', 'MA_1024', 'MA_1033', 'MA_1034', 'MA_1120', 'MA_1801', 'MA_1971']], ['1000 Level Math', False, ['MA_1020', 'MA_1021', 'MA_1022', 'MA_1023', 'MA_1024', 'MA_1033', 'MA_1034', 'MA_1120', 'MA_1801', 'MA_1971']], ['Math Electives', False, ['MA_2051', 'MA_2071', 'MA_2072', 'MA_2073', 'MA_2210', 'MA_2211', 'MA_2212', 'MA_2251', 'MA_2271', 'MA_2273', 'MA_2431', 'MA_2610', 'MA_3212', 'MA_3213', 'MA_3231', 'MA_3233', 'MA_3471', 'MA_3475', 'MA_3627', 'MA_3631', 'MA_3823', 'MA_3825', 'MA_3831', 'MA_3832', 'BCB_4004', 'MA_4603', 'DS_4635', 'MA_4635', 'MA_4213', 'MA_4214', 'MA_4216', 'MA_4222', 'MA_4235', 'MA_4237', 'MA_4291', 'MA_4411', 'MA_4451', 'MA_4473', 'MA_4631', 'MA_4632', 'MA_4891', 'MA_4892', 'MA_4895', 'DS_502', 'MA_543', 'MA_542', 'MA_554', 'MA_540', 'MA_541']]], 'General Science': [['Biology', False, ['BB_1001', 'BB_1002', 'BB_1003', 'BCB_1003', 'BB_1025', 'BB_1035', 'BB_1045', 'BB_2002', 'BB_2003', 'BB_2030', 'BB_2040', 'BB_2050', 'BB_2550', 'BB_2902', 'BB_2903', 'BB_2904', 'BB_2915', 'BB_2917', 'BB_2920', 'BB_2950', 'BB_3003', 'BB_3010', 'BCB_3010', 'BB_3050', 'BB_3080', 'BB_3101', 'BB_3102', 'BB_3120', 'BB_3140', 'BB_3512', 'BB_3513', 'BB_3515', 'BB_3517', 'BB_3519', 'BB_3521', 'BB_3525', 'BB_3526', 'BB_3527', 'BB_3530', 'BB_3570', 'BB_3620', 'BB_3920', 'BB_4150', 'BB_4620', 'BB_4801', 'BCB_4001', 'BB_4900']], ['Biology', False, ['BB_1001', 'BB_1002', 'BB_1003', 'BCB_1003', 'BB_1025', 'BB_1035', 'BB_1045', 'BB_2002', 'BB_2003', 'BB_2030', 'BB_2040', 'BB_2050', 'BB_2550', 'BB_2902', 'BB_2903', 'BB_2904', 'BB_2915', 'BB_2917', 'BB_2920', 'BB_2950', 'BB_3003', 'BB_3010', 'BCB_3010', 'BB_3050', 'BB_3080', 'BB_3101', 'BB_3102', 'BB_3120', 'BB_3140', 'BB_3512', 'BB_3513', 'BB_3515', 'BB_3517', 'BB_3519', 'BB_3521', 'BB_3525', 'BB_3526', 'BB_3527', 'BB_3530', 'BB_3570', 'BB_3620', 'BB_3920', 'BB_4150', 'BB_4620', 'BB_4801', 'BCB_4001', 'BB_4900']], ['Biology', False, ['BB_1001', 'BB_1002', 'BB_1003', 'BCB_1003', 'BB_1025', 'BB_1035', 'BB_1045', 'BB_2002', 'BB_2003', 'BB_2030', 'BB_2040', 'BB_2050', 'BB_2550', 'BB_2902', 'BB_2903', 'BB_2904', 'BB_2915', 'BB_2917', 'BB_2920', 'BB_2950', 'BB_3003', 'BB_3010', 'BCB_3010', 'BB_3050', 'BB_3080', 'BB_3101', 'BB_3102', 'BB_3120', 'BB_3140', 'BB_3512', 'BB_3513', 'BB_3515', 'BB_3517', 'BB_3519', 'BB_3521', 'BB_3525', 'BB_3526', 'BB_3527', 'BB_3530', 'BB_3570', 'BB_3620', 'BB_3920', 'BB_4150', 'BB_4620', 'BB_4801', 'BCB_4001', 'BB_4900']]], 'Probability': [], 'Science/Engineering Electives': [['Science and Engineering Electives', False, ['BME_2001', 'BME_2210', 'BME_2211', 'BME_2502', 'BME_2610', 'BME_3012', 'BME_3013', 'BME_3014', 'BME_3111', 'BME_3112', 'BME_3300', 'BME_3503', 'BME_3505', 'BME_3506', 'BME_3605', 'BME_3610', 'BME_3811', 'BME_3813', 'BME_4011', 'ECE_4011', 'BME_4023', 'ECE_4023', 'BME_4201', 'BME_4300', 'BME_4503', 'BME_4504', 'ME_4504', 'BME_4606', 'ME_4606', 'BME_4701', 'BME_4814', 'ME_4814', 'BME_4828', 'BME_4831', 'BME_1001', 'BME_1004', 'CE_2000', 'CE_2001', 'CE_2002', 'CE_2020', 'CE_3006', 'CE_3008', 'CE_3010', 'CE_3020', 'CE_3025', 'CE_3026', 'CE_3030', 'CE_3031', 'CE_3041', 'CE_3044', 'CE_3050', 'CE_3051', 'CE_3059', 'CE_3060', 'CE_3061', 'CE_3062', 'CE_3070', 'CE_3074', 'CE_4007', 'CE_4060', 'CE_4061', 'CE_4063', 'CHE_4063', 'CE_4071', 'CE_4600', 'CE_4610', 'CE_1030', 'CHE_2011', 'CHE_2012', 'CHE_2013', 'CHE_2014', 'CHE_2301', 'ME_2301', 'CHE_3201', 'CHE_3301', 'CHE_3501', 'CHE_3702', 'CHE_3722', 'CHE_4401', 'CHE_4402', 'CHE_4403', 'CHE_4404', 'CHE_4405', 'CHE_4410', 'CHE_1011', 'ECE_2010', 'ECE_2019', 'ECE_2029', 'ECE_2049', 'ECE_2112', 'ECE_2201', 'ECE_2305', 'ECE_2311', 'ECE_2312', 'ECE_2799', 'ECE_3012', 'ECE_3113', 'ECE_3204', 'ECE_3308', 'ECE_3311', 'ECE_3500', 'ECE_3501', 'ECE_3829', 'ECE_3849', 'ECE_4305', 'ECE_4503', 'ECE_4703', 'ECE_4801', 'ECE_4902', 'ECE_4904', 'ECE_1799', 'ES_2001', 'ES_2501', 'ES_2502', 'ES_2503', 'ES_2800', 'ES_3001', 'ES_3002', 'ES_3003', 'ES_3004', 'ES_3011', 'ES_3323', 'ES_3501', 'ES_1020', 'ES_1310', 'ES_1500', 'ME_2300', 'ME_2312', 'ME_2820', 'ME_3310', 'ME_3311', 'ME_3320', 'ME_3411', 'ME_3501', 'ME_3506', 'ME_3801', 'ME_3820', 'ME_3901', 'ME_3902', 'ME_4320', 'ME_4323', 'ME_4324', 'ME_4422', 'ME_4429', 'ME_4430', 'ME_4505', 'ME_4506', 'ME_4512', 'ME_4710', 'ME_4813', 'ME_4832', 'ME_4840', 'ME_4875', 'MTE_575', 'RBE_4322', 'ME_4322', 'ME_1520', 'ME_1800', 'RBE_2001', 'RBE_2002', 'RBE_3001', 'RBE_3002', 'RBE_4540', 'RBE_4815', 'RBE_1001']], ['Science and Engineering Electives', False, ['BME_2001', 'BME_2210', 'BME_2211', 'BME_2502', 'BME_2610', 'BME_3012', 'BME_3013', 'BME_3014', 'BME_3111', 'BME_3112', 'BME_3300', 'BME_3503', 'BME_3505', 'BME_3506', 'BME_3605', 'BME_3610', 'BME_3811', 'BME_3813', 'BME_4011', 'ECE_4011', 'BME_4023', 'ECE_4023', 'BME_4201', 'BME_4300', 'BME_4503', 'BME_4504', 'ME_4504', 'BME_4606', 'ME_4606', 'BME_4701', 'BME_4814', 'ME_4814', 'BME_4828', 'BME_4831', 'BME_1001', 'BME_1004', 'CE_2000', 'CE_2001', 'CE_2002', 'CE_2020', 'CE_3006', 'CE_3008', 'CE_3010', 'CE_3020', 'CE_3025', 'CE_3026', 'CE_3030', 'CE_3031', 'CE_3041', 'CE_3044', 'CE_3050', 'CE_3051', 'CE_3059', 'CE_3060', 'CE_3061', 'CE_3062', 'CE_3070', 'CE_3074', 'CE_4007', 'CE_4060', 'CE_4061', 'CE_4063', 'CHE_4063', 'CE_4071', 'CE_4600', 'CE_4610', 'CE_1030', 'CHE_2011', 'CHE_2012', 'CHE_2013', 'CHE_2014', 'CHE_2301', 'ME_2301', 'CHE_3201', 'CHE_3301', 'CHE_3501', 'CHE_3702', 'CHE_3722', 'CHE_4401', 'CHE_4402', 'CHE_4403', 'CHE_4404', 'CHE_4405', 'CHE_4410', 'CHE_1011', 'ECE_2010', 'ECE_2019', 'ECE_2029', 'ECE_2049', 'ECE_2112', 'ECE_2201', 'ECE_2305', 'ECE_2311', 'ECE_2312', 'ECE_2799', 'ECE_3012', 'ECE_3113', 'ECE_3204', 'ECE_3308', 'ECE_3311', 'ECE_3500', 'ECE_3501', 'ECE_3829', 'ECE_3849', 'ECE_4305', 'ECE_4503', 'ECE_4703', 'ECE_4801', 'ECE_4902', 'ECE_4904', 'ECE_1799', 'ES_2001', 'ES_2501', 'ES_2502', 'ES_2503', 'ES_2800', 'ES_3001', 'ES_3002', 'ES_3003', 'ES_3004', 'ES_3011', 'ES_3323', 'ES_3501', 'ES_1020', 'ES_1310', 'ES_1500', 'ME_2300', 'ME_2312', 'ME_2820', 'ME_3310', 'ME_3311', 'ME_3320', 'ME_3411', 'ME_3501', 'ME_3506', 'ME_3801', 'ME_3820', 'ME_3901', 'ME_3902', 'ME_4320', 'ME_4323', 'ME_4324', 'ME_4422', 'ME_4429', 'ME_4430', 'ME_4505', 'ME_4506', 'ME_4512', 'ME_4710', 'ME_4813', 'ME_4832', 'ME_4840', 'ME_4875', 'MTE_575', 'RBE_4322', 'ME_4322', 'ME_1520', 'ME_1800', 'RBE_2001', 'RBE_2002', 'RBE_3001', 'RBE_3002', 'RBE_4540', 'RBE_4815', 'RBE_1001']]], 'Statistics': []}}}


new_dict = {'Computer Science': {'CS Core': [['CS 3043', False], ['CS 3133', False], ['CS 4000+ Level Electives', False, ['BCB_4002', 'CS_4802', 'BCB_4003', 'CS_4803', 'CS_4099', 'CS_4100', 'IMGD_4100', 'CS_4241', 'CS_4300', 'IMGD_4300', 'CS_4341', 'CS_4342', 'CS_4401', 'CS_4404', 'CS_4432', 'CS_4433', 'DS_4433', 'CS_4445', 'CS_4518', 'CS_4731', 'CS_4732', 'CS_4804', 'BCB_502', 'CS_582', 'BCB_503', 'CS_583', 'CS_504', 'CS_513', 'CS_514', 'ECE_572', 'CS_521', 'CS_522', 'MA_510', 'CS_525', 'CS_526', 'RBE_526', 'CS_528', 'CS_529', 'ECE_581', 'CS_534', 'CS_538', 'CS_539', 'CS_540', 'CS_543', 'CS_545', 'ECE_545', 'CS_548', 'CS_549', 'RBE_549', 'CS_557', 'CS_558', 'CS_559', 'CS_563', 'CS_564', 'CS_571', 'CS_573', 'CS_577', 'ECE_577', 'CS_578', 'ECE_578', 'CS_585', 'DS_503', 'CS_586', 'DS_504', 'CS_673', 'ECE_673', 'CS_5008', 'CS_541', 'DS_541', 'CS_547', 'DS_547', 'CS_565', 'SEME_565', 'CS_566', 'SEME_566', 'CS_567', 'SEME_567', 'CS_568', 'SEME_568']], ['CS 4000+ Level Electives', False, ['BCB_4002', 'CS_4802', 'BCB_4003', 'CS_4803', 'CS_4099', 'CS_4100', 'IMGD_4100', 'CS_4241', 'CS_4300', 'IMGD_4300', 'CS_4341', 'CS_4342', 'CS_4401', 'CS_4404', 'CS_4432', 'CS_4433', 'DS_4433', 'CS_4445', 'CS_4518', 'CS_4731', 'CS_4732', 'CS_4804', 'BCB_502', 'CS_582', 'BCB_503', 'CS_583', 'CS_504', 'CS_513', 'CS_514', 'ECE_572', 'CS_521', 'CS_522', 'MA_510', 'CS_525', 'CS_526', 'RBE_526', 'CS_528', 'CS_529', 'ECE_581', 'CS_534', 'CS_538', 'CS_539', 'CS_540', 'CS_543', 'CS_545', 'ECE_545', 'CS_548', 'CS_549', 'RBE_549', 'CS_557', 'CS_558', 'CS_559', 'CS_563', 'CS_564', 'CS_571', 'CS_573', 'CS_577', 'ECE_577', 'CS_578', 'ECE_578', 'CS_585', 'DS_503', 'CS_586', 'DS_504', 'CS_673', 'ECE_673', 'CS_5008', 'CS_541', 'DS_541', 'CS_547', 'DS_547', 'CS_565', 'SEME_565', 'CS_566', 'SEME_566', 'CS_567', 'SEME_567', 'CS_568', 'SEME_568']], ['CS 4000+ Level Electives', False, ['BCB_4002', 'CS_4802', 'BCB_4003', 'CS_4803', 'CS_4099', 'CS_4100', 'IMGD_4100', 'CS_4241', 'CS_4300', 'IMGD_4300', 'CS_4341', 'CS_4342', 'CS_4401', 'CS_4404', 'CS_4432', 'CS_4433', 'DS_4433', 'CS_4445', 'CS_4518', 'CS_4731', 'CS_4732', 'CS_4804', 'BCB_502', 'CS_582', 'BCB_503', 'CS_583', 'CS_504', 'CS_513', 'CS_514', 'ECE_572', 'CS_521', 'CS_522', 'MA_510', 'CS_525', 'CS_526', 'RBE_526', 'CS_528', 'CS_529', 'ECE_581', 'CS_534', 'CS_538', 'CS_539', 'CS_540', 'CS_543', 'CS_545', 'ECE_545', 'CS_548', 'CS_549', 'RBE_549', 'CS_557', 'CS_558', 'CS_559', 'CS_563', 'CS_564', 'CS_571', 'CS_573', 'CS_577', 'ECE_577', 'CS_578', 'ECE_578', 'CS_585', 'DS_503', 'CS_586', 'DS_504', 'CS_673', 'ECE_673', 'CS_5008', 'CS_541', 'DS_541', 'CS_547', 'DS_547', 'CS_565', 'SEME_565', 'CS_566', 'SEME_566', 'CS_567', 'SEME_567', 'CS_568', 'SEME_568']], ['CS 4000+ Level Electives', False, ['BCB_4002', 'CS_4802', 'BCB_4003', 'CS_4803', 'CS_4099', 'CS_4100', 'IMGD_4100', 'CS_4241', 'CS_4300', 'IMGD_4300', 'CS_4341', 'CS_4342', 'CS_4401', 'CS_4404', 'CS_4432', 'CS_4433', 'DS_4433', 'CS_4445', 'CS_4518', 'CS_4731', 'CS_4732', 'CS_4804', 'BCB_502', 'CS_582', 'BCB_503', 'CS_583', 'CS_504', 'CS_513', 'CS_514', 'ECE_572', 'CS_521', 'CS_522', 'MA_510', 'CS_525', 'CS_526', 'RBE_526', 'CS_528', 'CS_529', 'ECE_581', 'CS_534', 'CS_538', 'CS_539', 'CS_540', 'CS_543', 'CS_545', 'ECE_545', 'CS_548', 'CS_549', 'RBE_549', 'CS_557', 'CS_558', 'CS_559', 'CS_563', 'CS_564', 'CS_571', 'CS_573', 'CS_577', 'ECE_577', 'CS_578', 'ECE_578', 'CS_585', 'DS_503', 'CS_586', 'DS_504', 'CS_673', 'ECE_673', 'CS_5008', 'CS_541', 'DS_541', 'CS_547', 'DS_547', 'CS_565', 'SEME_565', 'CS_566', 'SEME_566', 'CS_567', 'SEME_567', 'CS_568', 'SEME_568']], ['CS Electives', False, ['CS_2011', 'CS_2223', 'CS_3516']], ['CS Electives', False, ['CS_2011', 'CS_2223', 'CS_3516']], ['CS Electives', False, ['CS_2011', 'CS_2223', 'CS_3516']], ['CS Electives', False, ['CS_2011', 'CS_2223', 'CS_3516']], ['CS Electives', False, ['CS_2011', 'CS_2223', 'CS_3516']]], 'General Math': [['1000 Level Math', False, ['MA_1020', 'MA_1021', 'MA_1022', 'MA_1023', 'MA_1024', 'MA_1033', 'MA_1034', 'MA_1120', 'MA_1801', 'MA_1971']], ['1000 Level Math', False, ['MA_1020', 'MA_1021', 'MA_1022', 'MA_1023', 'MA_1024', 'MA_1033', 'MA_1034', 'MA_1120', 'MA_1801', 'MA_1971']], ['1000 Level Math', False, ['MA_1020', 'MA_1021', 'MA_1022', 'MA_1023', 'MA_1024', 'MA_1033', 'MA_1034', 'MA_1120', 'MA_1801', 'MA_1971']], ['1000 Level Math', False, ['MA_1020', 'MA_1021', 'MA_1022', 'MA_1023', 'MA_1024', 'MA_1033', 'MA_1034', 'MA_1120', 'MA_1801', 'MA_1971']], ['Math Electives', False, ['MA_2051', 'MA_2071', 'MA_2072', 'MA_2073', 'MA_2210', 'MA_2211', 'MA_2212', 'MA_2251', 'MA_2271', 'MA_2273', 'MA_2431', 'MA_2610', 'MA_3212', 'MA_3213', 'MA_3231', 'MA_3233', 'MA_3471', 'MA_3475', 'MA_3627', 'MA_3631', 'MA_3823', 'MA_3825', 'MA_3831', 'MA_3832', 'BCB_4004', 'MA_4603', 'DS_4635', 'MA_4635', 'MA_4213', 'MA_4214', 'MA_4216', 'MA_4222', 'MA_4235', 'MA_4237', 'MA_4291', 'MA_4411', 'MA_4451', 'MA_4473', 'MA_4631', 'MA_4632', 'MA_4891', 'MA_4892', 'MA_4895', 'DS_502', 'MA_543', 'MA_542', 'MA_554', 'MA_540', 'MA_541']]], 'General Science': [['Biology', False, ['BB_1001', 'BB_1002', 'BB_1003', 'BCB_1003', 'BB_1025', 'BB_1035', 'BB_1045', 'BB_2002', 'BB_2003', 'BB_2030', 'BB_2040', 'BB_2050', 'BB_2550', 'BB_2902', 'BB_2903', 'BB_2904', 'BB_2915', 'BB_2917', 'BB_2920', 'BB_2950', 'BB_3003', 'BB_3010', 'BCB_3010', 'BB_3050', 'BB_3080', 'BB_3101', 'BB_3102', 'BB_3120', 'BB_3140', 'BB_3512', 'BB_3513', 'BB_3515', 'BB_3517', 'BB_3519', 'BB_3521', 'BB_3525', 'BB_3526', 'BB_3527', 'BB_3530', 'BB_3570', 'BB_3620', 'BB_3920', 'BB_4150', 'BB_4620', 'BB_4801', 'BCB_4001', 'BB_4900']], ['Biology', False, ['BB_1001', 'BB_1002', 'BB_1003', 'BCB_1003', 'BB_1025', 'BB_1035', 'BB_1045', 'BB_2002', 'BB_2003', 'BB_2030', 'BB_2040', 'BB_2050', 'BB_2550', 'BB_2902', 'BB_2903', 'BB_2904', 'BB_2915', 'BB_2917', 'BB_2920', 'BB_2950', 'BB_3003', 'BB_3010', 'BCB_3010', 'BB_3050', 'BB_3080', 'BB_3101', 'BB_3102', 'BB_3120', 'BB_3140', 'BB_3512', 'BB_3513', 'BB_3515', 'BB_3517', 'BB_3519', 'BB_3521', 'BB_3525', 'BB_3526', 'BB_3527', 'BB_3530', 'BB_3570', 'BB_3620', 'BB_3920', 'BB_4150', 'BB_4620', 'BB_4801', 'BCB_4001', 'BB_4900']], ['Biology', False, ['BB_1001', 'BB_1002', 'BB_1003', 'BCB_1003', 'BB_1025', 'BB_1035', 'BB_1045', 'BB_2002', 'BB_2003', 'BB_2030', 'BB_2040', 'BB_2050', 'BB_2550', 'BB_2902', 'BB_2903', 'BB_2904', 'BB_2915', 'BB_2917', 'BB_2920', 'BB_2950', 'BB_3003', 'BB_3010', 'BCB_3010', 'BB_3050', 'BB_3080', 'BB_3101', 'BB_3102', 'BB_3120', 'BB_3140', 'BB_3512', 'BB_3513', 'BB_3515', 'BB_3517', 'BB_3519', 'BB_3521', 'BB_3525', 'BB_3526', 'BB_3527', 'BB_3530', 'BB_3570', 'BB_3620', 'BB_3920', 'BB_4150', 'BB_4620', 'BB_4801', 'BCB_4001', 'BB_4900']]], 'Probability': [], 'Science/Engineering Electives': [['Science and Engineering Electives', False, ['BME_2001', 'BME_2210', 'BME_2211', 'BME_2502', 'BME_2610', 'BME_3012', 'BME_3013', 'BME_3014', 'BME_3111', 'BME_3112', 'BME_3300', 'BME_3503', 'BME_3505', 'BME_3506', 'BME_3605', 'BME_3610', 'BME_3811', 'BME_3813', 'BME_4011', 'ECE_4011', 'BME_4023', 'ECE_4023', 'BME_4201', 'BME_4300', 'BME_4503', 'BME_4504', 'ME_4504', 'BME_4606', 'ME_4606', 'BME_4701', 'BME_4814', 'ME_4814', 'BME_4828', 'BME_4831', 'BME_1001', 'BME_1004', 'CE_2000', 'CE_2001', 'CE_2002', 'CE_2020', 'CE_3006', 'CE_3008', 'CE_3010', 'CE_3020', 'CE_3025', 'CE_3026', 'CE_3030', 'CE_3031', 'CE_3041', 'CE_3044', 'CE_3050', 'CE_3051', 'CE_3059', 'CE_3060', 'CE_3061', 'CE_3062', 'CE_3070', 'CE_3074', 'CE_4007', 'CE_4060', 'CE_4061', 'CE_4063', 'CHE_4063', 'CE_4071', 'CE_4600', 'CE_4610', 'CE_1030', 'CHE_2011', 'CHE_2012', 'CHE_2013', 'CHE_2014', 'CHE_2301', 'ME_2301', 'CHE_3201', 'CHE_3301', 'CHE_3501', 'CHE_3702', 'CHE_3722', 'CHE_4401', 'CHE_4402', 'CHE_4403', 'CHE_4404', 'CHE_4405', 'CHE_4410', 'CHE_1011', 'ECE_2010', 'ECE_2019', 'ECE_2029', 'ECE_2049', 'ECE_2112', 'ECE_2201', 'ECE_2305', 'ECE_2311', 'ECE_2312', 'ECE_2799', 'ECE_3012', 'ECE_3113', 'ECE_3204', 'ECE_3308', 'ECE_3311', 'ECE_3500', 'ECE_3501', 'ECE_3829', 'ECE_3849', 'ECE_4305', 'ECE_4503', 'ECE_4703', 'ECE_4801', 'ECE_4902', 'ECE_4904', 'ECE_1799', 'ES_2001', 'ES_2501', 'ES_2502', 'ES_2503', 'ES_2800', 'ES_3001', 'ES_3002', 'ES_3003', 'ES_3004', 'ES_3011', 'ES_3323', 'ES_3501', 'ES_1020', 'ES_1310', 'ES_1500', 'ME_2300', 'ME_2312', 'ME_2820', 'ME_3310', 'ME_3311', 'ME_3320', 'ME_3411', 'ME_3501', 'ME_3506', 'ME_3801', 'ME_3820', 'ME_3901', 'ME_3902', 'ME_4320', 'ME_4323', 'ME_4324', 'ME_4422', 'ME_4429', 'ME_4430', 'ME_4505', 'ME_4506', 'ME_4512', 'ME_4710', 'ME_4813', 'ME_4832', 'ME_4840', 'ME_4875', 'MTE_575', 'RBE_4322', 'ME_4322', 'ME_1520', 'ME_1800', 'RBE_2001', 'RBE_2002', 'RBE_3001', 'RBE_3002', 'RBE_4540', 'RBE_4815', 'RBE_1001']], ['Science and Engineering Electives', False, ['BME_2001', 'BME_2210', 'BME_2211', 'BME_2502', 'BME_2610', 'BME_3012', 'BME_3013', 'BME_3014', 'BME_3111', 'BME_3112', 'BME_3300', 'BME_3503', 'BME_3505', 'BME_3506', 'BME_3605', 'BME_3610', 'BME_3811', 'BME_3813', 'BME_4011', 'ECE_4011', 'BME_4023', 'ECE_4023', 'BME_4201', 'BME_4300', 'BME_4503', 'BME_4504', 'ME_4504', 'BME_4606', 'ME_4606', 'BME_4701', 'BME_4814', 'ME_4814', 'BME_4828', 'BME_4831', 'BME_1001', 'BME_1004', 'CE_2000', 'CE_2001', 'CE_2002', 'CE_2020', 'CE_3006', 'CE_3008', 'CE_3010', 'CE_3020', 'CE_3025', 'CE_3026', 'CE_3030', 'CE_3031', 'CE_3041', 'CE_3044', 'CE_3050', 'CE_3051', 'CE_3059', 'CE_3060', 'CE_3061', 'CE_3062', 'CE_3070', 'CE_3074', 'CE_4007', 'CE_4060', 'CE_4061', 'CE_4063', 'CHE_4063', 'CE_4071', 'CE_4600', 'CE_4610', 'CE_1030', 'CHE_2011', 'CHE_2012', 'CHE_2013', 'CHE_2014', 'CHE_2301', 'ME_2301', 'CHE_3201', 'CHE_3301', 'CHE_3501', 'CHE_3702', 'CHE_3722', 'CHE_4401', 'CHE_4402', 'CHE_4403', 'CHE_4404', 'CHE_4405', 'CHE_4410', 'CHE_1011', 'ECE_2010', 'ECE_2019', 'ECE_2029', 'ECE_2049', 'ECE_2112', 'ECE_2201', 'ECE_2305', 'ECE_2311', 'ECE_2312', 'ECE_2799', 'ECE_3012', 'ECE_3113', 'ECE_3204', 'ECE_3308', 'ECE_3311', 'ECE_3500', 'ECE_3501', 'ECE_3829', 'ECE_3849', 'ECE_4305', 'ECE_4503', 'ECE_4703', 'ECE_4801', 'ECE_4902', 'ECE_4904', 'ECE_1799', 'ES_2001', 'ES_2501', 'ES_2502', 'ES_2503', 'ES_2800', 'ES_3001', 'ES_3002', 'ES_3003', 'ES_3004', 'ES_3011', 'ES_3323', 'ES_3501', 'ES_1020', 'ES_1310', 'ES_1500', 'ME_2300', 'ME_2312', 'ME_2820', 'ME_3310', 'ME_3311', 'ME_3320', 'ME_3411', 'ME_3501', 'ME_3506', 'ME_3801', 'ME_3820', 'ME_3901', 'ME_3902', 'ME_4320', 'ME_4323', 'ME_4324', 'ME_4422', 'ME_4429', 'ME_4430', 'ME_4505', 'ME_4506', 'ME_4512', 'ME_4710', 'ME_4813', 'ME_4832', 'ME_4840', 'ME_4875', 'MTE_575', 'RBE_4322', 'ME_4322', 'ME_1520', 'ME_1800', 'RBE_2001', 'RBE_2002', 'RBE_3001', 'RBE_3002', 'RBE_4540', 'RBE_4815', 'RBE_1001']]], 'Statistics': []}}



# Print the values of the dictionary
def print_dict_values(dict, json_file):
    for tracking_sheet, tracking_sheet_div in dict.items():
        for category, subcategories in tracking_sheet_div.items():
            # print(f"Category: {category}")
            for subcategory, requirements in subcategories.items():
                # print(f"  Subcategory: {subcategory}")
                for requirement in requirements:
                    if len(requirement) > 2:
                        for subrequirement in requirement[2]:
                            for course in json_file['courses']:
                                subrequirement = subrequirement.replace("_", " ")
                                if subrequirement == course['Course Number']:
                                    print(f"Course: {course['Course Number']}")
                                    


       
# # read json file
# with open("Data/Oscar+RP_Ddata/CS_courses.json", "r") as file:
#     courses_data = json.load(file)


# def json_print(json_file):
#     for course in json_file['courses']:
#         print(course['Course Number'])
    

# print_dict_values(dict, courses_data)

# json_print(courses_data)



import json
from collections import defaultdict

def transform_data(input_file, output_file):
    # Read the input JSON file
    with open(input_file, "r") as f:
        data = json.load(f)

    # Dictionary to hold the transformed data
    transformed_data = {"courses": []}
    courses_dict = defaultdict(lambda: {
        "Course Number": None,
        "Course Name": None,
        "average_grade": None,
        "hours": None,
        "Professors": []
    })

    # Process each course
    for entry in data:
        course_number = entry["Course Number"]
        if not courses_dict[course_number]["Course Number"]:
            courses_dict[course_number]["Course Number"] = entry["Course Number"]
            courses_dict[course_number]["Course Name"] = entry["Course Name"]
            courses_dict[course_number]["average_grade"] = entry["average_grade"]
            courses_dict[course_number]["hours"] = entry["hours"]

        courses_dict[course_number]["Professors"].append({
            "Professor Name": entry["Professor"],
            "Rating": entry["Rating"],
            "Would Take Again": entry["Would Take Again"],
            "Difficulty": entry["Difficulty"]
        })

    # Add the processed courses to the final structure
    transformed_data["courses"] = list(courses_dict.values())

    # Write the transformed data to the output JSON file
    with open(output_file, "w") as f:
        json.dump(transformed_data, f, indent=4)

# Example usage
transform_data("courses.json", "final_courses.json")











