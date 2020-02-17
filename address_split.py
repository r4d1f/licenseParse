import re

def f1(address):
    split_address = split(address)
    arr_address = split_address.split(";")

def swap(address):
    arr_address = address.rstrip(";").split(',')
    res = ''
    for i in range(len(arr_address)):
        res += arr_address[len(arr_address)-1-i] + ','
    res = res[:-1].lstrip(" ") 
    return res

def split_home(address):
    tmp = 0
    tmp_address = ''
    address = address.strip(" ")
    index_arr = re.findall(r'\d{5,9}', address)
    for i in range(len(index_arr)):
        if len(index_arr[i]) != 6:
            index_arr[i] = index_arr[i][len(index_arr[i])-6:]
    if len(index_arr)>1:
        for i in index_arr[1:]:
            currInd = address.find(i, tmp+1)
            tmp_address += address[tmp:currInd] 
            tmp = currInd
        tmp_address += address[tmp:]
        address = tmp_address
    address_arr = address.split(';')
    tmp_address = ''
    for i in range(len(address_arr)-1):
        curr_address = address_arr[i]
        if curr_address[0:4].isdigit() == False:
            curr_address = swap(curr_address)
        pattern_1 = re.compile(r'д\.\s*\d+,*|дом\s*\d+,*|д\. № \d*,*|дом № \d*,*')
        pattern_2 = re.compile(r',\s*\d+')
        house_arr = re.findall(pattern_1, curr_address)
        num_arr = re.findall(pattern_2, curr_address)
        if (re.search(pattern_1, curr_address) != None) & (re.search(pattern_2, curr_address) == None):
            if len(house_arr) > 1:
                template = curr_address[:curr_address.find(house_arr[0])]
                for j in range(len(house_arr) - 1):
                    tmp_address += template + curr_address[curr_address.find(house_arr[j]):curr_address.find(house_arr[j+1])] + ';'
                tmp_address += template + curr_address[curr_address.find(house_arr[-1]):] + ';'
            else:
                tmp_address += curr_address + ';'
        elif (re.search(pattern_1, curr_address) != None) & (re.search(pattern_2, curr_address) != None):
            if len(num_arr) >= 1:
                template = curr_address[:curr_address.find(num_arr[0])]
                tmp_address += template + ';'
                for j in range(len(num_arr) - 1):
                    tmp_address += template[:-2] + curr_address[curr_address.find(num_arr[j])+1:curr_address.find(num_arr[j+1])] + ';'
                tmp_address += template[:-2] + curr_address[curr_address.find(num_arr[-1])+1:] + ';'
            else:
                tmp_address += curr_address + ';'      
        elif (re.search(pattern_1, curr_address) == None) & (re.search(pattern_2, curr_address) != None): 
            if len(num_arr) > 1:
                template = curr_address[:curr_address.find(num_arr[0])]
                for j in range(len(num_arr) - 1):
                    tmp_address += template + curr_address[curr_address.find(num_arr[j]):curr_address.find(num_arr[j+1])] + ';'
                tmp_address += template + curr_address[curr_address.find(num_arr[-1]):] + ';'
            else:
                tmp_address += curr_address + ';'
        elif (re.search(pattern_1, curr_address) == None) & (re.search(pattern_2, curr_address) == None):
            tmp_address += curr_address + ';'
    address = tmp_address
    return address

def f(address):
    tmp = 0
    tmp_address = ''
    address = address.strip(" ")
    index_arr = re.findall(r'\d{6,9}', address)
    for i in range(len(index_arr)):
        if len(index_arr[i]) != 6:
            index_arr[i] = index_arr[i][len(index_arr[i])-6:]
    if (address[:6].isdigit()):
        if len(index_arr)>1:
            for i in index_arr[1:]:
                currInd = address.find(i, tmp+1)
                tmp_address += address[tmp:currInd] + ';'
                tmp = currInd
            tmp_address += address[tmp:]
            address = tmp_address
        address_arr = address.split(';')
        tmp_address = ''
        for i in range(len(address_arr)):
            curr_address = address_arr[i]
            pattern = re.compile(r'ул\.\s*\S*,|ул\.\s*\S*\s*\S*\s*\S*|ул\.\s*\S*\s*\S*\s*\S*,|пер\.\s*\S*,|пл\.\s*\S*,|переулок\s*\S*,|просп\.\s*\S*,|туп\.\s*\S*,')
            street_arr = re.findall(pattern, curr_address)
            if (len(street_arr) > 1):
                template = curr_address[:curr_address.find(street_arr[0])]
                for j in range(len(street_arr) - 1):
                    tmp_address += template + curr_address[curr_address.find(street_arr[j]):curr_address.find(street_arr[j+1])] + ';'
                tmp_address += template + curr_address[curr_address.find(street_arr[-1]):] + ';'
            else:
                tmp_address += curr_address + ';'
        address = tmp_address
        address = split_home(address)
        return address
    else:
        if len(index_arr) > 1:
            for i in index_arr[:-1]:
                currInd = address.find(i, tmp+1) + 6
                tmp_address += address[tmp:currInd] + ';'
                tmp = currInd
            tmp_address += address[tmp:]
            address = tmp_address
        address_arr = address.split(';')
        tmp_address = ''
        for i in range(len(address_arr)):
            curr_address = address_arr[i]
            pattern = re.compile(r'ул\.\s*\S*,|ул\.\s*\S*\s*\S*\s*\S*|ул\.\s*\S*\s*\S*\s*\S*,|пер\.\s*\S*,|пл\.\s*\S*,|переулок\s*\S*,|просп\.\s*\S*,|туп\.\s*\S*,')
            street_arr = re.findall(pattern, curr_address)
            if (len(street_arr) > 1):
                l = curr_address[curr_address.find(street_arr[-1]):]
                house_num = re.search(r'\d+,|\d+\s', l).group(0)
                template = l[l.find(house_num) + len(house_num):].lstrip()
                for j in range(len(street_arr) - 1):
                    tmp_address += curr_address[curr_address.find(street_arr[j]):curr_address.find(street_arr[j+1])] + template + ';'
                tmp_address += curr_address[curr_address.find(street_arr[-1]):] + ';'
            else:
                tmp_address += curr_address + ';'
        address = tmp_address
        address = split_home(address)
        return address

