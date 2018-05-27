from pathlib import Path

KEYWORD_FORMAT = "format"
KEYWORD_UPDATE = "update"

def generate_formatfile(region:str, year:int, mo:int):
    p = Path("%04d_%02d.txt" %(year, mo))
    
    if not p.is_file():
        newlist = open(p, "w")
        newlist.write("format %s\n" %region)
        newlist.write("year %04d-%02d\n\n" %(year, mo))
        newlist.write("#LIST")
        newlist.close()
        print("%04d_%02d.txt " %(year, mo) + "generated.")
    else:
        print("%04d_%02d.txt " %(year, mo) + "exists.")
    
formatlists = open("dates.txt", "r")
region, year, mo = (None, None, None)
for line in formatlists:
    line = line.rstrip()

    if line.find(KEYWORD_FORMAT) >= 0:
        index = line.find(KEYWORD_FORMAT)
        region = line[index + len(KEYWORD_FORMAT) + 1:]
    elif line.find(KEYWORD_UPDATE) >= 0:
        index = line.find(KEYWORD_UPDATE)
        line = line[index + len(KEYWORD_UPDATE) + 1:]
        year = int(line[0:4])
        mo = int(line[5:7])
        
        generate_formatfile(region, year, mo)
formatlists.close()
