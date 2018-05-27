from keywords import *

def list_formatdates(region:str) -> list:
    """ Converts a format dates file into a list """
    dates = []
    folder = "lists_" + region

    datefile = open(folder + "/dates.txt", 'r')
    for line in datefile:
        line = line.rstrip()

        if line.find(KEYWORD_UPDATE) >= 0:
            index = line.find(KEYWORD_UPDATE)
            line = line[index + len(KEYWORD_UPDATE) + 1:]
            year = int(line[0:4])
            mo = int(line[5:7])
            dates.append((year,mo))
            
    datefile.close()
    return dates
