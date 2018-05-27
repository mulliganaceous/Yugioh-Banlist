"""
Base banlist class which processes the date files and all the
banlist text files.

Version: Alpha
"""

from pathlib import Path
from keywords import *
from fsm import status_change

class Node_BST:
    """
    Represents a binary search tree node holding strings.
    """
    def __init__(self, name:str):
        """ Constructor for a BST node """
        self.name = name
        self.left = None
        self.right = None

    def __add__(self, name: str):
        """ Adds an additional node to the BST """
        if (name == self.name):
            return self
        elif (name < self.name):
            if (self.left):
                self.left += name
            else:
                self.left = Node_BST(name)
        elif (name > self.name):
            if (self.right):
                self.right += name
            else:
                self.right = Node_BST(name)
        return self

    def __str__(self):
        """ Prints the elements of the BST in ascending order """
        string = ""
        if (self.left):
            string += str(self.left)
        string += self.name + "\n"
        if (self.right):
            string += str(self.right)
            
        return string

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

def process_formatfiles(bst: Node_BST, date_list:list, region:str) -> Node_BST:
    """ Obtain the BST of name files by datelist and region. """
    for date in date_list:
        year = date[0]
        mo = date[1]
        
        folder = "lists_" + region + "/"
        listfile = open(folder + "%04d_%02d.txt" %(year, mo), 'r')
        
        for line in listfile:
            line = line.rstrip()

            name = status_change(line)
            if name and not bst:
                bst = Node_BST(name)
            if name and bst:
                bst += name
            
        listfile.close()
    
    print(region + " cards on lists added to binary search tree.")    
    return bst

def generate_names(bst: Node_BST) -> None:
    """ Write the name file """
    namefile = open("names.txt", 'w')
    namefile.write(str(bst))
    namefile.close()
    print("Name file created.")

def generate_cards() -> None:
    """ Write the supplementary card info file, if it does not exist. """
    folder = "cards/"
    names = open("names.txt", 'r')
    count = 0
    for line in names:
        line = line.rstrip()
        filename = line.replace("/", "&slash")
        filename = filename.replace("\"", "&quote")
        filename = filename.replace(":", "&colon")
        p = Path(folder + filename + ".txt")
        if not p.is_file():
            card = open(p, 'w')
            card.write("card \"" + line + "\" {\n")
            card.write("\t" + "release ocg " + "\n")
            card.write("\t" + "release tcg " + "\n")
            card.write("\t" + "type " + "\n")
            card.write("}\n\n")
            count += 1
            card.close()
        else:
            print(line + " exists.")
    print("%d card files created." %count)

# PROCESS SEGMENT
TCG_LIST = list_formatdates("TCG")
OCG_LIST = list_formatdates("OCG")
NAME_BST = None
NAME_BST = process_formatfiles(NAME_BST, TCG_LIST, "TCG")
NAME_BST = process_formatfiles(NAME_BST, OCG_LIST, "OCG")
generate_names(NAME_BST)

def str_depth(bst: Node_BST, dep: str) -> str:
    nametree = ""
    # Print number of asterisks based on depth, then name
    nametree += dep + "" + bst.name + "\n"
    # Recurse lower half
    if bst.left:
        nametree += str_depth(bst.left, dep + "<")
    # Recurse upper half
    if bst.right:
        nametree += str_depth(bst.right, dep + ">")
    return nametree

def size(bst: Node_BST) -> int:
    k = 0
    if bst.left:
        k += size(bst.left)
    if bst.right:
        k += size(bst.right)
    return k + 1

def output_tree() -> None:
    print(str_depth(NAME_BST,""))
    print(size(NAME_BST))