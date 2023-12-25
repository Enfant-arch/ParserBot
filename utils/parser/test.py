import re
import json
import asyncio
from collections import namedtuple
{"id":"Z385079901903_Z901903688511",
"title":"Столы для ноутбука","titleImage":"https:\u002F\u002Fmain-cdn.sbermegamarket.ru\u002Fmid9\u002Fhlr-system\u002F189\u002F800\u002F082\u002F662\u002F022\u002F36\u002F2463684633829567t.jpg","nodes":[],"sequence":11000,
"subTitle":"","category":None,"collection":
{"collectionId":"688511","parentId":"901903","collectionType":"CATEGORY","title":"Столы для ноутбука","isDepartment":False,"hierarchy":[],"url":"\u002Fcatalog\u002Fstoly-dlya-noutbuka\u002F",
"images":{},"description":"","slug":"stoly-dlya-noutbuka","navigationMode":"","allowedServiceSchemes":[],"code":"","mainListingCollectionId":"",
"attributes":None,"rating":{},"shortTitle":"","mainListingCollectionRelativeUrl":"",
"name":"","displayName":""}
,"parentId":"Z385079901903"}
catalog_entity = namedtuple("Position", ["id", "title", "titleImage", "nodes",
                "sequence","subTitle", "category", "collection", "parentId"])

f = open(file=r"C:\Users\frigm\Work\ParserBot\page.htm", mode="r+", encoding='utf-8')

html = f.read()


pattern0 = r"window\.__APP__=(\{.*?\});"
pattern = r'"currentDepartmentCategories"\s*:\s*(\[(?:[^\[\]]|\[(?:[^\[\]]|\[[^\[\]]*\])*\])*\])'
async def test_enject():
    match = re.findall(pattern0, html, re.DOTALL)
    if match:
        catalog = re.search(pattern, match[1])
        return str(catalog.group(1)).replace("null", "None").replace("false", "False").replace("true", "True")
    else:
        print("Не нашли currentDepartmentCategories")
async def test_kbB():
    data = await test_enject()
    catalog_data = eval(data)
    for item in catalog_data:
        if item["id"]
    
    

asyncio.run(test_kbB())