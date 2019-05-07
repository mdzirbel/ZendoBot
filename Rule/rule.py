
from Rule.rule_manipulation import *
from Rule.build_min_rule import build_min_rule

"""
Set:
Dictionary
Animals
Nouns
Verbs
Adjectives
Countries
States
Heathrows
Python Reserved Words
Uppercase
Lowercase
Vowel
Consonant

User defined set = {"element_1", "element_2" ...}

Conditions:
true           |  True
false          |  False
palindrome     |  <Set> is palindrome                   |  Whether every element in <Set> is a palindrome
equal          |  <Number> == <Number>  |  <Set> == <Set>
greater_equal  |  <Number> >= <Number>
less_equal     |  <Number> <= <Number>
greater        |  <Number> > <Number>
less           |  <Number> < <Number>
and            |  <Condition> and <Condition>
or             |  <Condition> or <Condition>
not            |  not <Condition>
case_contains  |  <Set1> contains <Set2> case sensitive
contains       |  <Set1> contains <Set2>                 |  Whether any element of <Set2> can be found anywhere in <Set1> eg. {'hello'} contains {'hell'} -> True
case_subset    |  <Set1> is case sensitive subset of <Set2>
subset         |  <Set1> is subset of <Set2>             |  <Set1> is subset of <Set2> eg. ["dog", "cat", "llama"] is subset of animals -> True
is_lowercase   |  <Set> is lowercase                     |  Checks whether everything in <Set> is lowercase. Ignores numbers
is_uppercase   |  <Set> is uppercase                     |  Checks whether everything in <Set> is uppercase. Ignores numbers

Operations:
every_nth      |  <Set>     |  every (n)th <Set>                         |  eg. every 2nd word - ["the", "quick", "brown", "fox"] -> ["quick", "fox"]
nth            |  <Set>     |  (n)th <Set>                               |  <Set>[n]
length         |  <Number>  |  length of <Set>                           |  Length of set. length of sentence -> 1, length of words -> number of words
sum            |  <Number>  |  sum of <Set>                              |  Sum of letters in set, a=A=1, b=B=2, 1=1, 2=2
case_location_of  <Number>  |  case sensitive location of <Set1> in <Set2>
location_of    |  <Number>  |  location of <Set1> in <Set2>              |  Finds the index of the first element of Set1 which it shares with Set2 or -1
intersect_set  |  <Set>     |  <Set1> intersect <Set2>                   |  <Set1> n <Set2> (case sensitive)
union_set      |  <Set>     |  <Set1> union <Set2>                       |  <Set1> U <Set2> (case sensitive)
minus          |  <???>     |  <Set1> - <Set2> or <Number1> - <Number2>  |  <Set1> \ <Set2> or <Number1> - <Number2>
plus           |  <Number>  |  <Number> + <Number>
mod            |  <Number>  |  <Number1> mod <Number2>                   |  <Number1> % <Number2>
number_of      |  <Number>  |  (<Set> s#, <Location> l#)[Condition]      |  Checks condition for any s and related l eg. (word s1, next l1)[(sum of s1) > (sum of l1)]
!lowercase      |  <Set>     |  lowercase of <Set>                        |  Makes <Set> lowercase
!uppercase      |  <Set>     |  uppercase of <Set>                        |  Makes <Set> uppercase

Identity:
identity       |  Rule      |  Same rule, allows for extra parentheses

Number:
...
-1
0
1
2
...

Level: Alias for <Set>
Sentence  |  Set of one element which is the entire guess  |  "The quick brown" -> ["The quick brown"]
Word      |  every word in sentence                        |  "The quick brown" -> ["The", "quick", "brown"]
Letter    |  every letter in sentence                      |  "The quick brown" -> ['T', 'h', 'e', 'q', 'u' ...]
Words     |  Alias for Word, and can be used interchangeably
Letters   |  Alias for Letter, and can be used interchangeably

Location:
Next 
Previous
Last
First
Opposite

During processing:
%r#      |  Rule      |  subrules
%s#      |  Set       |  sets
%c#      |            |  number_of_storage

"""


def build_rule(rule_string: str, verbose=False):

    if verbose: print("Building rule:",rule_string)

    subrules = []
    sets = []

    # Put user sets into their own list, make lowercase, then remove ordinals
    rule_string = format_rule(rule_string, sets)

    if verbose: print("pre:", rule_string, subrules, sets)

    # While rule string is not packed into a pointer to one rule
    while rule_string != ("%r" + str(len(subrules)-1)):

        min_rule, enclosed = find_min_rule(rule_string)  # Get a min rule

        rule_reference = build_min_rule(min_rule, subrules, verbose=verbose)  # Build it into a rule Node

        if enclosed:
            rule_string = rule_string.replace("("+min_rule+")", rule_reference, 1)  # Replace the rule_string segment with a %r# pointer
        else:
            rule_string = rule_string.replace(min_rule, rule_reference, 1)  # Replace the rule_string segment with a %r# pointer

    if verbose: print("post:",rule_string, subrules, sets, "\n")

    root_rule = subrules[int(rule_string[2:])]

    root_rule.build(sets, subrules)

    if verbose:
        print("Built rule.")
        root_rule.print()

    return root_rule


if __name__ == "__main__":

    rule = build_rule("(word s1, next l1)[(length of s1) == (length of l1)] == ((length of word) - 1)", verbose=True)
    # rule = build_rule("word is subset of dictionary", verbose=True)

    print(rule.evaluate_top_level("the she lol FOX"))
    # print(rule.evaluate_top_level("hello"))
