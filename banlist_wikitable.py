from keywords import *
from banlist_cardlister import Node_BST, NAME_BST
from banlist_cardlister import list_formatdates
from banlist_cardlister import output_tree
from banlist_data_generator import *
from card_data import *
import time

class Annual_Lists:
    def __init__(self, year: int, year_list: list):
        self.year = year
        self.updates = year_list

    def __str__(self):
        return str(self.year) + str(self.updates)

def generate_header(region:str, year1:int, year2:int):
    date_list = get_formatdates(region)
    date_tree = []
    year_list = []
    year, mo = None, None

    for date in date_list:
        if date[0] >= year1 and date[0] <= year2:
            if not year and not mo:
                year_list.append(date[1])
            elif date[0] != year:
                date_tree.append(Annual_Lists(year, year_list))
                year_list = [date[1]]
            else:
                year_list.append(date[1])
            year, mo = date[0], date[1]
    date_tree.append(Annual_Lists(year, year_list))

    def calculate_width(updates:list):
        return 160 + 120*len(updates)

    header = "<div style=\"font-size:8pt; font-family:monospace\">\n"
    header += "{| class=\"wikitable\" "
    header += "style=\"width: " + str(calculate_width(date_tree)) + "px"
    header += "; line-height: 10pt\"\n"
            
    return header

def generate_date_row(region, year1, year2):
    date_list = get_formatdates(region)
    date_tree = []
    year_list = []
    year, mo = None, None

    for date in date_list:
        if date[0] >= year1 and date[0] <= year2:
            if not year and not mo:
                year_list.append(date[1])
            elif date[0] != year:
                date_tree.append(Annual_Lists(year, year_list))
                year_list = [date[1]]
            else:
                year_list.append(date[1])
            year, mo = date[0], date[1]
    date_tree.append(Annual_Lists(year, year_list))
    
    header = "|-\n"
    header += "! rowspan=2 scope=\"col\" style=\"width: 160px\"| Card\n"
    for date_year in date_tree:
        header += "! colspan=" + str(len(date_year.updates)) + " scope=\"col\""
        header += " style=\"width:120px\""
        header += "|" + str(date_year.year) + "\n"
    header += "|-\n"
    
    for date_year in date_tree:
        def month_name(mo:int):
            switch = {
                1:"JAN",2:"FEB",3:"MAR",4:"APR",5:"MAY",6:"JUN",
                7:"JUL",8:"AUG",9:"SEP",10:"OCT",11:"NOV",12:"DEC"
            }
            return switch.get(mo, "INI")
        for mo in date_year.updates:
            header += "! colspan=1"
            header += " scope=\"col\""
            header += "|" + month_name(mo) + "\n"
    return header

def generate_card_rows(region:str, year1:int, year2:int, alph1=None, alph2=None):
    card_rows = ""
    date_list = get_formatdates(region)
    cardstatuses = get_CG(region)
    if not cardstatuses:
        raise Exception("Card Statuses")

    def generate_row(card:Card):
        row = ""
        row += "|-\n"
        row += "| scope\"row\" | " + "[[" + card.name + "]] "
        enc = historical_statuses(card, region)

        def cardstatus_background(status:int) -> str:
            switch = {
                STATUS_UNRELEASED:"Did not exist",
                STATUS_UNLIMITED:"Unlimited",
                STATUS_SEMILIMITED:"Semi-limited",
                STATUS_LIMITED:"Limited",
                STATUS_FORBIDDEN:"Forbidden",
            }
            return switch.get(status, "Illegal")

        # Row generation begins here
        def cardstatus_entry(enc:CardHistory) -> str:
            string = "{{"
            string += cardstatus_background(enc.status)
            if enc.notes:
                string += "|" + enc.notes
            string += "}}"
            return string
        
        i = 0
        while i < len(date_list) and date_list[i][0] <= year2:
            if date_list[i][0] >= year1:
                row += "|| " + cardstatus_entry(enc.index(i))
            i += 1
        row += "\n"
        
        return row

    count = 0
    card_rows += generate_date_row(region, year1, year2)
    for card in cardstatuses:
        if not alph1 and not alph2 and count > 0 and count % 48 == 0:
            card_rows += generate_date_row(region, year1, year2)

        if not alph1 or card.name[0] >= alph1:
            if not alph2 or card.name[0] <= alph2:
                card_rows += generate_row(card)
            
        count += 1
        
    return card_rows

def generate_end():
    footer = "|}"
    footer += "</div>"
    return footer

def generate_table(region:int, year1:int, year2:int, alph1=None, alph2=None):
    elapsed = time.time()
    filename = "wikitables/updates_%s-%d%d" %(region, year1, year2)
    if alph1:
        filename += alph1
    else:
        filename += "@"
    if alph2:
        filename += alph2
    else:
        filename += "@"
    filename += ".txt"
    file = open(filename, 'w')
    
    file.write(generate_header(region, year1, year2))
    file.write(generate_card_rows(region, year1, year2, alph1, alph2))
    file.write(generate_end())
    file.close()
    
    elapsed = time.time() - elapsed
    print("Generate %s files from %d-%d %s-%s: %fs" %(region, year1, year2, alph1, alph2, elapsed))

file = open("updates_tcg.txt", 'w')
for card in get_CG("TCG"):
    file.write(str(card) + "\n")
    file.write(str(historical_statuses(card, "TCG")) + "\n\n")
file.close()

file = open("updates_ocg.txt", 'w')
for card in get_CG("OCG"):
    file.write(str(card) + "\n")
    file.write(str(historical_statuses(card, "OCG")) + "\n\n")
file.close()

generate_table("OCG", 1998, 2004)
generate_table("OCG", 2002, 2013)
generate_table("TCG", 2002, 2013)

generate_table("OCG", 2013, 2018)
generate_table("TCG", 2013, 2018)

generate_table("OCG", 2002, 2018)
generate_table("TCG", 2002, 2018)
