import re

def f(address):
    index_arr = re.findall(r'\d{6,9}', address)
    if (index_arr[0] != address[0:6] or len(index_arr) == 1):
        return address
    for i in range(len(index_arr)):
        if len(index_arr[i]) != 6:
            index_arr[i] = index_arr[i][len(index_arr[i])-6:]
    new_adrress = ''
    tmp = 0
    print(index_arr)
    for i in index_arr[1:]:
        currInd = address.find(i, tmp+1)
        new_adrress += address[tmp:currInd] + ';'
        tmp = currInd
    return new_adrress