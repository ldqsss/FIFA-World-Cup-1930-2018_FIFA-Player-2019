# encoding: utf-8
# @file : data_cleansing.py
# @software : PyCharm
# @author : Ading
# Official Account: AdingBLOG
import os

import pandas as pd


def unit_conversion(valueStr):
    valueStr = str(valueStr)
    idxOfM = valueStr.find('M')
    idxOfK = valueStr.find('K')
    if idxOfM != -1 and idxOfK != -1:
        return int(float(valueStr[:idxOfM]) * 1e6 + float(valueStr[idxOfM + 1:idxOfK]) * 1e3)
    elif idxOfM != -1 and idxOfK == -1:
        return int(float(valueStr[:idxOfM]) * 1e6)
    elif idxOfM == -1 and idxOfK != -1:
        return int(float(valueStr[idxOfM + 1:idxOfK]) * 1e3)
    elif idxOfM == -1 and idxOfK == -1:
        return float(valueStr)


class DataCleansing:
    """
    only cleans csv file
    """

    def __init__(self, filePath=''):
        self.__select_dimension = []
        self.__fileName = filePath
        if self.__fileName != '':
            self.df = pd.read_csv(filePath)
        else:
            self.df = None

    @property
    def fileName(self):
        return self.__fileName

    @fileName.setter
    def fileName(self, value):
        if value == '' or value is None:
            raise ValueError("value is None or empty")
        self.__fileName = value
        self.df = pd.read_csv(self.__fileName )

    @property
    def select_dimension(self):
        return self.__select_dimension

    @select_dimension.setter
    def select_dimension(self, select_dimension):
        if not isinstance(select_dimension, list):
            raise ValueError("select_dimension must be a list")
        self.__select_dimension = select_dimension

    def glance(self):
        """
        take a glace at the data
        :return:
        """
        print(self.df.sample(4))

    def export_csv(self, fileName):
        if not self.__select_dimension:
            raise NotImplementedError("You should assign select_dimension")
        if "cleansed" not in os.listdir("./data"):
            os.mkdir("./data/cleansed")
        fileName = "./data/cleansed/" + fileName
        self.df.to_csv(fileName, float_format="%.2f", columns=self.__select_dimension, index=False, encoding="utf-8")

    def show_columns(self):
        print(self.df.columns)

    def data_clean(self, str_, column):
        """
        remove str_ in a field of a record
        :param str_: the string to be removed
        :return:
        """
        self.df[column] = self.df[column].map(lambda x: str(x).lstrip(str_).rstrip(str_))
        print(self.df[column])

    def data_replace(self, str_from, str_to, column):
        """
        :param str_from:
        :param str_to:
        :param colomn:
        :return:
        """
        self.df[column] = self.df[column].map(lambda x: str(x).replace(str_from, str_to))
        print(self.df[column])

    def str_to_value(self, column):
        if isinstance(column, list):
            for col in column:
                self.df[col] = self.df[col].map(lambda x: unit_conversion(x))
            return
        self.df[column] = self.df[column].map(lambda x: unit_conversion(x))

    def add_dimension(self, dimens_add: list, add_value):
        if dimens_add:
            for dimen in dimens_add:
                self.df[dimen] = add_value
                print(add_value)
        else:
            raise ValueError("dimens_add is None or Empty")

    def read_rows(self):
        for row in self.df.index:
            for col in self.df.columns:
                print(self.df[col][row]," ")

    def load_rows(self):
        r = []
        for row in self.df.index:
            record = []
            for col in self.df.columns:
                record.append(self.df[col][row])
            r.append(record)
        return r




if __name__ == '__main__':
    filePath = "./data/FIFA-2019/FIFA-2019.csv"
    dc = DataCleansing(filePath)
    dc.select_dimension = ['Name', 'Age', 'Potential', 'Body Type', 'Value', 'Wage']
    dc.data_clean("€", 'Wage')
    dc.data_clean("€", 'Value')
    dc.str_to_value(["Wage", "Value"])
    dc.export_csv("fifa-2019-cleansed.csv")
