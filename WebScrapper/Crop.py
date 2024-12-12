from PIL import Image
from pytesseract import pytesseract
import cv2
import numpy as np


def adjust_average(total_students, original_average, total_adjust):
    # Check for valid inputs
    if total_students < 0 or total_students < total_adjust:
        print(total_students)
        print(total_adjust)
        print(total_students < total_adjust)

        raise ValueError("Total students must be greater than 'Don't Know' students.")
    
    # Calculate the adjusted average
    adjusted_average = (
        (total_students * original_average - total_adjust * 5) /
        (total_students - total_adjust)
    )
    return adjusted_average


def preprocess_for_tesseract(image, threshold, kernel_size=1):
    # Convert to grayscale
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
    
    # Apply dilation and erosion to remove noise
    kernel = np.ones((1, 1), np.uint8)  # Larger kernel for stronger dilation/erosion
    processed_image = cv2.dilate(thresh, kernel, iterations=1)
    processed_image = cv2.erode(processed_image, kernel, iterations=1)
    
    # Convert back to PIL Image
    processed_image = Image.fromarray(processed_image)
    
    return processed_image


def average_grade_to_letter(average_grade):
    if average_grade < 1.33:
        return 'A+'
    if average_grade < 1.66:
        return 'A'
    if average_grade < 2:
        return 'A-'
    elif average_grade < 2.33:
        return 'B+'
    elif average_grade < 2.66:
        return 'B'
    elif average_grade < 3:
        return 'B-'
    elif average_grade < 3.33:
        return 'C+'
    elif average_grade < 3.66:
        return 'C'
    elif average_grade < 4:
        return 'C-'
    else:
        return 'D'


def average_hours_to_groups(average_hours):
    if average_hours < 2:
        return '0 hr/week'
    elif average_hours < 3:
        return '1-5 hr/week'
    elif average_hours < 4:
        return '6-10 hr/week'
    elif average_hours < 5:
        return '11-15 hr/week'
    elif average_hours < 6:
        return '16-20 hr/week'
    else:
        return '21+ hr/week'


def process_crop_and_preprocess(image, crop_coords, threshold=210 , kernel_size=1):
    # Crop the image
    cropped_image = image.crop(crop_coords)
    # Preprocess the cropped image
    return preprocess_for_tesseract(cropped_image, threshold, kernel_size)


path_to_tesseract = r"C:\Users\artur\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract 

# Define Tesseract configuration
custom_config = r'--psm 7 -c tessedit_char_whitelist=0123456789.'

results = []

#skip numbers 6,12,15
for i in range(2,54):
    if i in []:
        continue

    print("processing image", i)
    # Generate filenames dynamically
    review_path = f'ME courses/review_{i}.png'
    course_path = f'ME courses/course_{i}.png'

    review = Image.open(review_path)
    course = Image.open(course_path)

    # Crop regions for different parts of the image
    crop_coords = {
        "course": (541, 179, 820, 194),
        "students": (835, 561, 855, 577),
        "grade": (1186, 411, 1220, 426),
        "other": (900, 540 , 1425, 555),
        "hours": (1185, 628, 1220, 644)
    }
    

    # Process cropped and preprocessed images for each region
    cropped_course = course.crop(crop_coords["course"])
    cropped_students = process_crop_and_preprocess(course, crop_coords["students"])
    cropped_grade = process_crop_and_preprocess(review, crop_coords["grade"])
    cropped_hours = process_crop_and_preprocess(review, crop_coords["hours"])

    # Find number of students who don't know
    cropped_other = review.crop(crop_coords["other"]).convert("RGBA")
    pixels = cropped_other.load()
    width, height = cropped_other.size

    x_coord = 0
    for x in range(width):
        r, g, b, a = pixels[x, 5]
        if r == 172:
            x_coord = x

    if x_coord != 0:
        crop_other = cropped_other.crop((x_coord+4 , 0, x_coord + 17, height))
        #shorw crop_other
        # crop_other.show()
        
        other_text = pytesseract.image_to_string(crop_other, config=custom_config).strip()
    else:
        other_text = 0

    # OCR for grade and hours
    course_text = pytesseract.image_to_string(cropped_course, config= '--psm 7').strip()
    students_text = pytesseract.image_to_string(cropped_students, config=custom_config).strip()
    grade_text = pytesseract.image_to_string(cropped_grade, config=custom_config).strip()
    hours_text = pytesseract.image_to_string(cropped_hours, config=custom_config).strip()


    #shorw cropped images
    # cropped_students.show()
    # cropped_grade.show()
    # cropped_hours.show()



    if students_text == '':
        cropped_students = process_crop_and_preprocess(course, crop_coords["students"], threshold=220,kernel_size=1)
        students_text = pytesseract.image_to_string(cropped_students, config=custom_config).strip()
        cropped_students.show()
      
    if grade_text == '':
        cropped_grade = process_crop_and_preprocess(review, crop_coords["grade"], threshold=220,kernel_size=1)
        grade_text = pytesseract.image_to_string(cropped_grade, config=custom_config).strip()
        cropped_grade.show()
    
    if hours_text == '':
        cropped_hours = process_crop_and_preprocess(review, crop_coords["hours"], threshold=220,kernel_size=1)
        hours_text = pytesseract.image_to_string(cropped_hours, config=custom_config).strip()
        cropped_hours.show()

    if grade_text.endswith('.'):
        grade_text = grade_text[:-1]

    # Handle decimal point for grade and hours
    if float(grade_text) > 6:
        grade_text = grade_text[:1] + '.' + grade_text[1:]

    if float(hours_text) > 21:
        hours_text = hours_text[:1] + '.' + hours_text[1:]

    # Adjust average grade and convert to letter grade
    adjust_average_grade = adjust_average(int(students_text), float(grade_text), int(other_text))
    average_grade = average_grade_to_letter(adjust_average_grade)
    average_hours = average_hours_to_groups(float(hours_text))

    # Create dictionary with course average grade and hours
    course_info = {
        "course": course_text,
        "average_grade": average_grade,
        "hours": average_hours
    }

    results.append(course_info)

# print(results)

# save csv file
import csv

with open('ME courses/ME_courses.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Course", "Average Grade", "Hours"])
    for result in results:
        writer.writerow([result["course"], result["average_grade"], result["hours"]])

