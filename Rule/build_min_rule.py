
from Rule.node import Node
from reference import *

def build_min_rule(min_rule, subrules, verbose=True):

    if verbose: print("Building min_rule:",min_rule)

#########################  number_of   #########################

    if "[" in min_rule and "]" in min_rule: # number_of
        if verbose: print("Building number_of node")

        # parameters[0] = set to look through
        # parameters[1] = index to hold current at
        # parameters[2] = what the relation is, or None
        # parameters[3] = index to hold relation at, or None
        # parameters[4] = inner rule, to iterate over

        set1 = min_rule.split()[0]
        if verbose: print(set1)

        index_current = int(find_next_number(min_rule.split()[1][2:])) # Trim the %c off the front and , off the back and it should just be the index
        if verbose: print(index_current)

        if len(min_rule.split()) >= 3 and min_rule.split()[2] in locations:
            relation = min_rule.split()[2]
            relation_index = int(find_next_number(min_rule.split()[3][2:]))
        else:
            relation = None
            relation_index = None

        if verbose: print(relation)
        if verbose: print(relation_index)

        inner_rule = min_rule[min_rule.find("[")+1 : min_rule.find("]")]
        if verbose: print(inner_rule)

        min_rule_node = Node("number_of", "operation", [set1, index_current, relation, relation_index, inner_rule])

#########################  Conditions  #########################

    elif "true" in min_rule: # true
        if verbose: print("Building true node")
        min_rule_node = Node("true", "condition", [])

    elif "false" in min_rule: # false
        if verbose: print("Building false node")
        min_rule_node = Node("false", "condition", [])

    elif " is palindrome" in min_rule: # palindrome

        if verbose: print("Building palindrome node")

        condition_index = min_rule.find("is palindrome")

        set1 = min_rule[0: condition_index].strip()

        if verbose: print("set -"+set1+"-")

        min_rule_node = Node("palindrome", "condition", [set1])

    elif " == " in min_rule: # equal

        if verbose: print("Building equal node")

        condition_index = min_rule.find("==")

        set1 = min_rule[0: condition_index].strip()

        set2 = min_rule[condition_index + len("=="): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + set2 + "-")

        min_rule_node = Node("equal", "condition", [set1, set2])

    elif " >= " in min_rule:  # greater_equal

        if verbose: print("Building greater_equal node")

        condition_index = min_rule.find(">=")

        set1 = min_rule[0: condition_index].strip()

        set2 = min_rule[condition_index + len(">="): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + set2 + "-")

        min_rule_node = Node("greater_equal", "condition", [set1, set2])

    elif " <= " in min_rule:  # less_equal

        if verbose: print("Building less_equal node")

        condition_index = min_rule.find("<=")

        set1 = min_rule[0: condition_index].strip()

        set2 = min_rule[condition_index + len("<="): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + set2 + "-")

        min_rule_node = Node("less_equal", "condition", [set1, set2])

    elif " > " in min_rule:  # greater

        if verbose: print("Building greater node")

        condition_index = min_rule.find(">")

        set1 = min_rule[0: condition_index].strip()

        set2 = min_rule[condition_index + len(">"): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + set2 + "-")

        min_rule_node = Node("greater", "condition", [set1, set2])

    elif " < " in min_rule:  # less

        if verbose: print("Building less node")

        condition_index = min_rule.find("<")

        set1 = min_rule[0: condition_index].strip()

        set2 = min_rule[condition_index + len("<"): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + set2 + "-")

        min_rule_node = Node("less", "condition", [set1, set2])

    elif " and " in min_rule:  # and

        if verbose: print("Building and node")

        condition_index = min_rule.find("and")

        set1 = min_rule[0: condition_index].strip()

        set2 = min_rule[condition_index + len("and"): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + set2 + "-")

        min_rule_node = Node("and", "condition", [set1, set2])

    elif " or " in min_rule:  # or

        if verbose: print("Building or node")

        condition_index = min_rule.find(" or ")

        set1 = min_rule[0: condition_index].strip()

        set2 = min_rule[condition_index + len(" or "): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + set2 + "-")

        min_rule_node = Node("or", "condition", [set1, set2])

    elif "not " in min_rule:  # not

        if verbose: print("Building not node")

        condition_index = min_rule.find("not")

        set1 = min_rule[condition_index + len("not"): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        min_rule_node = Node("not", "condition", [set1])

    elif " contains " in min_rule and "case sensitive" in min_rule: # case_contains

        if verbose: print("Building case_contains node")

        condition_index = min_rule.find("contains")

        set1 = min_rule[0: condition_index].strip()

        set2 = min_rule[condition_index + len("contains"): len(min_rule) - len("case sensitive")].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + set2 + "-")

        min_rule_node = Node("case_contains", "condition", [set1, set2])

    elif " contains " in min_rule: # contains

        if verbose: print("Building contains node")

        condition_index = min_rule.find("contains")

        set1 = min_rule[0: condition_index].strip()

        set2 = min_rule[condition_index + len("contains"): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + set2 + "-")

        min_rule_node = Node("contains", "condition", [set1, set2])

    elif "is case sensitive subset of" in min_rule: # case_contains

        if verbose: print("Building case_contains node")

        condition_index = min_rule.find("is case sensitive subset of")

        set1 = min_rule[0: condition_index].strip()

        set2 = min_rule[condition_index + len("is case sensitive subset of"): len(min_rule)+1].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + set2[:30] + "-")

        min_rule_node = Node("case_subset", "condition", [set1, set2])

    elif " is subset of " in min_rule:  # subset
        if verbose: print("Building subset node")
        condition_index = min_rule.find("is subset of")
        set1 = min_rule[0: condition_index].strip()
        set2 = min_rule[condition_index + len("is subset of"): len(min_rule)+1].strip()
        if verbose: print("set1 -" + set1 + "-")
        if verbose: print("set2 -" + set2[:30] + "-")
        min_rule_node = Node("subset", "condition", [set1, set2])

    elif " is lowercase" in min_rule:  # is_lowercase

        if verbose: print("Building lowercase node")

        condition_index = min_rule.find("is lowercase")

        set1 = min_rule[0: condition_index].strip()

        if verbose: print("set1 -" + set1 + "-")

        min_rule_node = Node("is_lowercase", "condition", [set1])

    elif " is uppercase" in min_rule:  # is_uppercase

        if verbose: print("Building uppercase node")

        condition_index = min_rule.find("is uppercase")

        set1 = min_rule[0: condition_index].strip()

        if verbose: print("set1 -" + set1 + "-")

        min_rule_node = Node("is_uppercase", "condition", [set1])

