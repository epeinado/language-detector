#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
sys.path.append('../')
from lang_detection_api import Detector

class TestDetector(unittest.TestCase):
    """Language detection test"""

    def setUp(self):
        print "Initializing detector..."
        self.detector = Detector("../models/model.latin")
        print "Detector initialized!"
        self.texts = {"en":"This is an English short text",
                      "es":"Esto es un texto corto en castellano",
                      "it":"Un èrror",
                      "ca":"Això és un text curt en català",
                      "pt":"Este é um pequeno texto em Português",
                      "de":"Dies ist ein kurzer Text in Deutsch"}

    # def testDetectMostProbable(self):
    #     for lang, text in self.texts.items():
    #         detected = self.detector.detect_most_probable(text.decode('utf-8'))
    #         self.assertEqual(lang, detected)

    def testDetectWithThreshold(self):
        for lang, text in self.texts.items():
            detected = self.detector.detect_with_threshold(text.decode('utf-8'), 0.718)
            self.assertEqual(lang, detected)
        print "Hola"
        for lang, text in self.texts.items():
            detected = self.detector.detect_with_threshold(text.decode('utf-8'), 0.718)
            self.assertEqual(lang, detected)

    # def testDetect(self):
    #     for lang, text in self.texts.items():
    #         probs = self.detector.detect(text.decode('utf-8'))
    #         detected = max(probs, key=probs.get)
    #         self.assertEqual(lang, detected)

if __name__ == '__main__':
    import sys, codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    unittest.main()

