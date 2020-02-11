import re

def f1(address):
    split_address = split(address)
    arr_address = split_address.split(";")

def swap(address):
    arr_address = address.split(',')
    res = ''
    for i in range(len(arr_address)):
        res += arr_address[len(arr_address)-1-i] + ','
    return res[:-1].lstrip(" ")


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
            pattern = re.compile(r'ул\.\s*\S*,|пер\.\s*\S*,|пл\.\s*\S*,|переулок\s*\S*,|просп\.\s*\S*,|туп\.\s*\S*,')
            street_arr = re.findall(pattern, curr_address)
            if (len(street_arr) > 1):
                template = curr_address[:curr_address.find(street_arr[0])]
                for j in range(len(street_arr) - 1):
                    tmp_address += template + curr_address[curr_address.find(street_arr[j]):curr_address.find(street_arr[j+1])] + ';'
                tmp_address += template + curr_address[curr_address.find(street_arr[-1]):] + ';'
            else:
                tmp_address += curr_address + ';'
        address = tmp_address
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
            pattern = re.compile(r'ул\.\s*\S*,|пер\.\s*\S*,|пл\.\s*\S*,|переулок\s*\S*,|просп\.\s*\S*,|туп\.\s*\S*,')
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
        return address