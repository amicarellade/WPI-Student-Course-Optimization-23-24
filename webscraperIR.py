from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv

# Set the path to your ChromeDriver
chrome_driver_path = r'C:\Users\sapna\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'

# Initialize the WebDriver using the Service class
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

try:
    # Open Workday login page
    driver.get('https://workday.wpi.edu/')  # Replace with actual Workday URL

    # Wait for manual login
    print("Please log in manually. The script will resume after 60 seconds.")
    time.sleep(30)  # Wait for you to log in

    # Navigate to the courses page
    courses_page_url = 'https://wd5.myworkday.com/wpi/d/task/3005$3860.htmld'  # Replace with actual courses page URL
    driver.get(courses_page_url)
    print("Please add information manually. The script will resume after 60 seconds.")
    time.sleep(70)  # Wait for the page to load
    print("Script executing")
    # Lists to store extracted data
    courses = []
    professors = []

    # Start scrolling to load all elements
    while True:
        # Extract all currently visible courses and professors
        course_elements = driver.find_elements(By.XPATH, '//div[@data-automation-id="promptOption"]')  # XPath for courses
        professor_elements = driver.find_elements(By.XPATH, '//span[@data-automation-id="compositeSubHeaderOne"]')  # XPath for professors

        # Add the text from each element to respective lists (without stripping)
        courses.extend([course.text for course in course_elements if course.text])  # Add course text
        professors.extend([prof.text for prof in professor_elements if prof.text])  # Add professor text

        print(f"Currently found {len(courses)} courses and {len(professors)} professors.")  # Debugging step

        # Scroll to the bottom of the page to load more elements
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Allow time for new elements to load

        # Check if new elements have been loaded
        new_course_elements = driver.find_elements(By.XPATH, '//div[@data-automation-id="promptOption"]')
        new_professor_elements = driver.find_elements(By.XPATH, '//span[@data-automation-id="compositeSubHeaderOne"]')

        if len(new_course_elements) == len(course_elements) and len(new_professor_elements) == len(professor_elements):
            # No new elements loaded, stop scrolling
            print("All elements loaded.")
            break

    # Save courses to a CSV file
    with open('all_courses_spring.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['course'])
        for course in courses:
            writer.writerow([course])

    # Save professors to a CSV file
    with open('all_professors_spring.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['professor'])
        for professor in professors:
            writer.writerow([professor])

    print("Scraping complete. Data saved to 'all_courses_spring.csv' and 'all_professors_spring.csv'.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
