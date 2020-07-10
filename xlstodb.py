import os
import pypyodbc
from collections import OrderedDict
import split
import ta
from operator import itemgetter
#import coordinates


def create_db(path_to_directory):
    db_path = path_to_directory + '/DB.mdb'
    if os.path.exists(db_path):
        os.remove(db_path)
    pypyodbc.win_create_mdb(db_path)
    db = pypyodbc.win_connect_mdb(db_path) 
    return db

def create_table(db):
    sql1 = \
    'CREATE TABLE address(\
        ID INT PRIMARY KEY,\
        org_id INT,\
        full_name_lic VARCHAR(255),\
        short_name_lic VARCHAR(255),\
        address_main_lic VARCHAR(255));'
    sql2 = \
    'CREATE TABLE buildings(\
        ID INT PRIMARY KEY,\
        address_id INT,\
        isDestroyed VARCHAR(5),\
        address_full VARCHAR(255),\
        latitude VARCHAR(255),\
        longitude VARCHAR(255),\
        FOREIGN KEY (address_id) REFERENCES address(ID));'
    sql3 = \
    'CREATE TABLE split_address(\
        ADR_ID INT,\
        ogrn VARCHAR(50),\
        ind VARCHAR(50),\
        country VARCHAR(50),\
        region VARCHAR(255),\
        locality VARCHAR(255),\
        street_house VARCHAR(255),\
        other VARCHAR(255),\
        FOREIGN KEY (ADR_ID) REFERENCES address(ID));'

    db.cursor().execute(sql1)
    db.cursor().execute(sql2)
    db.cursor().execute(sql3)
    db.commit()

def split_buildings(buildings):
    #print(buildings, '\n\n\n')
    for b in buildings:
        #print(111, b[0])
        b[0] = str(b[0]).split(';')
    return buildings

def get_buildings_len(buildings_arr):
    res = 0
    for buildings in buildings_arr:
        for build in buildings:
            res += len(build)
    return res


def remove_duplicates(org_id, full_name, short_name, address_main, buildings, ogrn, split_addr, region):
    for i in range(len(org_id)-1):
        for j in range(len(org_id)-i-1):
            if org_id[j] > org_id[j+1]:
                org_id[j], org_id[j+1] = org_id[j+1], org_id[j]
                full_name[j], full_name[j+1] = full_name[j+1], full_name[j]
                short_name[j], short_name[j+1] = short_name[j+1], short_name[j]
                address_main[j], address_main[j+1] = address_main[j+1], address_main[j]
                buildings[j], buildings[j+1] = buildings[j+1], buildings[j]
                ogrn[j], ogrn[j+1] = ogrn[j+1], ogrn[j]
                split_addr[j], split_addr[j+1] = split_addr[j+1], split_addr[j]
                region[j], region[j+1] = region[j+1], region[j]
    result_arr = []
    result_id = 0
    tmp_sn = False
    tmp_len_adr = 0
    for i in range(len(org_id)-1):
        cur_len = get_buildings_len(buildings[i])
        if (type(short_name[i]) == float and tmp_sn == False and cur_len > tmp_len_adr):
            tmp_len_adr = cur_len
            result_id = i
        elif(type(short_name) != float):
            if (tmp_sn == False):
                result_id = i
                tmp_sn = True
                tmp_len_adr = get_buildings_len(buildings[i])
            else:
                cur_len = get_buildings_len(buildings[i])
                if(tmp_len_adr < cur_len):
                    tmp_len_adr = cur_len
                    result_id = i
        if (i+1 == len(org_id)-1):
            if (org_id[i+1] != org_id[i]):
                result_arr.append(i+1)
            else:
                cur_len = get_buildings_len(buildings[i])
                if (type(short_name[i+1]) == float and tmp_sn == False and cur_len > tmp_len_adr):
                    tmp_len_adr = cur_len
                    result_id = i+1
                elif(type(short_name) != float):
                    if (tmp_sn == False):
                        result_id = i+1
                        tmp_sn = True
                        tmp_len_adr = get_buildings_len(buildings[i+1])
                    else:
                        cur_len = get_buildings_len(buildings[i+1])
                        if(tmp_len_adr < cur_len):
                            tmp_len_adr = cur_len
                            result_id = i+1
                result_arr.append(result_id)


        if (org_id[i] != org_id[i+1]):
            result_arr.append(result_id)
            result_id = 0
            tmp_sn = False
            tmp_len_adr = 0
    res = [[] for i in range(8)]
    #org_id, full_name, short_name, address_main, buildings, ogrn, split_addr, region
    for i in result_arr:
        res[0].append(org_id[i])
        res[1].append(full_name[i])
        res[2].append(short_name[i])
        res[3].append(address_main[i])
        res[4].append(buildings[i])
        res[5].append(ogrn[i])
        res[6].append(split_addr[i])
        res[7].append(region[i])
    return res





    '''for i in range(len(org_id)-1):
                    if org_id[i+1] == org_id[i]:
                        short_name[i+1] = 0
                i = 0
                while org_id[i] != org_id[len(org_id)-1]:
                    if type(short_name[i]) == float:
                        del(org_id[i])
                        del(full_name[i])
                        del(short_name[i])
                        del(address_main[i])
                        del(buildings[i])
                        del(ogrn[i])
                        del(split_addr[i]) 
                        del(region[i])
                    else: 
                        i += 1'''
    #return org_id, full_name, short_name, address_main, buildings, ogrn, split_addr, region
    '''ns_dict = {}
    for i in range(len(org_id)):
        ns_dict[org_id[i]] = (full_name[i], short_name[i], address_main[i], buildings[i], ogrn[i], split_addr[i], region[i])
    print(ns_dict)
    s_dict = OrderedDict(sorted(ns_dict.items(), key=lambda t: t[0]))
    print(s_dict)
    org_id.sort()
    for i in range(len(org_id)):
        full_name[i], short_name[i], address_main[i], buildings[i], ogrn[i], split_addr[i], region[i] = \
        s_dict[org_id[i]][0], s_dict[org_id[i]][1], s_dict[org_id[i]][2], s_dict[org_id[i]][3], s_dict[org_id[i]][4], s_dict[org_id[i]][5], s_dict[org_id[i]][6],
        #org_id[i] = s_dict.keys()[i]
    #print(s_dict)
    return org_id, full_name, short_name, address_main, buildings, ogrn, split_addr, region'''
    
    #for i in range(len(org_id)):
    #    print(org_id[i], full_name[i], short_name[i], address_main[i], buildings[i], ogrn[i], split_addr[i], region[i], '\n')
