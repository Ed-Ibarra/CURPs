import logging
import pytest
import time
import os
import undetected_chromedriver as uc
import pandas as pd


from person import Person, states
import functions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import openpyxl


if __name__ == '__main__':
    # Logs & Pytest reports
    # logging.basicConfig(filename='results/logs/1_single_person_accurate_information.log',
    #                 level=logging.INFO,
    #                 format='%(asctime)s - %(levelname)s - %(message)s')

    # pytest.main(["--html=results/reports/1_single_person_accurate_information.html",
    #              "--json-report",
    #              "--json-report-file=results/reports/1_single_person_accurate_information.json"])

    # Start of code
    try:
        logging.info("Starting '3_multiple_people' test")

        driver = functions.setup_chrome()
        data = functions.get_excel_data("people.xlsx")
        download_directory = "CURPS"

        for entry in data:
            if None in entry:
                # print(f"There is at least one missing value in the next entry: {entry}")
                logging.warning(
                    f"There is at least one missing value in the next entry: {entry}")
            else:

                person = Person(name=entry[0],
                                first_lastname=entry[1],
                                second_lastname=entry[2],
                                birthday=entry[3],
                                sex=entry[4],
                                state=entry[5])

                driver.get("https://www.gob.mx/curp/")

                datos = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "datos"))
                )

                datos.click()

                functions.send_data(driver, person)

                if functions.wait_for_download(download_directory, len(os.listdir(download_directory))):
                    logging.info(f"{person.name +
                                 person.first_lastname +
                                 person.second_lastname}'s "
                                 "CURP was successfully downloaded")
                else:
                    logging.warning(f"{person.name +
                                 person.first_lastname +
                                 person.second_lastname}'s "
                                 "CURP could not be downloaded")

        logging.info("Finishing '3_multiple_people' test")

    except Exception as e:
        # logging.error(f"'1_single_person_accurate_information' test failed: {str(e)}")
        raise
