# GETTING CURP DOCUMENT

## Summary
CURP is a registration document that is assigned to all people living in Mexico, as well as Mexicans residing abroad.

This project aims to automate the obtaining of the official CURP document in different scenarios using test automation tools.

## TEST SCENARIOS
1. **Get the document for a single person with accurate information**:
   - The data will be entered manually into the console and then the search will be done on the web.

2. **Get the document for a single person with erroneous data**:
   - The data will be entered manually into the console and later the search will be done on the web.

3. **Get the document for multiple people**:
   - The data will be taken from an Excel file with the information within this.

4. **Get the document for a person with partially correct data**:
   - Enter partially correct data and verify the system response.

5. **Validate the format of the data entered**:
   - Test with data that does not comply with the expected format and verify that the system properly handles these errors.

6. **Simulate multiple simultaneous requests**:
   - Send multiple requests at the same time to check how the system handles the load.

7. **Test with data from deceased people**:
   - Enter data on deceased people and verify how the system responds.

8. **Verificar la respuesta del sistema ante la falta de conexión a internet**:
   - Verify the system's response to the lack of internet connection.

9. **Test with different browsers and devices**:
   - Verify that the system works correctly on different browsers and devices.

## Technologies used
- **Python**: 3.12.4 as a programming language
- **Selenium**: For test automation in web browsers.
- **Excel**: For test data management.