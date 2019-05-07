
import ast, re

locations = ["next", "previous", "last", "first", "opposite"]

def contains_substring(string, substring):
    return substring.lower() in string.lower()

def split_to_words(sentence):
    if type(sentence) is str:
        return sentence.split(" ")
    elif type(sentence) is list:
        return sentence
    else:
        print("split_to_words takes string or list, got,",sentence)
        raise Exception("split_to_words takes string or list, got "+str(sentence))

def split_to_letters(sentence, verbose=False):
    letters = []
    if verbose: print("getting letters from:",sentence)

    if type(sentence) is list:
        sentence = sentence.join("")

    for s in sentence:
        if s != " ":
            letters.append(s)

    if verbose: print("got letters:",letters)
    return letters

# Given a string, finds digits until characters, then reports the string of the digits found. eg. "012hello" -> "012"
def find_next_number(s: str):
    number = ""

    while True:
        # Pop off first digit
        nextDigit = s[0]
        s = s[1:]

        if nextDigit.isdigit():
            number += nextDigit
        else:
            return number

        if len(s)==0:
            return number

def find_indexes_of(string: str, substring: str):
    return [m.start() for m in re.finditer(substring, string)]

def string_to_list(list_as_string: str):
    list_as_string = list_as_string.strip()
    return ast.literal_eval(list_as_string)

