from vehicle import Vehicle
import pandas as pd


class Owner:
    def __init__(self, df, id_lists):
        self.df = df
        self.id_lists = id_lists
        self.__id = self.df["id"].iloc[0]
        self.__name = self.df["owner_name"].iloc[0]
        self.__vehicles = self.generate_vehicles()


    def generate_vehicles(self):
        vehicles = []
        for _, row in self.df.iterrows():
            vehicle = Vehicle(
                license=row["license"],
                type=row["type"],
                start_date=row["pay_from_date"],
                end_date=row["pay_until_date"],
                draft_date=row["draft_date"],
                release_date=row["release_date"],
                payment_amount=row["payment_amount"]
            )
            vehicles.append(vehicle)
        return vehicles


    def number_of_vehicles(self):
        return len(self.__vehicles)


    def get_df(self):
        columns = {"id": "ח.פ",
                   "owner_name": "בעלים",
                   "license": "מספר רישוי",
                   "type": "סוג כלי",
                   "draft_date": "תאריך גיוס",
                   "release_date": "תאריך שחרור",
                   "pay_from_date": "תשלום מתאריך",
                   "pay_until_date": "תשלום עד תאריך",
                   "payment_amount": 'סכום לתשלום ללא מע"מ'}
        _df = self.df[list(columns.keys())]
        _df = _df.rename(columns=columns)
        return _df
    
    def has_sapak(self):
        return len(self.df[pd.notna(self.df["sapak"])]) > 0
        

    def get_message(self, sapak_bool):
        header = "שלום רב," + "\n\n"
        if not self.has_sapak() and sapak_bool:
            header += ('מצ"ב רשימת הכלים אשר גויסו כולל הסכום לתשלום עבור כל כלי.' + "\n"
                       + "עליך להמציא:")
        else:
            header += ("אנו מקדמים תשלום נוסף עבור הכלים המגויסים." + " "
                        + "לצורך כך אודה לקבלת חשבונית עבור הכלים על פי הפרטים הבאים בקובץ PDF:")
            
            
        body = ""
        for i, v in enumerate(self.__vehicles):
            if i > 0:
                body += "\n\n"
            body += f"{i + 1}) {v.get_message()}"
        
        first_time = ""
        if not self.has_sapak() and sapak_bool:
            first_time += ("\n\n" + "יש צורך להוציא עבור כל כלי חשבונית מס נפרדת עבור משרד הביטחון." + " "
                              + "(משרד הביטחון, ח.פ 500100581)" + "\n"
                              + 'יש להוסיף מע"מ, הסכומים הם לא כולל מע״מ.' + "\n\n"
                              + "בנוסף, עליך להעביר אלינו:" + "\n"
                              + "1) אישור ניכוי מס במקור (אחרת ירד אוטומטית 30% מס)" + "\n"
                              + "2) אישור ניהול ספרים" + "\n"
                              + "3) אישור ניהול חשבון" + "\n"
                              + "4) במידה ומדובר בעוסק מורשה, יש לצרף תעודת עוסק מורשה" + "\n"
                              + "5) במידה ומדובר בחברה, יש לצרף אישור מרשות התאגידים על קיום החברה" + "\n"
                              + "6) מצורף טופס, אודה לחתימתך (כולל חותמת החברה)" + "\n\n"
                              + "יש לשלוח את האישורים בהקדם האפשרי לוואטסאפ הזה על מנת לזרז את תהליך העברת התשלום." + "\n"
                              + "(מספר וואטסאפ 050-3348120)")

        list_msg = ""
        for lst in self.id_lists:
            list_msg += "\n\n"
            list_msg += lst.get_msg()
            print(self.get_name() + lst.get_msg())

        final_section = "\n\n" + 'יחידת אג"ד לאו"ם, גיוס כלי צמ"ה ומלגזות.'

        return header + "\n\n" + body + first_time + list_msg + final_section


    def get_id(self):
        return self.__id


    def get_name(self):
        return self.__name


    def get_vehicles(self):
        return self.__vehicles


    def set_vehicles(self, vehicles):
        self.__vehicles = vehicles


    def add_vehicle(self, vehicle):
        self.__vehicles.append(vehicle)