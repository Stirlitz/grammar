#!/usr/bin/env python

"""Unit Tests for grammar"""

import grammar
import unittest


class ParserFunctions(unittest.TestCase):
    options = {
        # 'do_decode_html': True,
        'do_quotations': True,  # uses regex
        # 'do_ellipsis': True,
        # 'do_askfm': False, # uses regex
        # 'do_fixcaps': True, # uses regex
        # 'do_fixi': True, # uses regex
        'do_fixnewline': True,  # uses regex
    }

    def setUp(self):
        self.parser = grammar.CorrectionManager()

    def load(self, text, **kwargs):
        self.parser.reset()
        options = self.options
        options.update(kwargs)
        if self.parser.load_text(text, **options):
            return self.parser.corrections[0]
        return False

    def positive(self, text, result=None):
        if result:
            self.assertEqual(self.load(text), result)
        else:
            self.assertTrue(self.load(text))

    def negative(self, text):
        self.assertFalse(self.load(text))

    # Tests
    def test_load_regular(self):
        """Try to properly load a regular sentence."""
        self.negative("This sentence is fine.")

    def test_possessive_as_be(self):
        self.positive("Its here or there", "[It's] here or there")
        self.positive("Your the best", "[You're] the best")
        self.positive("Whose your friend?", "[Who's] your friend?")
        # Exception 1
        self.negative("Some author, whose THE BOOK does, is")
        # Exception 2
        self.negative("Look at its after effects!")
        # Exception 3
        self.negative("See your all but nothing system")

    def test_youre_noun(self):
        self.positive("of you're own!", "of [your] own!")
        # Exception 1
        self.negative("You're day dreamers")
        self.negative("You're day dreaming")
        # Exception 2
        self.negative(
            "You're life savers, you're life wasters, you're life changers!")
        self.negative("you're life changing!")
        # Exception 3
        self.negative("You're life.")
        self.negative("You're life!")
        self.negative("You're life")

    def test_its_own(self):
        self.positive("sees it's own", "sees [its] own")

    def test_there_own(self):
        self.positive("To each there own", "To each [their] own")
        # Exception
        self.negative("Do any people out there own something?")
        self.negative("Does anyone out there own this item?")
        self.negative("Does someone out there own this?")
        self.negative("Does no one out there own that?")
        self.negative("Do any of you out there own these items?")
        # Exception with fused word
        self.negative("anyone out there own it?")

    def test_whose_been(self):
        self.positive("Whose been there?", "[Who's] been there?")
        self.positive("See that person, whose been there.",
                      "person, [who's] been there")

    def test_theyre_be(self):
        self.positive("They're is a cow", "[There's] a cow")
        self.positive("They're is and they're are", "[There's] and [they] are")
        self.positive("they're aren't any of those.", "[they] aren't any of")
        # Exception 1
        self.negative("the difference between their, there, and they're is")
        self.negative("the difference between there, their, and they're is")
        # Exception 2
        self.negative("they're is they are")
        self.negative("they're, aren't they?") # 2b

    def test_their_modal(self):
        self.positive("Their is", "[There] is")
        self.positive("Their must be something!", "[There] must be something!")

    def test_be_noun(self):
        self.positive("I am hear", "I am [here]")
        self.positive("I am board with", "I am [bored] with")
        self.positive("I am hear to win", "I am [here] to win")
        self.positive("They are hear", "They are [here]")
        self.positive("Those people are hear", "people are [here]")
        self.positive("He is hear", "He is [here]")
        # Tolerate misuse of verbs
        self.positive("He are hear", "He are [here]")
        self.positive("They is hear", "They is [here]")
        # Ignore misuse of 'am'
        self.negative("He am hear")
        self.negative("They am hear")

    def test_then(self):
        self.positive("this is better then that", "this is better [than] that")
        self.positive("I have more then you do", "I have more [than] you do")
        # Exception 1
        self.negative("wait until it's better then do it")
        # Exception 2
        self.negative("if it is better then you use it")
        self.negative("when it is better then get it")

    def test_than(self):
        self.positive("I did this and than I did that",
                      "did this and [then] I did that")
        # Exception 1
        self.negative("the difference between then and than")
        # Exception: 2
        self.negative("better than something and than something else")
        self.negative("Is it more than they do or than I do?")

    def test_of(self):
        self.positive("I should of done it", "I should['ve] done it")
        self.positive("I should not of done it", "I should not['ve] done it")
        self.positive("I shouldn't of done it", "I shouldn't['ve] done it")
        self.positive("I should of went there", "I should['ve gone] there")
        # Exception 1
        self.negative("He could of course do")
        # Exception 2
        self.negative("would of themselves justify")
        # Exception 3a
        self.negative("Face the full might of our army!")
        self.negative("the might of some guy")
        self.negative("the full might of them")
        self.negative("no might of him")
        # Exception 3b
        self.negative("might of the people")
        # Exception: 4
        self.negative("more of this than they would of that")

    def test_your_are(self):
        self.positive("your are", "[you] are")

    def test_supposed_to(self):
        self.positive("I don't supposed to", "[I'm not] supposed to")
        self.positive("you don't supposed to", "you [aren't] supposed to")
        self.positive("he doesn't supposed to", "he [isn't] supposed to")
        # Correct mismatched verbs
        self.positive("I doesn't supposed to", "[I'm not] supposed to")
        self.positive("you doesn't supposed to", "you [aren't] supposed to")
        self.positive("he don't supposed to", "he [isn't] supposed to")
        # Ignore modals
        self.negative("I can't supposed to")

    def test_whom_be(self):
        self.positive("he whom is", "he [who] is")
        self.positive("a person whom is", "person [who] is")
        self.positive("a person whom was", "person [who] was")
        self.positive("I whom was", "I [who] was")
        self.positive("people whom are", "people [who] are")
        self.positive("people whom were", "people [who] were")
        self.positive("see whomever is", "see [whoever] is")
        self.positive("Whomever is", "[Whoever] is")
        # "Whoever" is always singular
        self.positive("Whomever am", "[Whoever is]")
        self.positive("Whomever be", "[Whoever is]")
        self.positive("Whomever are", "[Whoever is]")
        # Correct improper verbs
        self.positive("I whom are", "I [who am]")
        self.positive("I whom were", "I [who was]")
        self.positive("a person whom are", "person [who is]")
        self.positive("a person whom were", "person [who was]")
        self.positive("people whom is", "people [who are]")
        self.positive("people whom was", "people [who were]")
        self.positive("You see me, whom is your friend.",
                      "see me, [who am] your friend")
        # A preceding word is required for verb conjugations
        self.negative("Whom is it?")
        # Other verbs might be valid for "whom"
        self.negative("Whom do they see?")

    def test_case(self):
        # lowercase detection
        self.positive("their is", "[there] is")
        # Titlecase Detection
        self.positive("Their is", "[There] is")
        # UPPERCASE DETECTION
        self.positive("THEIR is", "[THERE] is")

    def test_overlap(self):
        self.positive("Their is you're own", "[There] is [your] own")
        self.positive("Your you're own", "[You're your] own")
        self.positive("Its there own item", "[It's their] own item")
        self.positive("Your don't supposed to!", "[You aren't] supposed to!")

    def test_punctuation(self):
        # Keep question marks and exclamation marks
        self.positive("their is?", "[there] is?")
        self.positive("their is!", "[there] is!")
        # Original punctuation should be out of the brackets
        self.positive("I am hear!", "I am [here]!")
        # Retain double spaces
        self.positive("their  is", "[there]  is")
        # Drop periods, commas, and semicolons
        self.positive("their is.", "[there] is")
        self.positive("their is,", "[there] is")
        self.positive("their is;", "[there] is")

    def test_boundary_checks(self):
        """Make sure that the checks do not overread"""
        # possessive_as_be: <its/your/whose> _
        self.negative("It's its") # its_own: _ <it's>
        self.negative("your") # your_are: <your> _
        self.negative("Whose?") # whose_been: <whose> _
        # youre_noun: <you're> _
        self.negative("See you're")
        # there_own: _ <own>
        self.negative("Own this item now")
        # theyre_be: <they're> _
        self.negative("See, they're")
        # their_modal: <their> _
        self.negative("their")
        self.negative("their item")
        # be_noun: _ <hear/board with>
        self.negative("They can hear you")
        self.negative("Hear the silence")
        self.negative("Look at the board")
        self.negative("Board the train")
        self.negative("Board with them")
        # then: _ <comparative> <then> _
        self.negative("Then they went somewhere")
        self.negative("Do it better then")
        # than: _ <and/but/yet> _
        self.negative("And it works")
        self.negative("this and")
        # of: _ (not)? <of> _
        self.negative("of")
        self.negative("not of this but that")
        # supposed_to: _ <supposed> _
        self.negative("They supposed")
        self.negative("They supposed not")
        # whom_be: _ <whom> _
        self.negative("whom they say")
        self.negative("for whom?")

    def test_wording(self):
        """Verify that wording can be generated without failing"""
        self.positive("Their is and your don't supposed to")
        self.parser.generate_wording('@')
        #self.parser.generate_wording_long('@')

if __name__ == '__main__':
    unittest.main()
