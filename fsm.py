from keywords import *

def _is_status_keyword(word: str) -> bool:
    switch = {
        KEYWORD_UNLIMIT: True,
        KEYWORD_SEMILIMIT: True,
        KEYWORD_LIMIT: True,
        KEYWORD_FORBID: True
    }
    return switch.get(word, False)

def _is_modifier_keyword(word: str) -> bool:
    switch = {
        KEYWORD_EMERGENCY: True,
        KEYWORD_NERF: True
    }
    return switch.get(word, False)

def _is_header_keyword(word: str) -> bool:
    switch = {
        KEYWORD_FORMAT: True,
        KEYWORD_YEAR: True,
        KEYWORD_ANALOGUE: True
    }
    return switch.get(word, False)
    
def status_change(line: str):
    word = ""
    state = 0
    
    for k in range(len(line)):
        if state == 0:
            if line[0] == "#":
                return None
            if line[k] == ' ':
                if _is_status_keyword(word):
                    state = 10
                elif _is_modifier_keyword(word):
                    word = ""
                    state = 1
                elif _is_header_keyword(word):
                    return None
                else:
                    raise Exception(word, line)
            else:
                word += line[k]
        elif state == 1:
            if line[k] == ' ':
                if _is_status_keyword(word):
                    state = 10
                else:
                    raise Exception(word, line)
            else:
                word += line[k]
                
        elif state == 10:
            word = ""
            if line[k] == '"':
                state = 11
        elif state == 11:
            if line[k] == '\\':
                state = 12
            elif line[k] == '"':
                state = 20
            else:
                word += line[k]
        elif state == 12:
            if line[k] == '"':
                word += line[k]
                state = 11
        elif state == 20:
            return word
    # End of FSM

    if state == 20:
        return word
    return None
# End of fsm accepting update commands

def parse_update_line(line: str, region: str, date: int):
    word = ""
    state = 0

    status_str = None
    notes_str = None
    name = None
    
    
    for k in range(len(line)):
        if state == 0:
            if line[0] == "#":
                return None
            if line[k] == ' ':
                if _is_status_keyword(word):
                    status_str = word
                    state = 10
                elif _is_modifier_keyword(word):
                    notes_str = word
                    word = ""
                    state = 1
                elif _is_header_keyword(word):
                    return None
                else:
                    raise Exception(word, line)
            else:
                word += line[k]
        elif state == 1:
            if line[k] == ' ':
                if _is_status_keyword(word):
                    status_str = word
                    state = 10
                else:
                    raise Exception(word, line)
            else:
                word += line[k]
                
        elif state == 10:
            word = ""
            if line[k] == '"':
                state = 11
        elif state == 11:
            if line[k] == '\\':
                state = 12
            elif line[k] == '"':
                name = word
                state = 20
            else:
                word += line[k]
        elif state == 12:
            if line[k] == '"':
                word += line[k]
                state = 11
        elif state == 20:
            word = '"'
    # End of FSM

    if state == 20:
        from card_data import Update
        return (Update(region, date, status_str, notes_str), name)
    
    return None
