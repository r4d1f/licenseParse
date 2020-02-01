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

'''def split(address):
    index_arr = re.findall(r'\d{6,9}', address)
    if (not address[0:6].split()[0].isdigit()):
        address = swap(address)
    for i in range(len(index_arr)):
        if len(index_arr[i]) != 6:
            index_arr[i] = index_arr[i][len(index_arr[i])-6:]
    new_adrress = ''
    tmp = 0
    print(index_arr)
    if len(index_arr)>1:
        for i in index_arr[1:]:
            currInd = address.find(i, tmp+1)
            new_adrress += address[tmp:currInd] + ';'
            tmp = currInd
        print(tmp)
        new_adrress += address[tmp:]
    else:
        return address
    return new_adrress'''

#def rsplit(address)

def f(address):
    address = address.strip(" ")
    index_arr = re.findall(r'\d{6,9}', address)
    if (len(re.findall(r'\d{4,9}', address.split(',')[0])) == 0):
        address = swap(address)
    for i in range(len(index_arr)):
        if len(index_arr[i]) != 6:
            index_arr[i] = index_arr[i][len(index_arr[i])-6:]
    new_adrress = ''
    tmp = 0
    if len(index_arr)>1:
        for i in index_arr[1:]:
            currInd = address.find(i, tmp+1)
            new_adrress += address[tmp:currInd] + ';'
            tmp = currInd
        new_adrress += address[tmp:]
    else:
        return address
    return new_adrress