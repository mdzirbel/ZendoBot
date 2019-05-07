
import json

########################################  Saved Rules  ########################################

def save_rule(rule_id, rule): #saved_rules: dict):

    _saved_rules[rule_id] = rule

    with open("Saved/saved_rules.json", "w") as file:
        json.dump(_saved_rules, file)

def get_saved_rules():
    return _saved_rules

def _load_saved_rules():

    try:
        with open('Saved/saved_rules.json', "r") as json_file:
            rules = json.load(json_file)

        return rules

    except FileNotFoundError:
        print("Couldn't open saved_rules file to read (it will be made next time you save)")
        return {}

########################################  Saved Rule References  ########################################

def save_rule_reference(rule_key, rule):

    _saved_rule_references[rule_key] = rule

    with open("Saved/saved_rule_references.json", "w") as file:
        json.dump(_saved_rule_references, file)

def has_rule_reference(rule_key):
    return rule_key in _saved_rule_references

def get_rule_reference(rule_key):
    return _saved_rule_references[rule_key]

def _load_rule_references():

    try:
        with open('Saved/saved_rule_references.json', "r") as json_file:
            rule_references = json.load(json_file)

        return rule_references

    except FileNotFoundError:
        print("Couldn't open rule_references file to read (it will be made next time you save)")
        return {}

########################################  Saved Checked Guesses ########################################

def _save_checked_guesses():
    with open("Saved/saved_checked_guesses.json", "w") as file:
        json.dump(_saved_checked_guesses, file)

def save_checked_guess(channel_id, guess, result):

    channel_id = str(channel_id)

    if channel_id in _saved_checked_guesses:
        print(_saved_checked_guesses[channel_id], (guess, result))
        print((guess, result) in _saved_checked_guesses[channel_id])
        if not [guess, result] in _saved_checked_guesses[channel_id]: # Don't add repeats
            _saved_checked_guesses[channel_id].append([guess, result])
    else:
        _saved_checked_guesses[channel_id] = [(guess, result)]

    _save_checked_guesses()

def clear_checked_guesses(channel_id):

    channel_id = str(channel_id)

    _saved_checked_guesses.pop(channel_id, None) # Removes key from dictionary

    _save_checked_guesses()

def get_checked_guesses(channel_id):

    channel_id = str(channel_id)

    return _saved_checked_guesses.get(channel_id, [])

def _load_checked_guesses():

    try:
        with open('Saved/saved_checked_guesses.json', "r") as json_file:
            rule_references = json.load(json_file)

        return rule_references

    except FileNotFoundError:
        print("Couldn't open saved_checked_guesses file to read (it will be made next time you save)")
        return {}


_saved_rules = _load_saved_rules()
_saved_rule_references = _load_rule_references()
_saved_checked_guesses = _load_checked_guesses()