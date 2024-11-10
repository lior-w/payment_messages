class ID_list:
    def __init__(self, df, header, msg):
        self.__df = df
        self.__header = header
        self.__msg = msg

    def get_df(self):
        return self.__df
    
    def get_header(self):
        return self.__header
    
    def get_msg(self):
        return self.__msg