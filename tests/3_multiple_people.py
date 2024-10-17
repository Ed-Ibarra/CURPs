import logging
import pytest
import os
import functions

from person import Person
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if __name__ == '__main__':
    # Logs & Pytest reports
    logging.basicConfig(filename='results/logs/3_multiple_people.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    pytest.main(["--html=results/reports/3_multiple_people.html",
                 "--json-report",
                 "--json-report-file=results/reports/3_multiple_people.json"])

    # Start of code
    try:
        logging.info("Starting '3_multiple_people' test")

        downloaded_users = []
        download_failed = []
        data = functions.get_excel_data("people.xlsx")

        # Start iterating on the data obtained from the Excel file: entry = row
        for i, entry in enumerate(data, start=2):
            # If there is a NONE value in any field in the row, create a
            # warning in the logs to inform where the error is and append the
            # user's full name. If there is a NONE value, fill it with "(empty)".
            if None in entry:
                logging.warning(
                    f"There is at least one missing value in row number {i} of "
                    f"the Excel file. So, the CURP couldn't be downloaded."
                    )
                download_failed.append(
                    f"{entry[0] if entry[0] != None else "(empty)"} "
                    f"{entry[1] if entry[1] != None else "(empty)"} "
                    f"{entry[2] if entry[2] != None else "(empty)"} "
                    )
                
            else:
                # Create a new object using the row's information
                person = Person(name=entry[0],
                                first_lastname=entry[1],
                                second_lastname=entry[2],
                                birthday=entry[3],
                                sex=entry[4],
                                state=entry[5])

                # Get access to the form on the web
                driver = functions.setup_chrome()
                driver.get("https://www.gob.mx/curp/")

                datos = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "datos"))
                )

                datos.click()

                # Calls a function that sends the necessary information to fill
                # out the form that provides access to the button to download
                # the CURP
                functions.send_data(driver, person)
                
                full_name = f"{person.name} {person.first_lastname} {person.second_lastname}"
                
                # Calls a function that waits a certain amount of time for the
                # document to download, as the case may be, add a log with the
                # appropriate information and save the user's name to notify
                # later whether or not it was possible to download their CURP
                download_directory = "CURPS"
                
                if functions.wait_for_download(download_directory, len(os.listdir(download_directory))):
                    downloaded_users.append(full_name)
                    logging.info(
                        f"{full_name}'s CURP was successfully downloaded")
                else:
                    download_failed.append(full_name)
                    logging.warning(
                        f"{full_name}'s CURP could not be downloaded")
                    
        # Results log
        # If every CURP was downloaded
        if len(data) == len(downloaded_users):
            log = f"\nAll CURPs were successfully downloaded:"
        # If no document was downloaded
        elif len(data) == len(download_failed):
            log = f"\nNo CURP could be downloaded"
        else:
            # If some CURPs were downloaded, must specify which ones are and
            # which are not
            log = f"\nCURPs successfully downloaded: "
            log += f"{len(downloaded_users)}/{len(data)}\n"
            for i, user in enumerate(downloaded_users, start=1):
                log += f"{i}- {user}\n"
        
            log += f"\nMissing CURPs:"
            log += f"{len(download_failed)}/{len(data)}\n"
            for i, user in enumerate(download_failed, start=1):
                log += f"{i}- {user}\n"
                
        logging.info(log)
        logging.info("Finishing '3_multiple_people' test")
        

    except Exception as e:
        logging.error(
            f"'1_single_person_accurate_information' test failed: {str(e)}")
        raise