
import unittest, time
from Rule.rule import build_rule

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self._started_at = time.time()

    def tearDown(self):
        elapsed = time.time() - self._started_at
        if elapsed >= .02:
            print('{} ({}s)'.format(self.id(), round(elapsed, 4)))

    def test_true_t(self):
        rule = build_rule("true", verbose=False)
        self.assertEqual(rule.evaluate_top_level("katie", verbose=False), True)

    def test_false_f(self):
        rule = build_rule("false", verbose=False)
        self.assertEqual(rule.evaluate_top_level("katie", verbose=False), False)

    def test_palindrome_t(self):
        rule = build_rule("word is palindrome", verbose=False)
        self.assertEqual(rule.evaluate_top_level("hellolleh", verbose=False), True)

    def test_palindrome_f(self):
        rule = build_rule("word is palindrome", verbose=False)
        self.assertEqual(rule.evaluate_top_level("hellolh", verbose=False), False)

    def test_equal_t(self):
        rule = build_rule("3 == 3", verbose=False)
        self.assertEqual(rule.evaluate_top_level("", verbose=False), True)

    def test_equal_f(self):
        rule = build_rule("3 == 4", verbose=False)
        self.assertEqual(rule.evaluate_top_level("", verbose=False), False)

    def test_greater_equal_t(self):
        rule = build_rule("3 >= 2", verbose=False)
        self.assertEqual(rule.evaluate_top_level("", verbose=False), True)

    def test_greater_equal_f(self):
        rule = build_rule("3 >= 4", verbose=False)
        self.assertEqual(rule.evaluate_top_level("", verbose=False), False)

    def test_less_equal_t(self):
        rule = build_rule("3 <= 4", verbose=False)
        self.assertEqual(rule.evaluate_top_level("", verbose=False), True)

    def test_less_equal_f(self):
        rule = build_rule("3 <= 2", verbose=False)
        self.assertEqual(rule.evaluate_top_level("", verbose=False), False)

    def test_greater_t(self):
        rule = build_rule("3 > 2", verbose=False)
        self.assertEqual(rule.evaluate_top_level("", verbose=False), True)

    def test_greater_f(self):
        rule = build_rule("3 > 3", verbose=False)
        self.assertEqual(rule.evaluate_top_level("", verbose=False), False)

    def test_less_t(self):
        rule = build_rule("1 < 2", verbose=False)
        self.assertEqual(rule.evaluate_top_level("", verbose=False), True)

    def test_less_f(self):
        rule = build_rule("3 < 2", verbose=False)
        self.assertEqual(rule.evaluate_top_level("", verbose=False), False)

    def test_and_t(self):
        rule = build_rule("(true) and (true)", verbose=False)
        self.assertEqual(rule.evaluate_top_level("", verbose=False), True)

    def test_and_f(self):
        rule = build_rule("(true) and (false)", verbose=False)
        self.assertEqual(rule.evaluate_top_level("", verbose=False), False)

    def test_or_t(self):
        rule = build_rule("(true) or (false)", verbose=False)
        self.assertEqual(rule.evaluate_top_level("", verbose=False), True)

    def test_or_f(self):
        rule = build_rule("(false) or (false)", verbose=False)
        self.assertEqual(rule.evaluate_top_level("", verbose=False), False)

    def test_not_t(self):
        rule = build_rule("not (false)", verbose=False)
        self.assertEqual(rule.evaluate_top_level("", verbose=False), True)

    def test_not_f(self):
        rule = build_rule("not (true)", verbose=False)
        self.assertEqual(rule.evaluate_top_level("", verbose=False), False)

    def test_case_contains_t(self):
        rule = build_rule("adjectives contains word case sensitive", verbose=False)
        self.assertEqual(rule.evaluate_top_level("nice", verbose=False), True)

    def test_case_contains_f(self):
        rule = build_rule("adjectives contains word case sensitive", verbose=False)
        self.assertEqual(rule.evaluate_top_level("nIcE", verbose=False), False)

    def test_contains_t(self):
        rule = build_rule("adjectives contains word", verbose=False)
        self.assertEqual(rule.evaluate_top_level("nice the hello", verbose=False), True)

    def test_contains_f(self):
        rule = build_rule("adjectives contains word", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the hello", verbose=False), False)

    def test_case_subset_t(self):
        rule = build_rule("word is case sensitive subset of dictionary", verbose=False)
        self.assertEqual(rule.evaluate_top_level("hello", verbose=False), True)

    def test_case_subset_f(self):
        rule = build_rule("word is case sensitive subset of dictionary", verbose=False)
        self.assertEqual(rule.evaluate_top_level("hElLo", verbose=False), False)

    def test_subset_t(self):
        rule = build_rule("word is subset of dictionary", verbose=False)
        self.assertEqual(rule.evaluate_top_level("hello", verbose=False), True)

    def test_subset_f(self):
        rule = build_rule("word is subset of dictionary", verbose=False)
        self.assertEqual(rule.evaluate_top_level("asdfgh", verbose=False), False)

    def test_is_lowercase_t(self):
        rule = build_rule("sentence is lowercase", verbose=False)
        self.assertEqual(rule.evaluate_top_level("hello", verbose=False), True)

    def test_is_lowercase_f(self):
        rule = build_rule("sentence is lowercase", verbose=False)
        self.assertEqual(rule.evaluate_top_level("asdfgH", verbose=False), False)

    def test_is_uppercase_t(self):
        rule = build_rule("sentence is uppercase", verbose=False)
        self.assertEqual(rule.evaluate_top_level("HELLO", verbose=False), True)

    def test_is_uppercase_f(self):
        rule = build_rule("sentence is uppercase", verbose=False)
        self.assertEqual(rule.evaluate_top_level("HELLo", verbose=False), False)

###################################  Operations  ###################################

    def test_every_nth_t(self):
        rule = build_rule("(every 2nd word) == {'quick', 'fox'}", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the quick brown fox", verbose=False), True)

    def test_every_nth_f(self):
        rule = build_rule("(every 2nd word) == {'the', 'quick', 'brown', 'fox'}", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the quick brown fox", verbose=False), False)

    def test_nth_t(self):
        rule = build_rule("(2nd word) == {'quick'}", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the quick brown fox", verbose=False), True)

    def test_nth_f(self):
        rule = build_rule("(2nd word) == {'the', 'quick', 'brown', 'fox'}", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the quick brown fox", verbose=False), False)

    def test_letters_of_t(self):
        rule = build_rule("(letters of word) == {'t', 'h', 'e'}", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the", verbose=False), True)

    def test_length_t(self):
        rule = build_rule("(length of word) == 4", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the quick brown fox", verbose=False), True)

    def test_length_f(self):
        rule = build_rule("(length of word) == 3", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the quick brown fox", verbose=False), False)

    def test_sum_t(self):
        rule = build_rule("(sum of word) == (sum of {'t', 'he'})", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the", verbose=False), True)

    def test_sum_f(self):
        rule = build_rule("(sum of word) == (sum of {'t', 'h'})", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the", verbose=False), False)

    def test_case_location_of_t(self):
        rule = build_rule("(case sensitive location of {'qUICk', 'fox'} in word) == 4", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the quick brown fox", verbose=False), True)

    def test_case_location_of_f(self):
        rule = build_rule("(case sensitive location of {'quick' 'fox'} in word) == 2", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the", verbose=False), False)

    def test_location_of_t(self):
        rule = build_rule("(location of {'qUICk', 'fox'} in word) == 2", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the quick brown fox", verbose=False), True)

    def test_location_of_f(self):
        rule = build_rule("(location of {'quick' 'fox'} in word) == 2", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the", verbose=False), False)

    def test_intersect_set_t(self):
        rule = build_rule("({'The', 'the'} intersect {'The'}) == {'The'}", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the quick brown fox", verbose=False), True)

    def test_union_set_t(self):
        rule = build_rule("({'The', 'the'} union {'The'}) == {'The', 'the', 'The'}", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the quick brown fox", verbose=False), True)

    def test_minus_set_t(self):
        rule = build_rule("({'The', 'the'} - {'The', 'hi'}) == {'the'}", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the quick brown fox", verbose=False), True)

    def test_minus_number_t(self):
        rule = build_rule("(2 - 1) == 1", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the quick brown fox", verbose=False), True)

    def test_plus_t(self):
        rule = build_rule("(1 + 1) == 2", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the quick brown fox", verbose=False), True)

    def test_mod_t(self):
        rule = build_rule("(3 mod 2) == 1", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the quick brown fox", verbose=False), True)

    def test_number_of_t(self):
        rule = build_rule("(word s1, next l1)[(length of s1) == (length of l1)] == ((length of word) - 2)", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the she lol foxes", verbose=False), True)

    def test_lowercase_t(self):
        rule = build_rule("(lowercase of {'THe', 'quIck'}) == word", verbose=False)
        self.assertEqual(rule.evaluate_top_level("the quick", verbose=False), True)

    def test_uppercase_t(self):
        rule = build_rule("(uppercase of {'THe', 'quIck'}) == word", verbose=False)
        self.assertEqual(rule.evaluate_top_level("THE QUICK", verbose=False), True)

    ################################  Additional Tests  ################################

    def test_1(self):
        rule = build_rule("(sum of (1st word)) <= (sum of (2nd word))", verbose=False)
        self.assertEqual(rule.evaluate_top_level("THE QUICK", verbose=False), True)

    def test_2(self):
        rule = build_rule("(1st word) == ((2nd word))", verbose=False)
        self.assertEqual(rule.evaluate_top_level("THE the", verbose=False), False)

    def test_3(self):
        rule = build_rule("(1 > 2) and (true)", verbose=False)
        self.assertEqual(rule.evaluate_top_level("THE the", verbose=False), False)

    def test_4(self):
        rule = build_rule("word is subset of animals", verbose=False)
        self.assertEqual(rule.evaluate_top_level("dog cat llama", verbose=False), True)

    def test_5(self):
        rule = build_rule("(word s1)[(length of s1) == 4] == (length of word)", verbose=False)
        self.assertEqual(rule.evaluate_top_level("what that", verbose=False), True)

    def test_6(self):
        rule = build_rule("(word s1)[(word s2, opposite l1)[(s2 == l1) and ((sum of s1) == (sum of s2))] == (length of word)] == (length of word)", verbose=False)
        self.assertEqual(rule.evaluate_top_level("abc abc ab", verbose=False), False)

    def test_7(self):
        rule = build_rule("((every 2nd word) s1)[s1 contains vowel] == (length of (every 2nd word))", verbose=False)
        self.assertEqual(rule.evaluate_top_level("b a b a", verbose=False), True)

    def test_8(self):
        rule = build_rule("(word s1)[(word s2, opposite l1)[(s2 == l1) and ((sum of s1) == (sum of s2))] == (length of word)] == (length of word)", verbose=False)
        self.assertEqual(rule.evaluate_top_level("abc abc ab", verbose=False), False)
        self.assertEqual(rule.evaluate_top_level("abc abc abc", verbose=False), True)
        self.assertEqual(rule.evaluate_top_level("abc cba abc", verbose=False), True)
        self.assertEqual(rule.evaluate_top_level("abc abc ab", verbose=False), False)


if __name__ == '__main__':
    unittest.main()

