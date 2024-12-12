from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def click_and_reset(actions, x, y):
    """Perform a click at an offset and reset the cursor."""
    actions.move_by_offset(x, y).click().perform()
    actions.move_by_offset(-x, -y).perform()

def send_keys(actions, iterations, key):
    """Send a key multiple times using ActionChains."""
    for _ in range(iterations):
        actions.send_keys(key).perform()

def login_to_tableau(driver, email, password):
    """Log in to the Tableau site using provided credentials."""
    WebDriverWait(driver, 10).until(EC.url_contains('https://login.microsoftonline.com/'))
    
    # Enter email
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'loginfmt')))
    username_input = driver.find_element(By.NAME, 'loginfmt')
    username_input.send_keys(email)
    

    # Click next button
    login_button = driver.find_element(By.ID, "idSIButton9")
    login_button.click()

    time.sleep(2)

    # Enter password
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'passwd')))
    password_input = driver.find_element(By.NAME, 'passwd')
    password_input.send_keys(password)

    # Submit password
    psw_button = driver.find_element(By.ID, "idSIButton9")
    psw_button.click()

    # Wait until logged in and redirected
    WebDriverWait(driver, 40).until(EC.url_to_be('https://tableau.wpi.edu/#/site/WPICommunity/home'))

def navigate_to_report(driver, actions):
    """Navigate to the specific Tableau report."""
    driver.get('https://tableau.wpi.edu/#/site/WPICommunity/views/OSCAR/byCourse2019-Present?:iid=1')
    time.sleep(5)

    # Click on the academic year dropdown
    click_and_reset(actions, 722, 156)

    # Select academic year
    time.sleep(1)
    send_keys(actions, 7, Keys.DOWN)
    send_keys(actions, 1, Keys.ENTER)

def capture_screenshots(driver, actions, iterations=60):
    """Iterate through courses and capture screenshots of reports."""
    for iteration in range(iterations):
        # Open course dropdown
        time.sleep(1)
        click_and_reset(actions, 597, 185)

        # Search for course
        time.sleep(1)
        actions.send_keys("ME ").perform()

        # Select course
        time.sleep(1)
        send_keys(actions, iteration + 64, Keys.DOWN)
        send_keys(actions, 1, Keys.ENTER)

        # Click on the review
        time.sleep(2)
        click_and_reset(actions, 618, 220)

        # Take first screenshot
        time.sleep(2)
        driver.save_screenshot(f'course_{iteration + 1}.png')

        # Scroll down and take another screenshot
        time.sleep(2)
        send_keys(actions, 8, Keys.PAGE_DOWN)
        send_keys(actions, 2, Keys.PAGE_UP)
        time.sleep(0.5)
        driver.save_screenshot(f'review_{iteration + 1}.png')

        # Scroll back up
        time.sleep(1)
        send_keys(actions, 6, Keys.PAGE_UP)

def main():
    """Main execution function."""
    email = "yourwpiemail.edu"  # Replace with your email
    password = "youwpipassword"  # Replace with your password

    # Set up the WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()
    actions = ActionChains(driver)

    try:
        # Open Tableau site
        driver.get('https://tableau.wpi.edu/')

        # Log in
        login_to_tableau(driver, email, password)

        # Navigate to report
        navigate_to_report(driver, actions)

        # Capture screenshots
        capture_screenshots(driver, actions)

    finally:
        time.sleep(15)
        driver.quit()

if __name__ == "__main__":
    main()