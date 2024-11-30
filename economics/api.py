import re
import pandas as pd
from requests import get
from pandas import DataFrame
from datetime import datetime


class EconomicsAPI():


    # PARAMETERS
    INDICATORS_DICT : dict = {
        "UF": "uf",
        "UTM": "utm",
        "IMC": "imacec",
        "IPC": "ipc",
        "BTC": "bitcoin",
        "USD": "dolar",
        "USDI": "dolar_intercambio",
        "EU": "euro",
        "TPM": "tpm",
        "TD": "tasa_desempleo",
        "IVP": "ivp",
        "LC": "libra_cobre",
    }

    INDICATORS_INVERSE : dict

    BASE_URL : str = "https://mindicador.cl/api/%s/%s"
    DEFAULT_INDICATOR : str
    DEFAULT_YEAR : int
    DEFAULT_DATE : str



    # CONSTRUCTOR

    def __init__(self):
        """ 
        CONSTRUCTOR
        -----------
        DEFAULT_INDICATOR : String = Sets to "UF".
        DEFAULT_YEAR : Integer = Sets to current year with datetime.now().
        DEFAULT_DATE : String = Sets to current day [dd-mm-yyyy] with datetime.now().
        """
        self.DEFAULT_INDICATOR = self.INDICATORS_DICT["UF"]
        self.DEFAULT_YEAR = datetime.now().year
        self.DEFAULT_DATE = datetime.now().strftime("%d-%m-%Y")
        self.INDICATORS_INVERSE = {v: k for k, v in self.INDICATORS_DICT.items()}
        


    # CLASS METHODS

    # get indicator value by year
    def indicator_year(
            self,
            indicator : str = None,
            year : int = None,
        ) -> DataFrame | None:

        """ 
        Indicator Year
        --------------
        indicator : String = Any value from INDICATORS_DICT. Incorrect indicator falls to
        DEFAULT_INDICATOR.
        year : Integer = Any year that's prior or current year.

        Returns pandas.DataFrame with yearly values of selected indicator (or None).
        """
    
        # parameters
        indicator, year = self.get_valid_parameters(indicator, year)

        # get petition
        url = self.BASE_URL % (indicator, year)
        response = get(url = url)

        # return data
        if response.status_code == 200:
            data = response.json()["serie"]
            return DataFrame(data = data)
        
        return None
    


    # get indicator value by specific date [dd-mm-yyyy]
    def indicator_day(
            self,
            indicator : str = None,
            date : str = None
        ) -> DataFrame | None:

        """ 
        Indicator Day
        --------------
        indicator : String = Any value from INDICATORS_DICT. Incorrect indicator falls to
        DEFAULT_INDICATOR.
        date : String = Any date that's prior or current date.

        Returns pandas.DataFrame with day value of selected indicator (or None).
        """

        # parameters
        indicator = self.get_valid_indicator(indicator)
        date = self.get_valid_date(date)

        # get petition
        url = self.BASE_URL % (indicator, date)
        response = get(url = url)

        # return data
        if response.status_code == 200:
            data = response.json()["serie"]

            return DataFrame(data = data)
        
        return None


    # get indicator current value
    def indicator_current(
            self,
            indicator : str = None,
            year : int = None
        ) -> DataFrame | None:

        """ 
        Indicator Current Value
        -----------------------
        indicator : String = Any value from INDICATORS_DICT. Incorrect indicator falls to
        DEFAULT_INDICATOR.
        year : Integer = Any year that's prior or equal to current year.

        Returns pandas.DataFrame with day value of selected indicator (or None).
        """

        # parameters
        if indicator == "USDI" :
            url = f"https://mindicador.cl/api/{self.INDICATORS_DICT[indicator]}/"

        else:
            indicator, year = self.get_valid_parameters(indicator, year)
            url = self.BASE_URL % (indicator, year)
                
        # get petition
        response = get(url = url)
        print(response.status_code)

        # response
        if response.status_code == 200:
            data = response.json()["serie"][0]
            data["indicador"] = indicator if indicator != "USDI" else self.INDICATORS_DICT[indicator]
            data["sigla"] = self.INDICATORS_INVERSE[indicator] if indicator != "USDI" else "USDI"

            return data

        return None

    
    # get valid parameters
    def get_valid_parameters(
            self,
            indicator : str = None,
            year : int = None
        ) -> tuple :

        """ 
        Get Valid Parameters
        --------------------
        indicator : String = Indicator to check.
        year : Integer = Year to check.

        Returns tuple with valid indicator and year.
        """

        # parameters        
        valid_indicator = indicator and indicator in self.INDICATORS_DICT
        valid_year = year and year <= datetime.now().year

        indicator = self.INDICATORS_DICT[indicator] if valid_indicator else self.DEFAULT_INDICATOR
        year = str(year if valid_year else self.DEFAULT_YEAR)
        
        # return
        return (indicator, year)
    
    
    
    # get valid indicator
    def get_valid_indicator(
            self,
            indicator : str = None
        ) -> str:

        """ 
        Get Valid Indicator
        --------------------
        indicator : String = Indicator to check.

        Returns valid indicator.
        """

        # check
        valid_indicator = indicator and indicator in self.INDICATORS_DICT
        indicator = self.INDICATORS_DICT[indicator] if valid_indicator else self.DEFAULT_INDICATOR
        
        # return
        return indicator



    # get valid date
    def get_valid_date(
            self,
            date : str = None
        ) -> str:

        """ 
        Get Valid Date
        --------------------
        date : String = Date to check.

        Returns valid date.
        """

        # check   
        pattern = r"\b\d{2}-\d{2}-\d{4}\b"
        valid_date = date and bool(re.match(pattern, date))

        # return
        date = date if valid_date else self.DEFAULT_DATE
        return date



    # tostring
    def __str__(self) -> str:
        return (f"{self.DEFAULT_INDICATOR}\n{self.DEFAULT_YEAR}\n{self.DEFAULT_DATE}")

