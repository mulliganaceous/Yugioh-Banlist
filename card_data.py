from keywords import *
class Card:
    def __init__(self, name:str):
        self.name = name
        self.status_changes = []

    def append_changes(self, update_info):
        self.status_changes.append(update_info)

    def __str__(self):
        return self.name

class Update:
    def __init__(self, region:str, date, status_str, notes_str):
        self.region = region
        self.date = date
        self.status = status_str
        self.notes = notes_str

    def __str__(self):
        return str(self.region) + str(self.date) + str(self.status) + str(self.notes)

class CardUpdates:
    def __init__(self):
        self.history = []

    def __str__(self):
        string = ""
        for h in self.history:
            string += str(h)
        return string

    def append(self, status, notes):
        self.history.append(CardHistory(status, notes))

    def index(self, k):
        return self.history[k]

class CardHistory:
    def __init__(self, status, notes):
        self.status = status
        self.notes = notes

    def __str__(self):
        def _char_notes(notes):
            switcher = {
                KEYWORD_ERRATA:"e",
                KEYWORD_NERF:"E",
                KEYWORD_EMERGENCY:"L",
            }
            return switcher.get(notes, ".")
        
        return str(self.status) + _char_notes(self.notes) + " "
