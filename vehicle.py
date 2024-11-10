import pandas as pd


class Vehicle:
    def __init__(self, license, type, start_date, end_date, draft_date, release_date, payment_amount):
        self.__license = license
        self.__type = type
        self.__start_date = start_date
        self.__end_date = end_date
        self.__draft_date = draft_date
        self.__release_date = release_date
        self.__payment_amount = payment_amount


    def get_license(self):
        return self.__license


    def get_type(self):
        return self.__type


    def get_start_date(self):
        if pd.isna(self.__start_date):
            return pd.NA
        return self.__start_date.strftime('%d/%m/%Y')


    def get_end_date(self):
        if pd.isna(self.__end_date):
            return pd.NA
        return self.__end_date.strftime('%d/%m/%Y')


    def get_draft_date(self):
        if pd.isna(self.__draft_date):
            return pd.NA
        return self.__draft_date.strftime('%d/%m/%Y')


    def get_release_date(self):
        if pd.isna(self.__release_date):
            return pd.NA
        return self.__release_date.strftime('%d/%m/%Y')


    def get_payment_amount(self):
        return "{:,}".format(self.__payment_amount)


    def get_message(self):
        msg = ""
        msg +=  "חשבונית מס עבור כלי מס' רישוי:" + " " +  f"{self.get_license()} - {self.get_type()}" + "\n"
        if not pd.isna(self.get_release_date()):
            msg += "שוחרר בתאריך:" + " " + f"{self.get_release_date()}" + "\n"
        msg += "תשלום עבור תאריכים:" + " " f"{self.get_start_date()} - {self.get_end_date()}" + " " + "(נדרש לציין על גבי החשבונית)" + "\n"
        msg += 'סכום לתשלום לא כולל מע"מ:' + " " + f"{self.get_payment_amount()}" + " " + 'ש"ח'
        return msg