ID = 1
ID_buildings = 1

def add_data(db, org_id, full_name, short_name, address_main, buildings, ogrn, split_addr, region):
    #print(len(buildings[46][0]))
    global ID, ID_buildings
    for i in range(len(full_name)):
        #print(buildings[i])
        #if (type(short_name[i]) == float):
        #    continue
        db.cursor().execute("INSERT INTO address VALUES(?, ?, ?, ?, ?)", (ID, org_id[i], full_name[i], short_name[i], address_main[i]))
        for k in range(len(split_addr[i])):
            if (split_addr[i][k]['ind'] == '') & (split_addr[i][k]['locality'] == '') & \
            (split_addr[i][k]['street_house'] == '') & (split_addr[i][k]['other'] == ''):
                continue
            db.cursor().execute("INSERT INTO split_address VALUES(?, ?, ?, ?, ?, ?, ?, ?)", \
                (ID, str(ogrn[i]), split_addr[i][k]['ind'], 'Россия',  split_addr[i][k]['region'], \
                split_addr[i][k]['locality'], split_addr[i][k]['street_house'], split_addr[i][k]['other']))
        for j in range(len(buildings[i][0])-1):
            db.cursor().execute("INSERT INTO buildings VALUES(?, ?, ?, ?, ?, ?)", (ID_buildings, ID, 'False', buildings[i][0][j], '', ''))
            ID_buildings += 1
        ID += 1
    db.commit()
    db.close()
#split_addr[i][k]['region']
if __name__ == '__main__':
    path_to_directory = os.getcwd()
    db = create_db(path_to_directory)
    create_table(db)
    org_id, ogrn, inn, kpp, full_name, short_name, address_main, buildings, region = ta.f()
    #print(3, buildings[len(buildings)-1])
    split_addr = split.get_ogrn_address(buildings)
    buildings = split_buildings(buildings)
    #print(4, buildings[len(buildings)-1])
    org_id, full_name, short_name, address_main, buildings, ogrn, split_addr, region = remove_duplicates(org_id, full_name, short_name, address_main, buildings, ogrn, split_addr, region)
    #print(short_name)
    
    #for i in buildings:
    #    print(i[0])
    #coord = coordinates.f(buildings)
    #print(coord)    
    add_data(db, org_id, full_name, short_name, address_main, buildings, ogrn, split_addr, region)

    