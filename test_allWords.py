from unittest import TestCase
from my_vocabulary import MyVocabulary, AllWords


class TestMyVocabulary(TestCase):

    def test_add_word(self):

        my_vocabulary = MyVocabulary(AllWords())

        self.assertEqual(self.my_vocabulary.add_word("stát se čím"),
                         "This word has been already added. "
                         "Try adding another word.")
        self.assertEqual(self.my_vocabulary.add_word("bít"),
                         "The word has been successfully added.")


class TestAllWords(TestCase):

    all_words = AllWords()

    def test_search(self):
        self.assertTrue(self.all_words.search("být"))
        self.assertTrue(self.all_words.search("bít"))
        self.assertTrue(self.all_words.search("stát se čím"))
        self.assertTrue(self.all_words.search("začít"))
        self.assertTrue(self.all_words.search("kousnout"))
        self.assertTrue(self.all_words.search("foukat"))
        self.assertTrue(self.all_words.search("rozbít"))
        self.assertTrue(self.all_words.search("přinést"))
        self.assertTrue(self.all_words.search("postavit"))
        self.assertTrue(self.all_words.search("koupit"))
        self.assertFalse(self.all_words.search(""))
        self.assertFalse(self.all_words.search("d"))
        self.assertFalse(self.all_words.search("býtbýt"))
        self.assertFalse(self.all_words.search("3"))

    def test_value(self):
        self.assertEqual(self.all_words.value("být"), "be")
        self.assertEqual(self.all_words.value("bít"), "beat")
        self.assertEqual(self.all_words.value("stát se čím"), "become")
        self.assertEqual(self.all_words.value("začít"), "begin")
        self.assertEqual(self.all_words.value("kousnout"), "bite")
        self.assertEqual(self.all_words.value("foukat"), "blow")
        self.assertEqual(self.all_words.value("rozbít"), "break")
        self.assertEqual(self.all_words.value("přinést"), "bring")
        self.assertEqual(self.all_words.value("postavit"), "build")
        self.assertEqual(self.all_words.value("koupit"), "buy")
        self.assertNotEqual(self.all_words.value("být"), "být")
        self.assertNotEqual(self.all_words.value("bít"), "be")
        self.assertNotEqual(self.all_words.value("kousnout"), "h")
        self.assertNotEqual(self.all_words.value("rozbít"), "")
        with self.assertRaises(KeyError):
            self.all_words.value("")
        with self.assertRaises(KeyError):
            self.all_words.value("  ")
        with self.assertRaises(KeyError):
             self.all_words.value("bring")
