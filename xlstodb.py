import os
import pypyodbc
import split
import pandas as pd


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
    for b in buildings:
        b[0] = str(b[0]).split(';')
    return buildings

ID = 1
ID_buildings = 1

def add_data(db, full_name, short_name, address_main, buildings, ogrn, split_addr):
    global ID, ID_buildings
    for i in range(len(full_name)):
        db.cursor().execute("INSERT INTO address VALUES(?, ?, ?, ?)", (ID, full_name[i], short_name[i], address_main[i]))
        for k in range(len(split_addr[ogrn[i]])):
            db.cursor().execute("INSERT INTO split_address VALUES(?, ?, ?, ?, ?, ?, ?, ?)", \
                (ID, str(ogrn[i]), split_addr[ogrn[i]][k]['ind'], split_addr[ogrn[i]][k]['country'],  split_addr[ogrn[i]][k]['region'], \
                split_addr[ogrn[i]][k]['locality'], split_addr[ogrn[i]][k]['street_house'], split_addr[ogrn[i]][k]['other']))     
        for j in range(len(buildings[i][0])-1):
            db.cursor().execute("INSERT INTO buildings VALUES(?, ?, ?, ?, ?, ?)", (ID_buildings, ID, 'False', buildings[i][0][j], '', ''))
            ID_buildings += 1
        ID += 1
    db.commit()
    db.close()

if __name__ == '__main__':
    name_xlsx = "License2.xlsx"
    name_page = "Лист1"
    df = pd.read_excel(name_xlsx, name_page, usecols=[0, 1, 3, 4, 6, 7])
    path_to_directory = os.getcwd()
    db = create_db(path_to_directory)
    create_table(db)
    ogrn = []
    inn = []
    full_name = []
    short_name = []
    address_main = []
    buildings = []
    for i in range(len(df)):
        ogrn.append(df.iat[i, 0])
        inn.append(df.iat[i, 1])
        full_name.append(df.iat[i, 2])
        short_name.append(df.iat[i, 3])
        address_main.append(df.iat[i, 4])
        buildings.append([df.iat[i, 5]])

    buildings = split_buildings(buildings)
    ogrn_split_addr, split_addr = split.get_ogrn_address("License2.xlsx", "Лист1")
    add_data(db, full_name, short_name, address_main, buildings, ogrn_split_addr, split_addr)
   