import pandas as pd

# Load the CSV files into pandas DataFrames
file1 = "courses_and_professors_with_ratings.csv"  # Replace with the actual path to your first CSV file
file2 = "courses_dataset.csv"  # Replace with the actual path to your second CSV file


# Load data
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Preprocessing to ensure the keys match for merging
# Strip any whitespace and unify case for course numbers
df1['Course Number'] = df1['Course Number'].str.strip().str.upper()
df2['course'] = df2['course'].str.split("-").str[0].str.strip().str.upper()  # Standardize and extract course numbers

# Merge the DataFrames on the cleaned 'Course Number' column
merged_df = pd.merge(df1, df2, left_on='Course Number', right_on='course', how='inner')

# Drop redundant 'course' column from the second DataFrame
merged_df = merged_df.drop(columns=['course'])

# Save the merged DataFrame to a new CSV file
merged_file = "merged_courses.csv"
merged_df.to_csv(merged_file, index=False)

print(f"Merged CSV saved as '{merged_file}'")