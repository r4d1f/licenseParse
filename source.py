from bs4 import BeautifulSoup
import xlsxwriter
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import os
import zipfile
import datetime
#url = "http://isga.obrnadzor.gov.ru/rlic/details/0B0F0C12-0F0C-130A-110F-0E0F13120B0A100F100E/"

def f(newzip,driver,wait):
    count = 0
    dont_working_urls = []
    with open('file.txt', 'r') as f:
        urls = f.read().splitlines()
    print("Start work: ")
    for i in range(len(urls)):
        print(i)
        try:
            driver.get("http://isga.obrnadzor.gov.ru/rlic/details/" + urls[i] + '/')
        except:
            dont_working_urls.append(urls[i])

        soup = BeautifulSoup(driver.page_source, "lxml")
        data = dict()
        table1 = soup.find("table",{"class": "table table-bordered"}).find("tbody").find_all("tr")
        for tr in table1:
            tds = tr.find_all("td")   
            tds = [ele.text.strip() for ele in tds]
            if (tds[0] == "ОГРН") | (tds[0] == "ИНН") | (tds[0] == "Полное наименование организации (ФИО индивидуального предпринимателя)") |\
               (tds[0] == "Сокращенное наименование организации") | (tds[0] == "Место нахождения организации"):
                key = tds[0]
                value = tds[1]
                data[key] = value

        driver.find_element_by_xpath('/html/body/div/div[3]/table/tbody/tr[1]').click()
        wait.until(lambda browser: browser.find_element_by_xpath('/html/body/div/div[3]/table/tbody/tr[2]/td/table[1]'))

        soup2 = BeautifulSoup(driver.page_source, "lxml")
        table = soup2.find("table", {"class": "table table-bordered cells-centered"}).find("tbody").find_all("tr")
        for tr in table:
            tds = tr.find_all("td")   
            tds = [ele.text.strip() for ele in tds]
            if tds[0] == "Места осуществления образовательной деятельности":
                key = tds[0]
                value = tds[1]
                data[key] = value
        count += 1 
    
        xlsxname = data["Сокращенное наименование организации"] + ".xlsx"
        workbook = xlsxwriter.Workbook(xlsxname)
        worksheet = workbook.add_worksheet()    
        row = 0
        col = 0
        for key in data.keys():
            worksheet.write(row, col, key)
            worksheet.write(row+1, col, data[key])
            col += 1 
        workbook.close()

        newzip.write(xlsxname)
        os.remove(xlsxname)
    return (dont_working_urls, count)

if __name__ == '__main__':
    nowDate = datetime.datetime.now().strftime("%d.%m.%y")
    s_dir = os.getcwd() + "\\"
    path_to_zip = s_dir + 'Organization_' + nowDate + ".zip"
    newzip = zipfile.ZipFile(path_to_zip,'w')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(os.getcwd() + "/chromedriver.exe",chrome_options=options)
    wait = ui.WebDriverWait(driver,10)

    dont_working_urls, count = f(newzip,driver,wait)
    print('dont working urls = ', dont_working_urls, '(', len(dont_working_urls), ')', "\ncount parsed url = ", count)
    driver.close()
    newzip.close()