# encoding: utf-8
# @file : data_integration.py
# @software : PyCharm
# @author : Ading
# Official Account: AdingBLOG
import csv
import os

from csv_to_mysql import MysqlUtil, DB_CONFIG, CSV2Mysql
from data_cleansing import DataCleansing


class DataIntegration:
    all_file_data = []

    def __init__(self, fileFolder, targetFilename):
        self.dimens = None
        self.fileFolder = fileFolder
        self.fileList = [file for file in os.listdir(fileFolder) if file[-4:] == ".csv"]
        if "integrated" not in os.listdir("./data"):
            os.mkdir("./data/integrated")
        self.targetFilename = "./data/integrated/" + targetFilename

    def manipulate_dimens(self, data_cleansing: DataCleansing, dimens_select: list, dimens_add):
        """
        custom method, to add a col named year
        :param data_cleansing:
        :param dimens_select:
        :param dimens_add:
        :return:
        """

        for fileName in self.fileList:
            data_cleansing.fileName = self.fileFolder + fileName
            dimens_add_value = fileName.lstrip("FIFA - ").rstrip(".csv")
            data_cleansing.select_dimension = dimens_select
            data_cleansing.add_dimension(dimens_add, dimens_add_value)
            self.all_file_data.append(data_cleansing.load_rows())

        self.dimens = dimens_select+dimens_add


    def export_csv(self):
        print(self.all_file_data)
        with open(self.targetFilename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.dimens)  # header
            for file in self.all_file_data:
                for row in file:
                    writer.writerow(row)
            f.close()


if __name__ == '__main__':
    data_i = DataIntegration(fileFolder="./data/FIFA-1930-2018/", targetFilename="fifa-1930-2018.csv")
    dimens_select = ['Position', 'Team', 'Games Played', 'Win', 'Draw', 'Loss', 'Goals For','Goal Difference','Points']
    dc = DataCleansing()
    data_i.manipulate_dimens(data_cleansing=dc, dimens_select=dimens_select, dimens_add=["year"])
    data_i.export_csv()
    conn =MysqlUtil(DB_CONFIG['00'])
    csv2mysql = CSV2Mysql(data_i.targetFilename)
    table_fields=['position','team','games_played','win','draw','loss','goals_for','goals_against',"goals_difference",'points','year']
    csv2mysql.insert_sql(table="fifa_1930_2018",conn=conn,table_fields=table_fields)