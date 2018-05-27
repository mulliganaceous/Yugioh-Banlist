from datelist import *
OCG_LIST = list_formatdates("OCG")
TCG_LIST = list_formatdates("TCG")

def errorcheck(badname):
    _error_check_format(badname, OCG_LIST, "OCG")
    _error_check_format(badname, TCG_LIST, "TCG")

def _error_check_format(badname:str, date_list:list, region:str):
    for date in date_list:
        year = date[0]
        mo = date[1]
        
        folder = "lists_" + region + "/"
        listfile = open(folder + "%04d_%02d.txt" %(year, mo), 'r')
        for line in listfile:
            line = line.rstrip()
            if line.find("\"") >= 0:
                name = line[line.index("\"") + 1:]
                name = name[:name.index("\"")]
                if badname == name:
                    print(region, date, ":", badname)
        listfile.close()
