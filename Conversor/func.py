def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def isint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def parsing_int_float(num:str):
    if "," in num: num = num.replace(',','.')

    if isint(num):
        return int(num)
    elif isfloat(num):
        return float(num)
    else:
        return 'Erro'  

def casting_str(num:float or int, flag:bool):    
    s = str(num)
    if len(s) > 15: s = ''
    elif "." in s and flag: s = s.replace('.',',')
    return s
