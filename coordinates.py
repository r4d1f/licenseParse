# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options



#adr = ["676282, Россия, Амурская область, г. Тында, ул. Школьная, д. № 5;", "676439, Амурская область, Свободненский район,с. Уст-Пёра, ул. Мира7;", "676415, Россия, Амурская область, Свободненский район, с. Буссе, ул. Молодежная. д. 6;", "76623, Амурская область, Свободненский район, с. Москвитино, ул. Гагарина 9;", "676301, Амурская область, г.Шимановск, ул. Гайдара 41;"]
#return exmpl: ['55.151379, 124.730951', '51.450029, 128.149778', '51.222785, 126.917559', '51.146569, 127.980337', '52.004455, 127.692086']
def find_coord(adr):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(r'C:/Users/acer2/Desktop/Работа/licenseParse/test/chromedriver.exe', options = options)
    driver.get("https://yandex.ru/maps/")
    coordinates = []
    for a in adr:
        sbox = driver.find_element_by_class_name("input__control")
        sbox.send_keys(Keys.CONTROL + "a")
        sbox.send_keys(Keys.DELETE);
        sbox.send_keys(a)
        sbox.submit()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "button._view_search._size_medium._pin-left._pin-right")))
        try:
            coord = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "clipboard__action-wrapper")))
            res = coord.text
        except Exception as e: 
            print(e)
            res = ''
        coordinates.append(res)
    driver.close()
    return (coordinates)

