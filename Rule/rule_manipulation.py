
from reference import *
import re

def format_rule(rule_string: str, sets, verbose=False):

    if verbose: print("Formatting rule \""+rule_string+"\"")
    # Extract user defined sets
    level = 0
    i = 0
    set_string = ""
    new_rule_string = ""
    while i < len(rule_string):
        c = rule_string[i]
        if c == "{":
            level += 1
            set_string += "["
            if level >= 2:
                print("huh? level >= 2 in reference.", rule_string, sets)
                raise Exception("huh? level >= 2 in reference." + str(rule_string) + " " + str(sets))
        elif c == "}":
            set_string += "]"
            new_rule_string += "%s" + str(len(sets))
            sets.append(string_to_list(set_string))
            set_string = ""
            level -= 1
        elif level == 1:
            set_string += c
        elif level == 0:
            new_rule_string += c
        i += 1

    rule_string = new_rule_string

    if verbose: print("Extracted user sets. rule: \""+rule_string+"\"", "sets:", sets)

    # We can now change the rule to be lowercase
    rule_string = rule_string.lower()

    # Delete Nth, Nst, Nrd, (Ordinal Indicators) etc. Don't change to a for loop, as we need to go backward
    rule_string = re.sub(r"(?<=\d)(st|nd|rd|th)\b", '', rule_string)

    if verbose: print("Made lower and removed ordinals. Now:",rule_string, sets)

    rule_string = rule_string.replace("words", "word")
    rule_string = rule_string.replace("letters", "letter")

    # Put parentheses around (<Set> s#)[] -> (<Set> s#[])
    rule_string = rule_string.replace(")[", "[")
    rule_string = rule_string.replace("]", "])")

    # Put parentheses inside (<Set s#[]) -> (<Set> s#[()])
    rule_string = rule_string.replace("[", "[(")
    rule_string = rule_string.replace("]", ")]")

    if verbose: print("Before number_of formatting:",rule_string)

    # For number_of, replace s# and l# with %c#
    i = 0
    while i < len(rule_string):
        if rule_string[i] == " ":
            if rule_string[i+1] == "s":
                nums = find_next_number(rule_string[i+2:])
                if nums != "": # To avoid rules which include words starting with s
                    nums = int(nums)
                    if verbose: print("s", nums)
                    rule_string = rule_string.replace("s"+str(nums), "%c"+str(nums*2)) # Make positions the even numbers
            elif rule_string[i+1] == "l":
                numl = find_next_number(rule_string[i+2:])
                if numl != "": # To avoid rules which include words starting with l
                    numl = int(numl)
                    rule_string = rule_string.replace("l"+str(numl), "%c"+str(numl*2 + 1)) # Make relative the odd numbers
        i += 1

    if verbose: print("Post formatting:",rule_string)

    return rule_string

# Find a rule composed of only primitives
def find_min_rule(rule: str):

    endIndex = rule.find(")")

    # If there are no parentheses, we must have only the top level condition to analyse
    if endIndex == -1:
        return rule, False

    else:
        startIndex = endIndex
        while True:
            if rule[startIndex-1] == "(":
                break
            else:
                startIndex -= 1
        return rule[startIndex:endIndex], True


if __name__ == "__main__":

    print(format_rule("(word s1, next l1)[((letter s2, next l2)[letter is palindrome]) == length of letter)] == (length of word)", []))

