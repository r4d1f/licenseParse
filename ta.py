import pandas as pd
import numpy as np


def f():
    df = pd.read_excel("License.xlsx", "Sheet1", usecols=[0, 1, 2, 3, 4, 6, 7])
    ogrn = []
    inn = []
    kpp = []
    full_name = []
    short_name = []
    address_main = []
    buildings = []
    for i in range(len(df)):
        ogrn.append(df.iat[i, 0])
        inn.append(df.iat[i, 1])
        kpp.append(df.iat[i, 2])
        full_name.append(df.iat[i, 3])
        short_name.append(df.iat[i, 4])
        address_main.append(df.iat[i, 5])
        buildings.append([df.iat[i, 6]])
    
    df_vo = pd.read_excel("vo_orgs.xlsx", "Лист2", usecols=[5, 10, 13, 14, 15])
    vo_ogrn = []
    vo_inn = []
    vo_kpp = []
    vo_region = []
    vo_main_addr = []
    for i in range(len(df_vo)):
        vo_region.append(df_vo.iat[i, 0])
        vo_main_addr.append(df_vo.iat[i, 1])
        vo_inn.append(df_vo.iat[i, 2])
        vo_kpp.append(df_vo.iat[i, 3])
        vo_ogrn.append(df_vo.iat[i, 4])
    
    co = 0
    for i in range(len(vo_inn)):
        try:
            vo_ogrn[i] = int(vo_ogrn[i])
        except:
            vo_ogrn[i] = 0
        try:
            vo_inn[i] = int(vo_inn[i])
        except:
            vo_inn[i] = 0
        try:
            vo_kpp[i] = int(vo_kpp[i])
        except:
            vo_kpp[i] = 0

    res_ogrn = []
    res_inn = []
    res_kpp = []
    res_full_name = []
    res_short_name = []
    res_address_main = []
    res_buildings = []
    res_region = []
    for i in range(len(ogrn)):
        try:
            ogrn[i] = int(ogrn[i])
        except:
            ogrn[i] = -1
        try:
            inn[i] = int(inn[i])
        except:
            inn[i] = -1
        try:
            kpp[i] = int(kpp[i])
        except:
            kpp[i] = -1
        for j in range(len(vo_inn)):
            if (vo_inn[j] == inn[i]) & (vo_ogrn[j] == ogrn[i]) & (vo_kpp[j] == kpp[i]):
                if type(address_main[i]) != str:
                    if np.isnan(address_main[i]):
                        address_main[i] = vo_main_addr[j]
                co += 1
                res_ogrn.append(ogrn[i])
                res_inn.append(inn[i])
                res_kpp.append(kpp[i])
                res_full_name.append(full_name[i])
                res_short_name.append(short_name[i])
                res_address_main.append(address_main[i])
                res_buildings.append(buildings[i])
                res_region.append(vo_region[j])
                    
    print(co)
    return (res_ogrn, res_inn, res_kpp, res_full_name, res_short_name, res_address_main, res_buildings, res_region)
    
if __name__ == '__main__':
    f()
