
def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

def extracter(x, y, raw):
    """x = query
       y --> 0 - Away table
             1 - Home table
             2 - Away P Table
             3 - Home P Table
    """
    tableindex = list(find_all(raw, 'Team Totals'))
    awaytable = raw[tableindex[y]:tableindex[y] + 750]
    x = f'{x}" >'
    return awaytable[awaytable.find(x)+len(x):][:awaytable[awaytable.find(x)+len(x):].find('</td>')]