import logging
import pytest
import functions

from person import Person
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


if __name__ == '__main__':
    # Logs & Pytest reports
    logging.basicConfig(filename='results/logs/1_single_person_accurate_information.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    pytest.main(["--html=results/reports/1_single_person_accurate_information.html",
                 "--json-report",
                 "--json-report-file=results/reports/1_single_person_accurate_information.json"])

    # Start of code
    try:
        logging.info("Starting '1_single_person_accurate_information' test")

        # Creates a new object of type "person" and calls a function for the
        # user to manually enter the necessary data to download their CURP
        person = Person()
        person.get_data()

        # Get access to the form on the web
        driver = functions.setup_chrome()
        driver.get("https://www.gob.mx/curp/")

        datos = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "datos"))
        )

        datos.click()

        # Calls a function that sends the necessary information to fill out
        # the form that provides access to the button to download the CURP
        functions.send_data(driver, person)

        driver.quit()

        logging.info("Finishing '1_single_person_accurate_information' test")

    except OSError as e:
        logging.error(f"OSError occurred: {e}")
        raise
    except Exception as e:
        logging.error(
            f"'1_single_person_accurate_information' test failed: {str(e)}")
        raise
