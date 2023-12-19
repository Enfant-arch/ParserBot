from Good import product
import os
import pathlib
import json
from Good import product
import csv
import openpyxl


BASE_DIR = str(pathlib.Path().resolve()) + "/parserResults"


class ResultBuilder():
    def __init__(self, goods_list:list, username, query):
        self.goods_list = goods_list
        self.path = BASE_DIR + f"/{username}/{query}"
        try: os.makedirs(self.path)
        except Exception as err: pass
        ResultBuilder.generate_json(self.path, self.goods_list)
        ResultBuilder.generate_xl(self.path, self.goods_list)
        ResultBuilder.generate_csv(self.path, self.goods_list)
    
    @staticmethod 
    def generate_json(path, data:list):
        with open(file=f"{path}/result.json", mode="w+", encoding="utf-8") as file:
            json_product = json.dumps(data, default=namedtuple_to_dict, indent=4)
            file.write(json_product)

    @staticmethod
    def generate_xl(path, data:list):
        wb = openpyxl.Workbook()
        ws = wb.active
        product = []
        for good in data: product.append(list(good))
        for row in product:ws.append(row)
        wb.save(f"{path}/result.xlsx")

    @staticmethod
    def generate_csv(path, data:list):
        with open(file=f"{path}/result.csv", mode="w+", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(product._fields)
            for good in data:
                writer.writerow(good)

    
    
    
    




def namedtuple_to_dict(obj):
    if isinstance(obj, tuple) and hasattr(obj, '_asdict'): return obj._asdict()
    else:return obj

                


    

