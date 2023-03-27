from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.firefox import GeckoDriverManager
import numpy as np
from bs4 import BeautifulSoup

# Set up the Firefox browser options
firefox_options = Options()
firefox_options.add_argument("--headless")  # Run Firefox in headless mode

# Initialize the WebDriver
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

# Load the page
driver.get("https://discomap.eea.europa.eu/App/AirQualityStatistics/index.html#")

# Wait for the dynamic content to load (you may need to adjust the wait time)
driver.implicitly_wait(15)

years = np.arange(2009, 2024)
countries = ['Netherlands', 'France', 'Greece', 'Germany', 'Iceland', 'Belgium', 'Luxembourg', 'Hungary']

selectYear = Select(driver.find_element(By.ID, 'ReportingYear'))
selectCountry = Select(driver.find_element(By.ID, 'Country'))
# download = driver.find_element(By.XPATH, "/button/span[contains(text(), 'Download CSV')]")
download = driver.find_elements(By.TAG_NAME, 'button')[3]
print(download.text)

for y in years:
    selectCountry.select_by_visible_text("[ all ]")
    for c in countries:
        print(f'Downloading data for {y} - {c}')

        WebDriverWait(driver, timeout=600).until(element_to_be_clickable(driver.find_element(By.ID, 'ReportingYear')))
        if not str(y) in [o.text.split(' ')[0] for o in selectYear.options]:
            continue
        selectYear.select_by_value(str(y))
        print("Selected year")

        WebDriverWait(driver, timeout=600).until(element_to_be_clickable(driver.find_element(By.ID, 'Country')))
        if not c in [o.text.split(' ')[0] for o in selectCountry.options]:
            continue 
        selectCountry.select_by_value(c)
        print("Selected country")

        WebDriverWait(driver, timeout=600).until(element_to_be_clickable(download))
        download.click() 
        print('Clicked download')



# Get the page source
html = driver.page_source

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Print the title of the page
print(soup.title.text)

# Close the WebDriver
driver.quit()