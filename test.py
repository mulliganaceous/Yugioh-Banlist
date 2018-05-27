from banlist_data_generator import *

def generate_errata_notes(CG:list):
    string = ""
    for card in CG:
        updated = False
        for update in card.status_changes:
            if update.notes != None:
                if not updated:
                    string += card.name + "\n"
                    updated = True
                string += str(update) + "\n"
        if updated:
            string += "\n"
    return string

file = open("errata_OCG.txt", 'w')
file.write(generate_errata_notes(OCG))
file.close()
file = open("errata_TCG.txt", 'w')
file.write(generate_errata_notes(TCG))
file.close()
