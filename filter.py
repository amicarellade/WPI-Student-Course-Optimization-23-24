import csv

def filter_courses(input_file, output_file, valid_prefixes):
        filtered_rows = []
        with open(input_file, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip header
            filtered_rows.append(header)  # Add header to the result
            for row in reader:
                if row[0].startswith(tuple(valid_prefixes)):
                    filtered_rows.append(row)

        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(filtered_rows)

    # Preprocess course data
filter_courses('all_courses_spring.csv', 'filtered_courses_spring.csv', ['CS', 'MA', 'DS'])

    # Preprocess professor data (optional, you can filter professors too if needed)
    # filter_courses('all_professors.csv', 'filtered_professors.csv', ['CS', 'MA', 'DS'])

print("Data preprocessing complete. Filtered data saved to 'filtered_courses_spring.csv'.")