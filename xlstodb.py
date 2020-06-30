import os
import pypyodbc
import split
import ta
import coordinates

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

def add_data(db, full_name, short_name, address_main, buildings, ogrn, split_addr, region):
    global ID, ID_buildings
    for i in range(len(full_name)):
        db.cursor().execute("INSERT INTO address VALUES(?, ?, ?, ?)", (ID, full_name[i], short_name[i], address_main[i]))
        for k in range(len(split_addr[i])):
            if (split_addr[i][k]['ind'] == '') & (split_addr[i][k]['locality'] == '') & \
            (split_addr[i][k]['street_house'] == '') & (split_addr[i][k]['other'] == ''):
                continue
            db.cursor().execute("INSERT INTO split_address VALUES(?, ?, ?, ?, ?, ?, ?, ?)", \
                (ID, str(ogrn[i]), split_addr[i][k]['ind'], 'Россия',  region[i], \
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
    ogrn, inn, kpp, full_name, short_name, address_main, buildings, region = ta.f()
    split_addr = split.get_ogrn_address(buildings)
    buildings = split_buildings(buildings)
    #coord = coordinates.f(buildings)
    #print(coord)    
    add_data(db, full_name, short_name, address_main, buildings, ogrn, split_addr, region)

    