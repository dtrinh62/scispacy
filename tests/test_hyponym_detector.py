# pylint: disable=no-self-use,invalid-name
import unittest
import spacy

from scispacy.hyponym_detector import HyponymDetector


class TestHyponymDetector(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.nlp = spacy.load("en_core_sci_sm")
        self.detector = HyponymDetector(self.nlp, extended=True)
        self.nlp.add_pipe(self.detector, last=True)

    def test_pipe_sentence(self):
        text = ("Recognizing that the preferred habitats for the species "
                "are in the valleys, systematic planting of keystone plant "
                "species such as fig trees (Ficus) creates the best microhabitats.")
        doc = self.nlp(text)
        fig_trees = doc[21:23]
        keystone_plant_species = doc[16:19]
        assert doc._.hearst_patterns == [('such_as', keystone_plant_species, fig_trees)]

    def test_find_noun_compound_head(self):

        doc = self.nlp("The potassium channel is good.")

        head = self.detector.find_noun_compound_head(doc[1])
        assert head == doc[2]

        doc = self.nlp("Planting of large plants.")
        head = self.detector.find_noun_compound_head(doc[3])
        # Planting is a noun, but not a compound with 'plants'.
        assert head != doc[0]
        assert head == doc[3]

    def test_expand_noun_phrase(self):
        doc = self.nlp("Keystone plant habitats are good.")
        chunk = self.detector.expand_to_noun_compound(doc[1], doc)
        assert chunk == doc[0:3]
