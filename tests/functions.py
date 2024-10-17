import os
import time
import openpyxl
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_chrome():
    """
    Sets up a Chrome browser instance with specific options to avoid being
    discovered by an anti-bot and define in which folder the CURPS will be
    downloaded

    Returns:
        uc.Chrome: The Chrome browser object initialized with the specified options
    """
    # Get the folder path where script is located, then go one level up
    parent_directory = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))

    # Create the CURPS folder if it does not exist
    download_folder = os.path.join(parent_directory, "CURPS")
    os.makedirs(download_folder, exist_ok=True)

    # Using the "uc" tool helps avoid detection by anti-bot mechanisms.
    # It also sets the download folder.
    chrome_options = uc.ChromeOptions()
    prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,      # Do not ask where to save
    }
    chrome_options.add_experimental_option("prefs", prefs)

    return uc.Chrome(options=chrome_options)


def send_data(driver, person):
    """
    Uses collected user info to fill out a form and download the CURP
    
    Args:
        driver (WebDriver): The browser instance to navigate and interact with the web page
        person (Person): An instance of the Person class containing user information

    Returns:
        None
    """

    driver.find_element(By.ID, "nombre").send_keys(person.name)
    driver.find_element(By.ID, "primerApellido").send_keys(
        person.first_lastname)
    driver.find_element(By.ID, "segundoApellido").send_keys(
        person.second_lastname)
    driver.find_element(By.ID, "diaNacimiento").send_keys(person.day)
    driver.find_element(By.ID, "mesNacimiento").send_keys(person.month)
    driver.find_element(By.ID, "selectedYear").send_keys(person.year)
    driver.find_element(By.ID, "sexo").send_keys(person.sex)
    driver.find_element(By.ID, "claveEntidad").send_keys(person.state)

    driver.find_element(By.ID, "searchButton").click()

    download = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "download"))
    )
    download.click()


def get_excel_data(file):
    """
    Loads data from an Excel file.
    
    Args:
        file (str): Path to the Excel file

    Returns:
        data: List of lists of all rows in the Excel file with information
    """
    excel_dataframe = openpyxl.load_workbook(file)
    dataframe = excel_dataframe.active

    data = []

    for row in dataframe.iter_rows(min_row=2, max_col=6, values_only=True):
        # If at least 1 cell in the "row" has information, add the row to "data"
        if any(row):
            data.append(list(row))

    return data


def wait_for_download(directory, initial_count, timeout=30):
    """
    Wait a certain amount of time for the document to download. To check if it
    was downloaded, compare how many files there were before starting the
    download with the number of files in the directory that is updated every
    second

    Args:
        directory (str): The directory to check for downloaded files
        initial_count (int): The initial number of files in the directory
        timeout (int, optional): Max time to wait. Defaults to 30

    Returns:
        boolean: True = "Download successful"  False = "Download failed"
    """
    seconds = 0

    while seconds < timeout:
        time.sleep(1)
        current_count = len(os.listdir(directory))
    
        if current_count > initial_count:
            return True
        seconds += 1
    
    return False
