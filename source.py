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
from itertools import groupby


def json_parse(name = 'dataObrnadzor.json'):
    with open(name, encoding="utf8") as f:
        templates = json.load(f)

    arr = []
    for i in range(len(templates)):
        arr.append(templates[i]['guid'])
    return arr

def unique(items):
    found = set([])
    keep = []

    for item in items:
        if item not in found:
            found.add(item)
            keep.append(item)

    return keep

def asplit(address):
    res = ''
    address_arr = address.split(";")
    for i in address_arr:
        res += address_split.f(i)
    #print(res)
    return res

def get_data(url):
    data = dict()
    try:
        page1 = requests.get("http://isga.obrnadzor.gov.ru/rlic/details/" + url + "/") 
        soup1 = BeautifulSoup(page1.text, "lxml")
        table1 = soup1.find("table",{"class": "table table-bordered"}).find("tbody").find_all("tr")
        for tr in table1:
            tds = tr.find_all("td")   
            tds = [ele.text.strip() for ele in tds]
            if (tds[0] == "Текущий статус лицензии" and tds[1] == "Не действует"):
                continue   
            if (tds[0] == "ОГРН") | (tds[0] == "ИНН") | (tds[0] == "КПП") | (tds[0] == "Полное наименование организации (ФИО индивидуального предпринимателя)") |\
                (tds[0] == "Сокращенное наименование организации") | (tds[0] == "Субьект РФ"):
                key = tds[0]
                value = tds[1]
                data[key] = value
        data["Места осуществления образовательной деятельности"] = ''
        data["Место нахождения организации"] = ''
    except:
        with open("dont_working_urls.txt", "a+") as f:
            print("Ошибка! Не удалось открыть: http://isga.obrnadzor.gov.ru/rlic/details/" + url + "/")
            f.write(url)
            f.write("\n")
        return
        
    try:
        license_arr = soup1.find_all("tr",{"class": "clickable"})
        mood = []   #Место осуществления образовательной деятельности
        mno = []    #Место нахождения организации
        for lic in license_arr:
            if (lic.find_all("td")[3].text == "Действует"):
                url_to_full_address = lic["data-target"]
                page2 = requests.get("http://isga.obrnadzor.gov.ru/rlic/supplement/" + url_to_full_address + "/")
                soup2 = BeautifulSoup(page2.text, "lxml")
                table2 = soup2.find("table", {"class": "table table-bordered cells-centered"}).find("tbody").find_all("tr")
                for tr in table2:
                    tds = tr.find_all("td")
                    tds_text = [ele.text.strip() for ele in tds]
                    if (tds_text[0] == "Места осуществления образовательной деятельности"):
                        mood += tds[1].__str__().replace('<td>', '').replace('</td>', '').replace('\t', '').split("<br/>")
                    elif (tds_text[0] == "Место нахождения организации"):
                        mno += tds[1].__str__().replace('<td>', '').replace('</td>', '').replace('\t', '').split("<br/>")
        #print(mno)
        #print(mood)
        mno = unique(mno)
        for i in mno:
            data["Место нахождения организации"] += i + ";"
        mno = (asplit(data["Место нахождения организации"])).split(';')
        mno = unique(mno)
        data["Место нахождения организации"] = ''
        

        for i in mno:
            data["Место нахождения организации"] += i + ";"
        data["Место нахождения организации"] = data["Место нахождения организации"][:-1]

        mood = unique(mood)
        for i in mood:
            data["Места осуществления образовательной деятельности"] += i + ";"
        mood = (asplit(data["Места осуществления образовательной деятельности"])).split(';')
        mood = unique(mood)
        data["Места осуществления образовательной деятельности"] = ''
        for i in mood:
            data["Места осуществления образовательной деятельности"] += i + ";"
        data["Места осуществления образовательной деятельности"] = data["Места осуществления образовательной деятельности"][:-1]
    except TypeError:
        print('Ошибка:\n', traceback.format_exc())
        data["Места осуществления образовательной деятельности"] = ''
    except AttributeError:
        #print(url)
        print('Ошибка:\n', traceback.format_exc())
    except:
        print("Ошибка! Не удалось открыть: http://isga.obrnadzor.gov.ru/rlic/supplement/" + url_to_full_address + "/")
        #raise Exception("Ошибка! Не удалось открыть: http://isga.obrnadzor.gov.ru/rlic/supplement/" + url_to_full_address + "/") from None
        with open("dont_working_urls.txt", "a+") as f:
            #print("Ошибка! Не удалось открыть: http://isga.obrnadzor.gov.ru/rlic/supplement/" + url_to_full_address + "/")
            f.write(url)
            f.write("\n")
        return
        #print('Ошибка:\n', traceback.format_exc())
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
    urls = json_parse()     #для изменения количества лицензий изменить строку на urls = json_parse()[start:end], start и end - индексы
    #urls = ['d352f1b0-758f-474f-9a3a-815043654120']
    #urls = ['947731b7-e576-b69c-99ba-d26e95db7f62']
    fields = ["ОГРН", "ИНН", "КПП", "Полное наименование организации (ФИО индивидуального предпринимателя)", \
    "Сокращенное наименование организации", "Субьект РФ", "Место нахождения организации", "Места осуществления образовательной деятельности"]
    row = 1
    col = 0
    count = 0
    dw_counter = 0
    for i in range(len(fields)):
        worksheet.write(0, i, fields[i])
    for start_counter in range(0, len(urls)+5000, 5000):
        while True:
            with Pool(20) as p:
                if (start_counter+5000 < len(urls)):
                    end_counter = start_counter+5000
                else:
                    end_counter = len(urls)
                for result in p.map(make_all, urls[start_counter:end_counter]):
                    count += 1
                    for i in fields:
                        try:
                            worksheet.write(row, col, result[i])
                        except:
                            row -= 1
                            count -= 1
                        col += 1
                    row += 1
                    col = 0
            file = open("dont_working_urls.txt", "r")
            file_data = file.read().splitlines()
            #print("len(file_data) =========== ", len(file_data))
            if len(file_data) != 0:
                file.close()
                if (dw_counter == 5):
                    break
                urls = file_data
                file = open("dont_working_urls.txt", "w")
                file.close()
                dw_counter += 1
            else:
                file.close()
                dw_counter += 1
                break

    if (dw_counter == 5):
        print("Не все адреса обработаны. Проверьте файл dont_working_urls.txt")
    print('Done!, count urls = ', count, '\nStart: ', start, '\nEnd: ', datetime.datetime.now())
    workbook.close()