#########################  Condition Aliases  #########################

    elif "every " in min_rule and " contains " in min_rule and " case sensitive" in min_rule:  # case_subset alias

        if verbose: print("Building case_subset node by aliasing")

        condition_index = min_rule.find("contains")

        set1 = min_rule[len("every "): condition_index].strip()

        set2 = min_rule[condition_index + len("contains"): len(min_rule) + 1 - len("case sensitive")].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + set2 + "-")

        min_rule_node = Node("case_subset", "condition", [set1, set2])

    elif "every " in min_rule and " contains " in min_rule:  # subset alias

        if verbose: print("Building subset node by aliasing")

        condition_index = min_rule.find("contains")

        set1 = min_rule[len("every "): condition_index].strip()

        set2 = min_rule[condition_index + len("contains"): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + set2 + "-")

        min_rule_node = Node("subset", "condition", [set1, set2])

#########################  Operations  #########################

    elif "every " in min_rule and min_rule[6].isdigit(): # every_nth

        n = int(find_next_number(min_rule[len("every ")].strip()))

        condition_index = min_rule.find("every ")

        set1 = min_rule[condition_index + len("every ") + len(str(n)): len(min_rule) + 1].strip()

        if verbose: print("n -" + str(n) + "-")

        if verbose: print("set1 -" + set1 + "-")

        min_rule_node = Node("every_nth", "operation", [n, set1])

    elif min_rule.strip()[0].isdigit() and not "-" in min_rule and not "+" in min_rule and not "mod" in min_rule: # nth - avoid evaluating minus plus or mod

        n = find_next_number(min_rule)

        set1 = min_rule.strip()[min_rule.strip().find(" "): len(min_rule) + 1].strip()

        if verbose: print("n -" + n + "-")

        if verbose: print("set1 -" + set1 + "-")

        min_rule_node = Node("nth", "operation", [n, set1])

    # checks for letter of because initial parsing changes letters -> letter
    elif "letter of " in min_rule: # letters_of

        condition_index = min_rule.find("letter of")

        set1 = min_rule[condition_index + len("letter of"): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        min_rule_node = Node("letters_of", "operation", [set1])

    elif "length of " in min_rule: # length

        condition_index = min_rule.find("length of")

        set1 = min_rule[condition_index + len("length of"): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        min_rule_node = Node("length", "operation", [set1])

    elif "sum of " in min_rule: # sum

        condition_index = min_rule.find("sum of")

        set1 = min_rule[condition_index + len("sum of"): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        min_rule_node = Node("sum", "operation", [set1])

    elif "number of " in min_rule and " matching " in min_rule: # number_of

        condition_index = min_rule.find("matching")

        set1 = min_rule[len("number of "): condition_index].strip()

        condition = min_rule[condition_index + len("matching"): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + condition + "-")

        min_rule_node = Node("number_of", "operation", [set1, condition])

    elif "case sensitive location of " in min_rule and " in " in min_rule: # location_of

        condition_index = min_rule.find("in")

        set1 = min_rule[len("case sensitive location of "): condition_index].strip()

        set2 = min_rule[condition_index + len("in"): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + set2 + "-")

        min_rule_node = Node("case_location_of", "operation", [set1, set2])

    elif "location of " in min_rule and " in " in min_rule: # location_of

        condition_index = min_rule.find("in")

        set1 = min_rule[len("location of "): condition_index].strip()

        set2 = min_rule[condition_index + len("in"): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + set2 + "-")

        min_rule_node = Node("location_of", "operation", [set1, set2])

    elif " intersect " in min_rule:  # intersect_set

        condition_index = min_rule.find("intersect")

        set1 = min_rule[0: condition_index].strip()

        set2 = min_rule[condition_index + len("intersect"): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + set2 + "-")

        min_rule_node = Node("intersect_set", "operation", [set1, set2])

    elif " union " in min_rule:  # union_set

        condition_index = min_rule.find("union")

        set1 = min_rule[0: condition_index].strip()

        set2 = min_rule[condition_index + len("union"): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + set2 + "-")

        min_rule_node = Node("union_set", "operation", [set1, set2])

    elif " - " in min_rule:  # minus

        condition_index = min_rule.find("-")

        set1 = min_rule[0: condition_index].strip()

        set2 = min_rule[condition_index + len("-"): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + set2 + "-")

        min_rule_node = Node("minus", "operation", [set1, set2])


    elif " + " in min_rule:  # plus

        condition_index = min_rule.find("+")

        set1 = min_rule[0: condition_index].strip()

        set2 = min_rule[condition_index + len("+"): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + set2 + "-")

        min_rule_node = Node("plus", "operation", [set1, set2])


    elif " mod " in min_rule:  # mod

        condition_index = min_rule.find("mod")

        set1 = min_rule[0: condition_index].strip()

        set2 = min_rule[condition_index + len("mod"): len(min_rule) + 1].strip()

        if verbose: print("set1 -" + set1 + "-")

        if verbose: print("set2 -" + set2 + "-")

        min_rule_node = Node("mod", "operation", [set1, set2])

    elif "lowercase of " in min_rule:  # lowercase

        set1 = min_rule[len("lowercase of "):].strip()

        if verbose: print("set1 -" + set1 + "-")

        min_rule_node = Node("lowercase", "operation", [set1])

    elif "uppercase of " in min_rule:  # lowercase

        set1 = min_rule[len("uppercase of "):].strip()

        if verbose: print("set1 -" + set1 + "-")

        min_rule_node = Node("uppercase", "operation", [set1])


#########################  Identity #########################

    elif "%" in min_rule:

        set1 = min_rule.strip()

        min_rule_node = Node("identity", "identity", [set1])

#########################  Failure #########################

    else:
        print("Couldn't parse min_rule:", min_rule)
        raise Exception("Couldn't parse min_rule: " + min_rule)

    subrules.append(min_rule_node)

    return "%r"+str(len(subrules)-1)
