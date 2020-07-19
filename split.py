# -*- coding: utf-8 -*-
import pandas as pd
import re
import numpy as np

def address_split(adr):
    res = []
    #if (type(adr) == float) | (adr == ''):
    #    return [{"ind":"", "country":"","region":"", "locality":"", "street_house":"", "other":""}]
    try:
        adr_arr = adr.split(";")
    except AttributeError:
        res = [{"ind":"", "country":"","region":"", "locality":"", "street_house":"", "other":""}]
        return res
    if adr_arr[-1] == '':
        adr_arr = adr_arr[:-1]
    for el in adr_arr:
        el_arr = el.split(",")
        if len(el_arr) == 1:
            return [{"ind":el_arr[0], "country":"","region":"", "locality":"", "street_house":"", "other":""}]
        for i in range(len(el_arr)):
            el_arr[i] = el_arr[i].strip()
        dict_adr = dict.fromkeys(["ind", "country","region", "locality", "street_house", "other"])
        dict_adr["ind"] = el_arr[0]
        if (el_arr[1].lower() == "россия" or  el_arr[1].lower() == "российская федерация" or el_arr[1].lower() == "рф"):
            dict_adr["country"] = el_arr[1]
            haveCountry = 1
        else:
            dict_adr["country"] = "-"
            haveCountry = 0
        haveRegion = 0
        if (re.match(r"г\.|г\s|город\s", el_arr[1+haveCountry].lower())):
            dict_adr["region"] = "-"
        else:
            dict_adr["region"] = el_arr[1+haveCountry]
            haveRegion += 1
        try:
            if (re.match(r"г\.|г\s|город\s", el_arr[1+haveCountry+haveRegion].lower())):
                dict_adr["locality"] = el_arr[1+haveCountry+haveRegion]
                haveNotCity = 0
            else:
                dict_adr["locality"] = el_arr[1+haveCountry+haveRegion] + "," + el_arr[2+haveCountry+haveRegion]
                haveNotCity = 1
        except IndexError:
            dict_adr["locality"] = ""
            dict_adr["street_house"] = ""
            dict_adr["other"] = ""
            res.append(dict_adr)
            continue
        try:
            flag = 0
            print(el_arr[2 + haveCountry + haveNotCity+haveRegion])
            if (re.match(r"д\.\s*\d+,*|дом\s*\d+,*|д\.\s*№\s*\d*,*|дом № \d*,*", el_arr[2 + haveCountry + haveNotCity+haveRegion])):
                flag = 1
                dict_adr["street_house"] = el_arr[2+ haveCountry + haveNotCity+haveRegion] + "," + el_arr[3 + haveCountry + haveNotCity+haveRegion]
                haveHouse = 1
            elif (re.match(r'улица\s*|ул\.\s*\S*,|ул\.\s*\S*\s*\S*\s*\S*|ул\.\s*\S*\s*\S*\s*\S*,|пер\.\s*\S*|пл\.\s*\S*|переулок\s*\S*|просп\.\s*\S*|проспект\s*|пр-кт\s*|туп\.\s*\S*', el_arr[2 + haveCountry + haveNotCity+haveRegion])):
                flag =1
                dict_adr["street_house"] = el_arr[2+ haveCountry + haveNotCity+haveRegion] + "," + el_arr[3 + haveCountry + haveNotCity+haveRegion]
                haveHouse = 1
            else:
                dict_adr["street_house"] = el_arr[2+ haveCountry + haveNotCity+haveRegion]
                haveHouse = 0
        except IndexError:
            if (flag==1):
                dict_adr["street_house"] = el_arr[2+ haveCountry + haveNotCity+haveRegion]
            else:
                dict_adr["street_house"] = ""
            dict_adr["other"] = ""
            res.append(dict_adr)
            continue
        dict_adr["other"] = ""
        for i in el_arr[3 + haveCountry + haveNotCity + haveHouse+haveRegion:]:
            dict_adr["other"] += i + ","
        dict_adr["other"] = dict_adr["other"][:-1]
        res.append(dict_adr)
    return res
        

