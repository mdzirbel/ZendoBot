
from Rule.set import given_sets
from reference import *

"""
parameters = copy.deepcopy(self.parameters)

        # Switch out <Level> with its corresponding <Set>
        for i in range(len(parameters)):

            if parameters[i] == "sentence":
                if verbose: print("Switching 'sentence' for", sentence)
                parameters[i] = sentence
            elif parameters[i] == "word":
                if verbose: print("Switching 'word' for", words)
                parameters[i] = words
            elif parameters[i] == "letter":
                if verbose: print("Switching 'letter' for", letters)
                parameters[i] = letters

            # Weird pointer stuff here. If we point to the position in number_of_storage, then it will change when number_of_storage changes
            # Only things inside the number_of node have %c#, so we change them to point to the relevant location
            if isinstance(parameters[i], str) and parameters[i][:2] == "%c":
                parameters[i] = number_of_storage[int(parameters[i][2:])]

        # Recursively evaluate parameters
        if self.key != "number_of":
            for i in range(len(parameters)):
                if isinstance(parameters[i], Node):
                    parameters[i] = parameters[i].evaluate(sentence, words, letters, locations, verbose)

"""



class Node:

    def __init__(self, key, node_type, parameters: list):

        self.key = key.strip()
        self.node_type = node_type.strip() # Primitive or Node
        # Parameters can be primitives or nodes
        self.parameters = parameters

    def __str__(self):

        printable_parameters = []
        for param in self.parameters:
            if type(param) is list:
                printable_parameters.append(param[:30])
            else:
                printable_parameters.append(param)

        return "<Node '" + self.key + "' " + str(printable_parameters) + ">"

    def __repr__(self):

        printable_parameters = []
        for param in self.parameters:
            if type(param) is list:
                printable_parameters.append(param[:30])
            else:
                printable_parameters.append(param)

        return "<Node '" + self.key + "' " + str(printable_parameters) + ">"

    def build(self, strings, rules, verbose=False):

        if verbose: print("building \"" + self.key + "\" node, node_type = \"" + self.node_type + "\", parameters =", self.parameters)

        for i, parameter in enumerate(self.parameters):

            if parameter is None: # Should only be the case for number_of when not using location
                pass

            elif type(parameter) is int or parameter.isdigit(): # Number
                self.parameters[i] = int(parameter)

            elif parameter.title() in given_sets.keys(): # Given Set
                self.parameters[i] = given_sets[parameter.title()]

            elif "%s" in parameter: # Set
                index = int(parameter[2:])
                if verbose: print("taking string index",index)
                self.parameters[i] = strings[index]

            elif "%r" in parameter: # Rule
                index = int(parameter[2:])
                if verbose: print("taking rule index",index)
                self.parameters[i] = rules[index]
                self.parameters[i].build(strings, rules, verbose)

            elif parameter in ["sentence", "word", "letter"]: # Level
                pass # Evaluated at runtime

            elif parameter in locations: # Location
                pass # Don't need to do any processing, may decide to later

            elif "%c" in parameter:
                pass

            else:
                print("Couldn't build parameter \"" + self.parameters[i] + "\" into a rule")
                raise Exception("Couldn't build parameter \"" + self.parameters[i] + "\" into a rule")

    def print(self, level=0):

        print("\t"*level + "\"" + self.key + "\" Node. Parameters:")

        for parameter in self.parameters:

            if isinstance(parameter, Node):
                parameter.print(level+1)

            elif type(parameter) is int or parameter is None:
                print("\t"*(level+1) + str(parameter))

            else:
                print("\t"*(level+1) + str(parameter[:30]))

    def evaluate_top_level(self, sentence, verbose=True):
        words = split_to_words(sentence)
        letters = split_to_letters(sentence)
        result = self.evaluate([sentence], words, letters, {}, verbose=verbose)
        return result

    def evaluate(self, sentence, words, letters, number_of_storage, verbose=True):

        parameters = []

        # Switch out <Level> with its corresponding <Set>
        for i, param in enumerate(self.parameters):

            if self.parameters[i] == "sentence":
                if verbose: print("Switching 'sentence' for", sentence)
                parameters.append(sentence)
            elif self.parameters[i] == "word":
                if verbose: print("Switching 'word' for", words)
                parameters.append(words)
            elif self.parameters[i] == "letter":
                if verbose: print("Switching 'letter' for", letters)
                parameters.append(letters)

            # Weird pointer stuff here. If we point to the position in number_of_storage, then it will change when number_of_storage changes
            # Only things inside the number_of node have %c#, so we change them to point to the relevant location
            elif isinstance(self.parameters[i], str) and self.parameters[i][:2] == "%c":
                parameters.append(number_of_storage[int(self.parameters[i][2:])])

            # Recursively evaluate parameter
            # Evaluate all parameters except the fourth parameter of a number_of node
            elif (not (self.key == "number_of" and i==4)) and isinstance(self.parameters[i], Node):
                parameters.append(self.parameters[i].evaluate(sentence, words, letters, number_of_storage, verbose))

            else: # int, location, number_of parameter, list
                parameters.append(self.parameters[i])
                if verbose: print("appending by default", self.parameters[i])

        # Print what we are doing if verbose
        if verbose:
            printable_parameters = []
            for param in parameters:
                if type(param) is list:
                    printable_parameters.append(param[:30])
                else:
                    printable_parameters.append(param)

            print("Evaluating",self.node_type,"type",self.key,"with parameters:",printable_parameters)

        if self.node_type == "condition":

            if self.key == "true":
                return True

            elif self.key == "false":
                return False

            elif self.key == "palindrome":

                if isinstance(parameters[0], str):
                    strings_to_check = [parameters[0].replace(" ", "")]

                elif isinstance(parameters[0], list):
                    strings_to_check = [i.replace(" ", "") for i in parameters[0]]

                else:
                    raise Exception("Palindrome checks can only be done on <Sets>, found " + str(parameters[0]))

                if verbose: print("Strings to check for palindrome:",strings_to_check)

                for s in strings_to_check:
                    if s != s[::-1]:
                        return False

                return True

            elif self.key == "equal":

                if isinstance(parameters[0], int): # Numbers
                    return parameters[0] == parameters[1]

                else: # Sets
                    return parameters[0] == parameters[1]

            elif self.key == "greater_equal":

                return parameters[0] >= parameters[1]

            elif self.key == "less_equal":

                return parameters[0] <= parameters[1]

            elif self.key == "greater":

                return parameters[0] > parameters[1]

            elif self.key == "less":

                return parameters[0] < parameters[1]

            elif self.key == "and":

                return parameters[0] and parameters[1]

            elif self.key == "or":

                return parameters[0] or parameters[1]

            elif self.key == "not":

                return not parameters[0]

            elif self.key == "case_contains":

                for element in parameters[0]:
                    if element in parameters[1]:
                        return True

                return False

            elif self.key == "contains":

                lowercase_param_0 = [element.lower() for element in parameters[0]]
                lowercase_param_1 = [element.lower() for element in parameters[1]]

                for element in lowercase_param_0:
                    if element in lowercase_param_1:
                        return True

                return False

            elif self.key == "case_subset":

                for element in parameters[0]:
                    if not element in parameters[1]:
                        return False

                return True

            elif self.key == "subset":

                for element in (element.lower() for element in parameters[0]):
                    if not element in (set_element.lower() for set_element in parameters[1]):
                        return False

                return True

            elif self.key == "is_lowercase":

                lower = [element.lower() for element in parameters[0]]

                return parameters[0] == lower

            elif self.key == "is_uppercase":

                upper = [element.upper() for element in parameters[0]]

                return parameters[0] == upper

            else:
                print("No condition:",self.key)
                raise Exception

        elif self.node_type == "operation":

            if self.key == "every_nth":

                n = parameters[0]

                return parameters[1][n-1::n]

            elif self.key == "nth":

                if len(parameters[1]) >= parameters[0]:
                    return [parameters[1][parameters[0]-1]] # The -1 is so that 2nd returns index 1
                else:
                    return [""]

            elif self.key == "letters_of":

                letters = []

                for i, word in enumerate(parameters[0]):
                    for j, letter in enumerate(word):
                        letters.append(letter)

                return letters

            elif self.key == "length":

                return len(parameters[0])

            elif self.key == "sum":

                values = {chr(i): i - 96 for i in range(ord("a"), ord("a") + 26)}

                current_sum = 0

                for c in parameters[0]:

                    # List of strings
                    if len(c) > 1:
                        for c2 in c:

                            if c2.isdigit():
                                current_sum += int(c2)

                            else:
                                current_sum += values[c2.lower()]

                    else:
                        if c.isdigit():
                            current_sum += int(c)

                        else:
                            current_sum += values[c.lower()]

                return current_sum

            elif self.key == "number_of":

                # parameters[0] = set to look through
                # parameters[1] = index to hold current at
                # parameters[2] = what the relation is, or None
                # parameters[3] = index to hold relation at, or None
                # parameters[4] = inner rule, to iterate over

                num_matches = 0

                for i, element in enumerate(parameters[0]):

                    number_of_storage[parameters[1]] = element

                    if parameters[2] is None:
                        if parameters[4].evaluate(sentence, words, letters, number_of_storage, verbose):
                            num_matches += 1

                    elif parameters[2] == "next":
                        if i != len(parameters[0])-1:
                            number_of_storage[parameters[3]] = parameters[0][i+1]
                            if parameters[4].evaluate(sentence, words, letters, number_of_storage, verbose):
                                num_matches += 1

                    elif parameters[2] == "previous":
                        if i != 0:
                            number_of_storage[parameters[3]] = parameters[0][i-1]
                            if parameters[4].evaluate(sentence, words, letters, number_of_storage, verbose):
                                num_matches += 1

                    elif parameters[2] == "last":
                        number_of_storage[parameters[3]] = parameters[0][parameters[0]]
                        if parameters[4].evaluate(sentence, words, letters, number_of_storage, verbose):
                            num_matches += 1

                    elif parameters[2] == "first":
                        number_of_storage[parameters[3]] = parameters[0][0]
                        if parameters[4].evaluate(sentence, words, letters, number_of_storage, verbose):
                            num_matches += 1

                    elif parameters[2] == "opposite":
                        number_of_storage[parameters[3]] = parameters[0][len(parameters[0]) - 1 - i]
                        if parameters[4].evaluate(sentence, words, letters, number_of_storage, verbose):
                            num_matches += 1

                return num_matches

            elif self.key == "case_location_of":

                set1 = parameters[0]
                set2 = parameters[1]

                for i in range(len(set2)):

                    for element in set1:

                        if set2[i] == element:
                            return i+1

                return -1

            elif self.key == "location_of":

                set1 = parameters[0]
                set2 = parameters[1]

                for i in range(len(set2)):

                    for element in set1:

                        if set2[i].upper() == element.upper():
                            return i+1

                return -1

            elif self.key == "intersect_set":

                return [value for value in parameters[0] if value in parameters[1]]

            elif self.key == "union_set":

                return parameters[0] + parameters[1]

            elif self.key == "minus":

                if isinstance(parameters[0], list):
                    minus_set = []

                    for element in parameters[0]:
                        if not element in parameters[1]:
                            minus_set.append(element)

                    return minus_set

                else:
                    return parameters[0] - parameters[1]

            elif self.key == "plus":

                return parameters[0] + parameters[1]

            elif self.key == "mod":

                return parameters[0] % parameters[1]

            elif self.key == "lowercase":

                return [value.lower() for value in parameters[0]]

            elif self.key == "uppercase":

                return [value.upper() for value in parameters[0]]

            else:
                print(self.key,"is not a valid operator key")
                raise Exception

        elif self.node_type == "identity":
            return parameters[0]

        else:
            raise Exception("Nodes must be operators or conditions. Found " + self.node_type)