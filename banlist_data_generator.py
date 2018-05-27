from keywords import *
from banlist_cardlister import Node_BST, NAME_BST
from banlist_cardlister import list_formatdates
from banlist_cardlister import output_tree
from fsm import parse_update_line
from card_data import *
import time

# Preliminary Methods
def get_formatdates(region:str) -> list:
    """ Quickly obtain the dates """
    switch = {
        "TCG": TCG_UPDATES,
        "OCG": OCG_UPDATES
    }
    return switch.get(region, list_formatdates(region))

def list(bst: Node_BST) -> list:
    """ Converts the name BST into a sorted list. """
    name_list = []
    def helper(bst: Node_BST):
        if bst.left:
            helper(bst.left)
        name_list.append(bst.name)
        if bst.right:
            helper(bst.right)

    helper(bst)
    return name_list

# Global Variables
TCG_UPDATES = list_formatdates("TCG")
OCG_UPDATES = list_formatdates("OCG")
CARD_LIST = list(NAME_BST)

# Methods
def _generate_cardlist(bst: Node_BST) -> list:
    """ Converts the name BST into a sorted list of Card objects """
    card_list = []
    def helper(bst: Node_BST):
        if bst.left:
            helper(bst.left)
        card = Card(bst.name)
        card_list.append(card)
        if bst.right:
            helper(bst.right)

    helper(bst)
    return card_list

def index_of(name:str, card_list=None) -> int:
    # If the card list is not provided, convert the existing NAME_BST
    if not card_list:
        card_list = _generate_cardlist(NAME_BST)
        
    ini = 0
    fin = len(card_list) - 1
    mid = (ini + fin) // 2

    while ini <= fin:
        if name < card_list[mid].name:
            fin = mid - 1
        elif name > card_list[mid].name:
            ini = mid + 1
        elif name == card_list[mid].name:
            return mid
        mid = (ini + fin) // 2
        
    return -1

def get_card(name:str, card_list=None) -> Card:
    if not card_list:
        card_list = _generate_cardlist(NAME_BST)

    return card_list[index_of(name, card_list)]
        
def generate_cardstatuses(region:str) -> list:
    card_list = _generate_cardlist(NAME_BST)
    updates = get_formatdates(region)
    
    for date in updates:
        year = date[0]
        mo = date[1]
        
        folder = "lists_" + region + "/"
        listfile = open(folder + "%04d_%02d.txt" %(year, mo), 'r')
        
        for line in listfile:
            line = line.rstrip()
            update_line = parse_update_line(line, region, date)
            if update_line:
                update_info = update_line[0]
                update_cardname = update_line[1]
                index = index_of(update_cardname)
                if index >= 0:
                    card_list[index].append_changes(update_info)
        listfile.close()

    return card_list

def historical_statuses(card:Card, region:str) -> CardHistory:
    date_list = get_formatdates(region)

    def _int_status(str_status:str):
        switcher = {
            KEYWORD_UNLIMIT:STATUS_UNLIMITED,
            KEYWORD_SEMILIMIT:STATUS_SEMILIMITED,
            KEYWORD_LIMIT:STATUS_LIMITED,
            KEYWORD_FORBID:STATUS_FORBIDDEN,
        }
        return switcher.get(str_status, -1)

    def _char_notes(str_status:str):
        switcher = {
            KEYWORD_ERRATA:"e",
            KEYWORD_NERF:"E",
            KEYWORD_EMERGENCY:"L",
        }
        return switcher.get(str_status, None)
        
    history = CardUpdates()
    index = 0
    next_update = None
    if len(card.status_changes) > 0:
        next_update = card.status_changes[index]
    
    status = STATUS_UNRELEASED
    notes = None
    for date in date_list:
        if next_update and date == next_update.date:
            status = _int_status(next_update.status)
            notes = _char_notes(next_update.notes)
            index += 1
            if index < len(card.status_changes):
                next_update = card.status_changes[index]

        history.append(status, notes)
        notes = None
        
    return history

def generate_page(bst: Node_BST):
    """ Generates a table to track for errors. """
    table = open("page_table.txt.", 'w')
    table.write("{|\n")
    table.write("|-\n!Card\n")
    name_list = list(NAME_BST)
    for name in name_list:
        table.write("|-\n| " + "[[" + name + "]]\n")
    table.write("|}\n")
    table.close()

# Table Source Code Printer
output_tree()

elapsed = time.time()
TCG = generate_cardstatuses("TCG")
elapsed = time.time() - elapsed
print("TCG Updates: %fs" %elapsed)

elapsed = time.time()
OCG = generate_cardstatuses("OCG")
elapsed = time.time() - elapsed
print("OCG Updates: %fs" %elapsed)

def get_CG(region:str):
    switch = {
        "TCG":TCG,
        "OCG":OCG
    }
    return switch.get(region, None)

file = open("updates_tcg.txt", 'w')
for card in TCG:
    file.write(str(card) + "\n")
    file.write(str(historical_statuses(card, "TCG")) + "\n\n")
file.close()

file = open("updates_ocg.txt", 'w')
for card in OCG:
    file.write(str(card) + "\n")
    file.write(str(historical_statuses(card, "OCG")) + "\n\n")
file.close()
