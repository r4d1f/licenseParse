import pyodbc
import pypyodbc
import re
import split

def get_data_from_db(DataBase, Table):
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + DataBase + ";'")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ' + Table + "'")
    return(cursor.fetchall())

def make_standard_addr(buildings):
    for b in buildings:
        if b[3].find('строен.'):
            b[3] = b[3].replace('строен.', 'стр.')
        if b[3].find('проспект'):
            b[3] = b[3].replace('проспект', 'пр-кт')
        if b[3].find('просп.'):
            b[3] = b[3].replace('просп.', 'пр-кт')
        b[3] = b[3].replace('сооружение', 'стр.')
        b[3] = b[3].replace('дом', 'д.')
    return buildings

def rm_duplicates(buildings):
    keys = [str(b[1])+';'+b[3]+';'+b[4]+';'+b[5] for b in buildings]
    coord_dict = dict.fromkeys(keys, 0)
    c = 0
    for b in buildings:
        if coord_dict[str(b[1])+';'+b[3]+';'+b[4]+';'+b[5]] == 0:
            coord_dict[str(b[1])+';'+b[3]+';'+b[4]+';'+b[5]] = 1
        else:
            c += 1
    return coord_dict

def update_db(DataBase, res_buildings, split_addr):
    db = pypyodbc.win_connect_mdb(DataBase) 
    db.cursor().execute('CREATE TABLE buildings2(\
        ID INT PRIMARY KEY,\
        address_id INT,\
        isDestroyed VARCHAR(5),\
        address_full VARCHAR(255),\
        latitude VARCHAR(255),\
        longitude VARCHAR(255),\
        FOREIGN KEY (address_id) REFERENCES address(ID));')
    db.cursor().execute('CREATE TABLE split_address2(\
        ADR_ID INT,\
        ind VARCHAR(50),\
        country VARCHAR(50),\
        region VARCHAR(255),\
        locality VARCHAR(255),\
        street_house VARCHAR(255),\
        other VARCHAR(255),\
        FOREIGN KEY (ADR_ID) REFERENCES address(ID));')
    ID = 1
    res_buildings = list(res_buildings)
    for i in range(len(res_buildings)):
        db.cursor().execute("INSERT INTO buildings2 VALUES(?, ?, ?, ?, ?, ?)", (ID, res_buildings[i].split(';')[0], 'False', \
            res_buildings[i].split(';')[1], res_buildings[i].split(';')[2], res_buildings[i].split(';')[3]))
        db.cursor().execute("INSERT INTO split_address2 VALUES(?, ?, ?, ?, ?, ?, ?)", (res_buildings[i].split(';')[0],  split_addr[i][0]['ind'],\
         'Россия',  split_addr[i][0]['region'], split_addr[i][0]['locality'], split_addr[i][0]['street_house'], split_addr[i][0]['other']))
        ID += 1
    db.commit()

if __name__ == '__main__':
    DataBase = 'D:/W/task4/licenseParse/DB.mdb'
    Table1 = 'buildings'
    buildings = get_data_from_db(DataBase, Table1)
    buildings = make_standard_addr(buildings)
    res_buildings = rm_duplicates(buildings)
    split_buildings = split.f_for_addr_correction(res_buildings.keys())
    update_db(DataBase, res_buildings.keys(), split_buildings) 