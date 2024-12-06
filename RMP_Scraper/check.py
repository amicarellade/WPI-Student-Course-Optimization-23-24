import pandas as pd
file_path = "courses_and_professors_with_ratings.csv"  # Replace with your actual file path
df = pd.read_csv(file_path)
not_found_count = df[df["Rating"] == "Professor not found at WPI"].shape[0]
total_professors = df.shape[0]
not_found_percentage = (not_found_count / total_professors) * 100
print(f"Total professors: {total_professors}")
print(f"Professors not found: {not_found_count}")
print(f"Percentage of professors not found: {not_found_percentage:.2f}%")