def f_for_addr_correction(buildings):
    res = []
    for b in buildings:
        res.append(address_split(list(b.split(';'))[1]))
    return res

def get_ogrn_address(address):
    res_split = []
    for i in range(len(address)):
        if (type(address[i]) == float) | (address[i] == ''):
            continue 
        res_split.append(address_split(address[i][0]))
    return res_split

if __name__ == '__main__':
    adr = '119454, г. Москва, просп. Вернадского, д. 78, стр. 1;119454, г. Москва, просп. Вернадского, д. 78, стр. 2;119454, г. Москва, просп. Вернадского, д. 78, стр. 3;119454, г. Москва, просп. Вернадского, д. 78, стр. 4;119454, г. Москва, просп. Вернадского, д. 78, стр. 5;119454, г. Москва, просп. Вернадского, д. 78, стр. 6;119571, г. Москва, проспект Вернадского, д. 86, стр. 3;119571, г. Москва, проспект Вернадского, д. 86, стр. 5;119571, г. Москва, проспект Вернадского, д. 86, стр. 6;119571, г. Москва, проспект Вернадского, д. 86, стр. 7;119571, г. Москва, проспект Вернадского, д. 86, стр. 8;119454, г. Москва, просп. Вернадского, д. 78, строен. 1;119454, г. Москва, просп. Вернадского, д. 78, строен. 2;119454, г. Москва, просп. Вернадского, д. 78, строен. 3;119454, г. Москва, просп. Вернадского, д. 78, строен. 4;119454, г. Москва, просп. Вернадского, д. 78, строен. 5;119454, г. Москва, просп. Вернадского, д. 78, строен. 6;119454, г. Москва, пр-кт Вернадского, д. 78, строен. 1;119454, г. Москва, пр-кт Вернадского, д. 78, строен. 2;119454, г. Москва, пр-кт Вернадского, д. 78, строен. 3;119454, г. Москва, пр-кт Вернадского, д. 78, строен. 4;119454, г. Москва, пр-кт Вернадского, д. 78, строен. 5;119454, г. Москва, пр-кт Вернадского, д. 78, строен. 6;107996, г. Москва, ул. Стромынка, дом 20;119454, г. Москва, просп. Вернадского, д. 78, стр. 8;119454, г. Москва, просп. Вернадского, д. 78, стр. 9;119454, г. Москва, просп. Вернадского, д. 78, стр. 10;119454, г. Москва, просп. Вернадского, д. 78, стр. 11;119454, г. Москва, просп. Вернадского, д. 78, стр. 13;119454, г. Москва, просп. Вернадского, д. 78, стр. 14;107996, г. Москва, ул. Стромынка, дом 20, корпус 1;105118, г. Москва, ул. Соколиной Горы 5-я, д. 22;119435, г. Москва, ул. Малая Пироговская, д. 1, стр. 8;107996, г. Москва, ул. Стромынка, д. 20, стр. 4;119571, г. Москва, проспект Вернадского, д. 86, стр. 4;133093, г. Москва, пер. Щипковский 1-й, д. 23, стр. 1;133093, г. Москва, пер. Щипковский 1-й, д. 23, стр. 2;105118, г. Москва, ул. Соколиной Горы 5-я, д. 22, корп. 1;119048, г. Москва, ул. Усачева, д. 7/1;119435, г. Москва, ул. Малая Пироговская, д. 1, стр. 5;355035, Ставропольский край, г. Ставрополь, проспект Кулакова, д. 8, в квартале 601;355035, Ставропольский край, г. Ставрополь, улица 1 Промышленная, д. 13, в квартале 601;355035, Ставропольский край, город Ставрополь, проспект Кулакова 8, в квартале 601;355035, Ставропольский край, город Ставрополь, улица 1 Промышленная 13, в квартале 601;141190, Московская область, г. Фрязино, ул. Вокзальная, д. 2а, корп. 12;141190, Московская область, г. Фрязино, ул. Вокзальная, д. 2а, корп. 14;141190, Московская область, г. Фрязино, ул. Вокзальная, д. 2а, корп. 61;'
    print(address_split(adr))
    #for r in address_split(adr):
    #    print(r)
