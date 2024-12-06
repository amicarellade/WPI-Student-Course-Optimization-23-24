import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(options=chrome_options)

def accept_cookies():
    """Accept cookies on the RateMyProfessors website."""
    try:
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.CCPAModal__StyledCloseButton-sc-10x9kq-2"))
        )
        cookie_button.click()
        print("Cookies accepted.")
    except Exception as e:
        print("No cookie consent button found or already accepted:", e)

def get_professor_info(professor_name):
    """Retrieve professor information from RateMyProfessors."""
    try:
        
        base_url = "https://www.ratemyprofessors.com/search/professors/1220"
        search_url = f"{base_url}?q={professor_name.replace(' ', '%20')}"
        print(f"Navigating to search URL: {search_url}")
        driver.get(search_url)
        
        
        accept_cookies()
        
        
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
            
            # Extract rating
            try:
                rating_div = card.find_element(By.CSS_SELECTOR, "div.CardNumRating__CardNumRatingNumber-sc-17t4b9u-2")
                rating = rating_div.text
                print(f"  - Rating: {rating}")
            except Exception:
                rating = "No rating available"
                print("  - Rating not available.")
            
            # Extract "would take again" percentage
            try:
                take_again_div = card.find_elements(By.CSS_SELECTOR, "div.CardFeedback__CardFeedbackItem-lq6nix-1")[0]
                take_again_percentage = take_again_div.find_element(By.CSS_SELECTOR, "div.CardFeedback__CardFeedbackNumber-lq6nix-2").text
                print(f"  - Would Take Again: {take_again_percentage}")
            except Exception:
                take_again_percentage = "N/A"
                print("  - 'Would Take Again' not available.")
            
            # Extract level of difficulty
            try:
                difficulty_div = card.find_elements(By.CSS_SELECTOR, "div.CardFeedback__CardFeedbackItem-lq6nix-1")[1]
                difficulty_level = difficulty_div.find_element(By.CSS_SELECTOR, "div.CardFeedback__CardFeedbackNumber-lq6nix-2").text
                print(f"  - Level of Difficulty: {difficulty_level}")
            except Exception:
                difficulty_level = "N/A"
                print("  - Level of Difficulty not available.")
            
            # Return all extracted data
            return {
                "Professor Name": prof_name,
                "Rating": rating,
                "Would Take Again": take_again_percentage,
                "Difficulty": difficulty_level
            }
        
        print("No matching professor found.")
        return {
            "Professor Name": professor_name,
            "Rating": "Professor not found at WPI",
            "Would Take Again": "N/A",
            "Difficulty": "N/A"
        }
    
    except Exception as e:
        print(f"Error processing professor {professor_name}: {e}")
        return {
            "Professor Name": professor_name,
            "Rating": "Error",
            "Would Take Again": "Error",
            "Difficulty": "Error"
        }

# Load the previous CSV if it exists
output_file = "courses_and_professors_with_ratings.csv"
try:
    df = pd.read_csv(output_file)
    print(f"Loaded existing CSV file: {output_file}")
except FileNotFoundError:
    print(f"No previous CSV found. Starting fresh.")
    df = pd.DataFrame(columns=["Course Number", "Course Name", "Professor", "Rating", "Would Take Again", "Difficulty"])


not_found_df = df[df["Rating"] == "Professor not found at WPI"]


for index, row in not_found_df.iterrows():
    professor_name = row["Professor"]
    print(f"Retrying to fetch data for Professor: {professor_name}")
    data = get_professor_info(professor_name)
    df.at[index, "Rating"] = data["Rating"]
    df.at[index, "Would Take Again"] = data["Would Take Again"]
    df.at[index, "Difficulty"] = data["Difficulty"]

# Save the updated data back to the CSV
df.to_csv(output_file, index=False)
print(f"Updated data saved to {output_file}")


driver.quit()
