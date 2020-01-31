from bs4 import BeautifulSoup
import xlsxwriter
import os
import datetime
from multiprocessing import Pool
import requests
import traceback
import address_split

def get_data(url):
    dont_working_urls = []
    data = dict()
    try:
        page1 = requests.get("http://isga.obrnadzor.gov.ru/rlic/details/" + url + "/") 
        soup1 = BeautifulSoup(page1.text, "lxml")
        table1 = soup1.find("table",{"class": "table table-bordered"}).find("tbody").find_all("tr")
        for tr in table1:
            tds = tr.find_all("td")   
            tds = [ele.text.strip() for ele in tds]
            if (tds[0] == "ОГРН") | (tds[0] == "ИНН") | (tds[0] == "Полное наименование организации (ФИО индивидуального предпринимателя)") |\
                (tds[0] == "Сокращенное наименование организации") | (tds[0] == "Место нахождения организации"):
                key = tds[0]
                value = tds[1]
                data[key] = value
        data["Места осуществления образовательной деятельности"] = ''
    except:
        dont_working_urls.append(url)
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
    except:
        data["Места осуществления образовательной деятельности"] = ''
    return data
    
i = 0
def make_all(url):
    global i
    res = get_data(url)
    i+= 1
    print(i)
    return res

if __name__ == '__main__':  
    start = datetime.datetime.now()
    xlsxname = "License.xlsx"
    workbook = xlsxwriter.Workbook(xlsxname)
    worksheet = workbook.add_worksheet()
    with open('file.txt', 'r') as f:
        urls = f.read().splitlines()
    fields = ["ОГРН", "ИНН", "Полное наименование организации (ФИО индивидуального предпринимателя)", \
    "Сокращенное наименование организации", "Место нахождения организации", "Места осуществления образовательной деятельности"]
    row = 0
    col = 0
    count = 0
    with Pool(40) as p:
        for result in p.map(make_all, urls):
            count += 1
            for i in fields:
                try:
                    worksheet.write(row, col, result[i])
                except:
                    print(result)
                col += 1
            row += 1
            col = 0
    print('Done!, count urls = ', count, '\nStart: ', start, '\nEnd: ', datetime.datetime.now())
    workbook.close()
    f.close()