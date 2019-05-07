## Text-Based Implementation of Zendo, for Discord Servers

Zendo is a game where one person thinks of a rule for a group of pyramids. Then, everyone else builds groups of pyramids and tries to guess the rule based off whether their pyramids fit the rule or not.

In Text-Zendo, the basic idea is the same. One person writes a rule in my custom Context Free Grammar, and the Discord bot automates the task of checking guesses against the rule.

Here's an example rule: Every word in the guess has to be in the dictionary.

The person making the rule might enter `word is subset of dictionary` to create the rule.

Then people might guess `hello`, `asdfghjkl`, or `a b c d`, and the bot responds with whether they fit the rule, in this case only the first guess fit