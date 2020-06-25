import pandas as pd
import re

def address_split(adr):
    res = []
    try:
        adr_arr = adr.split(";")
    except AttributeError:
        res = [{"ind":"", "country":"","region":"", "locality":"", "street_house":"", "other":""}]
        return res
    if adr_arr[-1] == '':
        adr_arr = adr_arr[:-1]
    for el in adr_arr:
        el_arr = el.split(",")
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
        dict_adr["region"] = el_arr[1+haveCountry]
        if (re.match(r"г\.|г\s|город\s", el_arr[2+haveCountry].lower())):
            dict_adr["locality"] = el_arr[2+haveCountry]
            haveNotCity = 0
        else:
            dict_adr["locality"] = el_arr[2+haveCountry] + "," + el_arr[3+haveCountry]
            haveNotCity = 1
        try:
            if (re.match(r"д\.\s*\d+,*|дом\s*\d+,*|д\.\s*№\s*\d*,*|дом № \d*,*", el_arr[4 + haveCountry + haveNotCity])):
                dict_adr["street_house"] = el_arr[3+ haveCountry + haveNotCity] + "," + el_arr[4 + haveCountry + haveNotCity]
                haveHouse = 1
            elif (re.match(r'ул\.\s*\S*,|ул\.\s*\S*\s*\S*\s*\S*|ул\.\s*\S*\s*\S*\s*\S*,|пер\.\s*\S*,|пл\.\s*\S*,|переулок\s*\S*,|просп\.\s*\S*,|туп\.\s*\S*,|пр-кт\.\s*\S*,', el_arr[4 + haveCountry + haveNotCity])):
                dict_adr["street_house"] = el_arr[3+ haveCountry + haveNotCity] + "," + el_arr[4 + haveCountry + haveNotCity]
                haveHouse = 1
            else:
                dict_adr["street_house"] = el_arr[3+ haveCountry + haveNotCity]
                haveHouse = 0
        except IndexError:
            dict_adr["street_house"] = el_arr[3+ haveCountry + haveNotCity]
            dict_adr["other"] = ""
            res.append(dict_adr)
            continue
        dict_adr["other"] = ""
        for i in el_arr[4 + haveCountry + haveNotCity + haveHouse:]:
            dict_adr["other"] += i + ","
        dict_adr["other"] = dict_adr["other"][:-1]
        res.append(dict_adr)
    return res
         
        
def get_ogrn_address(name_xlsx, name_page):
    df = pd.read_excel(name_xlsx, name_page, usecols=[0, 7])
    ogrn_address = {}
    for i in range(int(df.size/2)):
        ogrn = df.iat[i, 0]
        address = df.iat[i, 1]
        res_split = address_split(address)
        ogrn_address.update({ogrn:res_split})
    return ogrn_address

