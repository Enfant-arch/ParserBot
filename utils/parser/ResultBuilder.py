import requests
from utils.parser.Good import product
import os
import pathlib
import json
from utils.parser.Good import product
import csv
import openpyxl
from collections import namedtuple
from collections import namedtuple
import pdfkit
import io
import requests


BASE_DIR = str(pathlib.Path().resolve()) + "\parserResults"


class ResultBuilder():
    def __init__(self, goods_list:set, username, query):
        self.goods_list = sorted(list(goods_list), key=lambda p: p.bonusAmount)
        self.path = BASE_DIR + f"/{username}/{query}"
        try: os.makedirs(self.path)
        except Exception as err: pass
        ResultBuilder.generate_json(self.path, self.goods_list)
        ResultBuilder.generate_xl(self.path, self.goods_list)
        ResultBuilder.generate_txt(self.path, self.goods_list)
        #ResultBuilder.generate_pdf(self.path, self.goods_list)
        self.message = ResultBuilder.generate_message(self.goods_list)
        print(self.message)
    
    @staticmethod 
    def generate_json(path, data:list):
        with open(file=f"{path}/result.json", mode="w+", encoding="utf-8") as file:
            json_product = json.dumps(list(data), default=namedtuple_to_dict, ensure_ascii=False, indent=4)
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
    
    @staticmethod
    def generate_pdf(path, data:list):
        html = """
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                table, th, td {
                    border: 1px solid black;
                    border-collapse: collapse;
                }
                th {
                    background-color: lightgrey;
                    color: white;
                }
                th, td {
                    padding: 5px;
                    text-align: left;
                }
            </style>
        </head>
        <body>
            <table>
                <tr>
                    <th>Название</th>
                    <th>Ссылка</th>
                    <th>Изображение</th>
                    <th>Цена</th>
                    <th>Бонус %</th>
                    <th>Бонус руб.</th>
                    <th>Отзывы</th>
                    <th>Продавец</th>
                </tr>
        """

        for product in data:
            html += f"""
                <tr>
                    <td>{product.name}</td>
                    <td><a href="{product.link}">{product.link}</a></td>
                    <td><img src="{product.image_link}" width="100" height="100"></td>
                    <td>{product.price}</td>
                    <td>{product.bonusPercent}</td>
                    <td>{product.bonusAmount}</td>
                    <td>{product.reviewCount}</td>
                    <td>{product.seller}</td>
                </tr>
            """

        html += """
            </table>
        </body>
        </html>
        """

        # создаем pdf-файл с именем products.pdf из HTML-кода
        pdfkit.from_string(html, "products.pdf")


    @staticmethod
    def generate_txt(path, data:list):
        with open(file=f"{path}/result.txt", mode="w+", encoding="utf-8") as file:
            for p in data:
                file.write("<===================================================>\n")
                file.write(f"Название товара: {p.name}\n")
                file.write(f"Сссылка: {p.link}\n")
                file.write(f"Цена: {p.price}\n")
                file.write(f"Процент кешбека: {p.bonusPercent}\n")
                file.write(f"Сумма кешбека: {p.bonusAmount}\n")
                file.write(f"Кол-во отзывов: {p.reviewCount}\n")
                file.write(f"Продавец: {p.seller}]\n")
                file.write("<====================================================>\n\n")
            file.close()

    
    @staticmethod 
    def generate_message(data:list):
        result = f"✅ Найдено: {len(data)} товаров\n"
        for x in range(len(data)):
            result += f'<a href="{data[x].link}">{data[x].name}</a> : кешбек/цена - {data[x].bonusAmount}/{data[x].price}₽\n'
            if x > 20:
                break
        result += "<code>и так далее</code>"
        return result
    


    

def namedtuple_to_dict(obj):
    
        if isinstance(obj, tuple) and hasattr(obj, '_asdict'): return obj._asdict()
        else:
            raise TypeError(
                "Unserializable object {} of type {}".format(obj, type(obj))
                )
            return obj

                
