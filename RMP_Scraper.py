import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium WebDriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(options=chrome_options)

def accept_cookies():
    try:
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.CCPAModal__StyledCloseButton-sc-10x9kq-2"))
        )
        cookie_button.click()
        print("Cookies accepted.")
    except Exception as e:
        print("No cookie consent button found or already accepted:", e)

def get_professor_info(professor_name):
    try:
        # Navigate to the search page
        search_url = f"https://www.ratemyprofessors.com/search/professors?q={professor_name.replace(' ', '%20')}"
        print(f"Navigating to search URL: {search_url}")
        driver.get(search_url)
        
        # Accept cookies if prompted
        accept_cookies()
        
        # Wait for the results container
        print("Waiting for search results container...")
        results_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.SearchResultsPage__StyledResultsWrapper-vhbycj-3"))
        )
        print("Found search results container.")
        
        # Get all teacher cards
        teacher_cards = results_container.find_elements(By.CSS_SELECTOR, "a.TeacherCard__StyledTeacherCard-syjs0d-0")
        print(f"Found {len(teacher_cards)} teacher cards.")
        
        for index, card in enumerate(teacher_cards):
            print(f"Processing teacher card #{index + 1}...")
            
            # Extract professor name
            name_div = card.find_element(By.CSS_SELECTOR, "div.CardName__StyledCardName-sc-1gyrgim-0")
            prof_name = name_div.text
            print(f"  - Professor Name: {prof_name}")
            
            # Extract school name
            school_div = card.find_element(By.CSS_SELECTOR, "div.CardSchool__School-sc-19lmz2k-1")
            school_name = school_div.text
            print(f"  - School Name: {school_name}")
            
            # Check if this is the correct professor
            if "Worcester Polytechnic Institute" in school_name:
                print("  - Match found for WPI!")
                try:
                    # Extract rating
                    rating_div = card.find_element(By.CSS_SELECTOR, "div.CardNumRating__CardNumRatingNumber-sc-17t4b9u-2")
                    rating = rating_div.text
                    print(f"  - Rating: {rating}")
                except Exception as e:
                    rating = "No rating available"
                    print("  - Rating not available.")
                
                try:
                    # Extract "would take again" percentage
                    take_again_div = card.find_elements(By.CSS_SELECTOR, "div.CardFeedback__CardFeedbackItem-lq6nix-1")[0]
                    take_again_percentage = take_again_div.find_element(By.CSS_SELECTOR, "div.CardFeedback__CardFeedbackNumber-lq6nix-2").text
                    print(f"  - Would Take Again: {take_again_percentage}")
                except Exception as e:
                    take_again_percentage = "N/A"
                    print("  - 'Would Take Again' not available.")
                
                try:
                    # Extract level of difficulty
                    difficulty_div = card.find_elements(By.CSS_SELECTOR, "div.CardFeedback__CardFeedbackItem-lq6nix-1")[1]
                    difficulty_level = difficulty_div.find_element(By.CSS_SELECTOR, "div.CardFeedback__CardFeedbackNumber-lq6nix-2").text
                    print(f"  - Level of Difficulty: {difficulty_level}")
                except Exception as e:
                    difficulty_level = "N/A"
                    print("  - Level of Difficulty not available.")
                
                # Return all extracted data
                return {
                    "Rating": rating,
                    "Would Take Again": take_again_percentage,
                    "Difficulty": difficulty_level
                }
        
        print("No matching professor found at WPI.")
        return {
            "Rating": "Professor not found at WPI",
            "Would Take Again": "N/A",
            "Difficulty": "N/A"
        }
    
    except Exception as e:
        print(f"Error processing professor {professor_name}: {e}")
        return {
            "Rating": "Error",
            "Would Take Again": "Error",
            "Difficulty": "Error"
        }

# Load the CSV and iterate through professors
df = pd.read_excel("courses_professors23_24.xlsx", engine='openpyxl')  


# Create columns for each field
df["Rating"] = None
df["Would Take Again"] = None
df["Difficulty"] = None

# Populate the fields
for index, row in df.iterrows():
    professor_name = row["Professor"]
    print(f"Fetching data for Professor: {professor_name}")
    data = get_professor_info(professor_name)
    df.at[index, "Rating"] = data["Rating"]
    df.at[index, "Would Take Again"] = data["Would Take Again"]
    df.at[index, "Difficulty"] = data["Difficulty"]

# Save the updated CSV
output_file = "courses_and_professors_with_ratings.csv"
df.to_csv(output_file, index=False)
print(f"Data saved to {output_file}")

# Close the driver
driver.quit()
