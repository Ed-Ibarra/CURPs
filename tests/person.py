from datetime import datetime

"""
This module contains the Person class, which represents an individual with
attributes such as name, first and second last names, birthday, sex and state.

The Person class is used for managing user information and is essential for
filling out forms to generate CURP documents.

Attributes:
    name (str): The first name of the person.
    first_lastname (str): The first last name of the person.
    second_lastname (str): The second last name of the person.
    birthday (str): The birth date of the person.
    sex (str): The sex of the person.
    state (str): The state of the person.
"""
class Person:
    def __init__(self, name="", first_lastname="", second_lastname="",
                 birthday="", sex="", state=""):
        self.name = name
        self.first_lastname = first_lastname
        self.second_lastname = second_lastname
        
        if isinstance(birthday, str) and birthday != "":
            self.birthday = datetime.strptime(birthday, "%m/%d/%Y")
        else:
            self.birthday = birthday
            
        self.sex = sex
        self.state = state
        
        
    def get_data(self):
        """
        Asks the user for their personal information

        Returns:
            None
        """
        self.name = input(
            "Please enter your name(s) separated by single whitespace: "
            )
        self.first_lastname = input("Please enter your first lastname: ")
        self.second_lastname = input("Please enter your second lastname: ")
        self.birthday = self._get_birthday()
        self.sex = self._get_sex()
        print("")
        self.state = self._get_state()
        
        
    def _get_birthday(self):
        """
        Request the date of birth with a specific format, so you can extract
        the day, month and year

        Returns:
            birthday: Date of birth with datetime.datetime format
        """
        while True:
            try:
                birthday = input("Date of birth (MM/DD/YYYY): ")
                if datetime.strptime(birthday, "%m/%d/%Y"):
                    return datetime.strptime(birthday, "%m/%d/%Y")
                
            except ValueError:
                print(
                    "\nYou enter a invalid date of birth. Please, try again!\n"
                    )

            
    def _get_sex(self):
        """
        Request the sex of the user

        Returns:
            sex: User's sex
        """
        while True:
            sex = input("Mujer (M) | Hombre (H) | No binario (N): ").upper()
            
            if sex in ["M", "H", "N"]:
                return sex
            else:
                print("\nWARNING: Please type just a single letter!")

            
    def _get_state(self):
        """
        Shows every state of Mexico and asks the user to type theirs,
        until they write it in its entirety

        Returns:
            state: User's state
        """
        while True:
            for state in states:
                print(f"{state.upper()}", end = ' | ')
                
            state = input("\nState: ").lower()
            
            if state not in states:
                print("\nInvalid option. Please, try again!\n")
            else:
                return state
                
    # Below properties will be used to extract its data from datetime variable
    @property
    def day(self):
        return f"{self.birthday.day:02d}" if self.birthday else None
    
    @property
    def month(self):
        return f"{self.birthday.month:02d}" if self.birthday else None
    
    @property
    def year(self):
        return self.birthday.year if self.birthday else None
        
        
states = ["aguascalientes",
          "baja california",
          "baja california sur",
          "campeche",
          "coahuila",
          "colima",
          "chiapas",
          "chihuahua",
          "ciudad de mexico",
          "durango",
          "guanajuato",
          "guerrero",
          "hidalgo",
          "jalisco",
          "estado de mexico",
          "michoacan",
          "morelos",
          "nayarit",
          "nuevo leon",
          "oaxaca",
          "puebla",
          "queretaro",
          "quintana roo",
          "san luis potosi",
          "sinaloa",
          "sonora",
          "tabasco",
          "tamaulipas",
          "tlaxcala",
          "veracruz",
          "yucatan",
          "zacatecas",
          "nacido en el extranjero"]