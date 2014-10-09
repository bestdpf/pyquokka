def make2dList(row, col, val):
    lst = []
    for i in xrange(row):
        lst += [[val]*col]
    return lst
