from bs4 import BeautifulSoup
import xlsxwriter
import os
import datetime
from multiprocessing import Pool
import requests
import traceback
import address_split
import json
import re

def json_parse(name = 'dataObrnadzor.json'):
    with open(name, encoding="utf8") as f:
        templates = json.load(f)

    arr = []
    for i in range(len(templates)):
        arr.append(templates[i]['guid'])
    return arr


def get_data(url):
    data = dict()
    try:
        page1 = requests.get("http://isga.obrnadzor.gov.ru/rlic/details/" + url + "/") 
        soup1 = BeautifulSoup(page1.text, "lxml")
        table1 = soup1.find("table",{"class": "table table-bordered"}).find("tbody").find_all("tr")
        for tr in table1:
            tds = tr.find_all("td")   
            tds = [ele.text.strip() for ele in tds]
            if (tds[0] == "ОГРН") | (tds[0] == "ИНН") | (tds[0] == "КПП") | (tds[0] == "Полное наименование организации (ФИО индивидуального предпринимателя)") |\
                (tds[0] == "Сокращенное наименование организации") | (tds[0] == "Субьект РФ") | (tds[0] == "Место нахождения организации"):
                key = tds[0]
                value = tds[1]
                if (key == "Место нахождения организации" and len(re.findall(r'\d{4,9}', value.split(',')[0].replace(" ", ""))) == 0):
                    value = address_split.swap(value)
                data[key] = value
        data["Места осуществления образовательной деятельности"] = ''
    except:
        with open("dont_working_urls.txt", "a+") as f:
            print("Ошибка! Не удалось открыть: http://isga.obrnadzor.gov.ru/rlic/details/" + url + "/")
            f.write(url)
            f.write("\n")
        return
        
    try:
        url_to_full_address = soup1.find("tr",{"class": "clickable"})['data-target']
        page2 = requests.get("http://isga.obrnadzor.gov.ru/rlic/supplement/" + url_to_full_address + "/")
        soup2 = BeautifulSoup(page2.text, "lxml")
        table2 = soup2.find("table", {"class": "table table-bordered cells-centered"}).find("tbody").find_all("tr")
        for tr in table2:
            tds = tr.find_all("td")   
            tds = [ele.text.strip() for ele in tds]
            if tds[0] == "Места осуществления образовательной деятельности":
                key = tds[0]
                value = tds[1]
                data[key] = value
        data["Места осуществления образовательной деятельности"] = address_split.f(data["Места осуществления образовательной деятельности"])
    except TypeError:
        data["Места осуществления образовательной деятельности"] = ''
    except AttributeError:
        #print(url)
        print('Ошибка:\n', traceback.format_exc())
    except:
        print('Ошибка:\n', traceback.format_exc())
    return data
    
def make_all(url):
    res = get_data(url)
    return res

if __name__ == '__main__':
    file = open("dont_working_urls.txt", "w")
    file.close()

    start = datetime.datetime.now()
    xlsxname = "License.xlsx"
    workbook = xlsxwriter.Workbook(xlsxname)
    worksheet = workbook.add_worksheet()
    urls = json_parse()[:500]
    fields = ["ОГРН", "ИНН", "КПП", "Полное наименование организации (ФИО индивидуального предпринимателя)", \
    "Сокращенное наименование организации", "Субьект РФ", "Место нахождения организации", "Места осуществления образовательной деятельности"]
    row = 1
    col = 0
    count = 0
    for i in range(len(fields)):
        worksheet.write(0, i, fields[i])
    while True:
        with Pool(40) as p:
            for result in p.map(make_all, urls):
                count += 1
                for i in fields:
                    try:
                        worksheet.write(row, col, result[i])
                    except:
                        row -= 1
                        count -= 1
                        #print(result)
                    col += 1
                row += 1
                col = 0
        file = open("dont_working_urls.txt", "r")
        file_data = file.read().splitlines()
        if len(file_data) != 0:
            urls = file_data
            file.close()
            file = open("dont_working_urls.txt", "w")
            file.close()
        else:
            file.close()
            break


    print('Done!, count urls = ', count, '\nStart: ', start, '\nEnd: ', datetime.datetime.now())
    workbook.close()