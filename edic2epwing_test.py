#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import edic2epwing
import unittest


class TestParseMethods(unittest.TestCase):

    def test_parse_index(self):
        res = edic2epwing.parse_index("|")
        self.assertEqual(res[0], [])
        self.assertEqual(res[1], [])

        res = edic2epwing.parse_index("|a")
        self.assertEqual(res[0], [])
        self.assertEqual(res[1], ["a"])

        res = edic2epwing.parse_index("|あ")
        self.assertEqual(res[0], [])
        self.assertEqual(res[1], ["あ"])

        res = edic2epwing.parse_index("a|")
        self.assertEqual(res[0], ["a"])
        self.assertEqual(res[1], [])

        res = edic2epwing.parse_index("あ|")
        self.assertEqual(res[0], ["あ"])
        self.assertEqual(res[1], [])

        res = edic2epwing.parse_index("a|あ")
        self.assertEqual(res[0], ["a"])
        self.assertEqual(res[1], ["あ"])

        res = edic2epwing.parse_index(" a | あ ")
        self.assertEqual(res[0], ["a"])
        self.assertEqual(res[1], ["あ"])

    def test_parse_en_index(self):
        res = list(edic2epwing.parse_en_phrase("a,b"))
        self.assertEqual(res[0], "a,b")
        self.assertEqual(res[1], "a")
        self.assertEqual(res[2], "b")

        res = list(edic2epwing.parse_en_phrase("a , b"))
        self.assertEqual(res[0], "a , b")
        self.assertEqual(res[1], "a")
        self.assertEqual(res[2], "b")

    def test__expand_en_optional_phrase(self):
        res = list(edic2epwing.expand_en_optional_phrase("a"))
        self.assertEqual(res[0], "a")

        res = list(edic2epwing.expand_en_optional_phrase("a(b)"))
        self.assertEqual(res[0], "a")
        self.assertEqual(res[1], "ab")

        res = list(edic2epwing.expand_en_optional_phrase("a (b)"))
        self.assertEqual(res[0], "a")
        self.assertEqual(res[1], "a b")

        res = list(edic2epwing.expand_en_optional_phrase("a(b)[c]"))
        self.assertEqual(res[0], "a")
        self.assertEqual(res[1], "ab")
        self.assertEqual(res[2], "ac")
        self.assertEqual(res[3], "abc")

        res = list(edic2epwing.expand_en_optional_phrase("a (b) [c]"))
        self.assertEqual(res[0], "a")
        self.assertEqual(res[1], "a b")
        self.assertEqual(res[2], "a c")
        self.assertEqual(res[3], "a b c")

    def test_parse_ja_index(self):
        res = list(edic2epwing.parse_ja_phrase("あ"))
        self.assertEqual(res[0], "あ")

        res = list(edic2epwing.parse_ja_phrase("あ［い］"))
        self.assertEqual(res[0], "あ［い］")
        self.assertEqual(res[1], "あ")
        self.assertEqual(res[2], "い")

        res = list(edic2epwing.parse_ja_phrase("あ［い｜う］"))
        self.assertEqual(res[0], "あ［い｜う］")
        self.assertEqual(res[1], "あ")
        self.assertEqual(res[2], "い")
        self.assertEqual(res[3], "う")

    def test__expand_ja_optional_phrase(self):
        res = list(edic2epwing.expand_ja_optional_phrase("あ"))
        self.assertEqual(res[0], "あ")

        res = list(edic2epwing.expand_ja_optional_phrase("あ（い）"))
        self.assertEqual(res[0], "あ")
        self.assertEqual(res[1], "あい")

        res = list(edic2epwing.expand_ja_optional_phrase("あ （い）"))
        self.assertEqual(res[0], "あ")
        self.assertEqual(res[1], "あ い")

        res = list(edic2epwing.expand_ja_optional_phrase("あ（い）［う］"))
        self.assertEqual(res[0], "あ")
        self.assertEqual(res[1], "あい")
        self.assertEqual(res[2], "あう")
        self.assertEqual(res[3], "あいう")

        res = list(edic2epwing.expand_ja_optional_phrase("あ （い） ［う］"))
        self.assertEqual(res[0], "あ")
        self.assertEqual(res[1], "あ い")
        self.assertEqual(res[2], "あ う")
        self.assertEqual(res[3], "あ い う")

    def test_parse_ja_alternative(self):
        res = list(edic2epwing.parse_ja_alternative("あ｜い"))
        self.assertEqual(res[0], "あ")
        self.assertEqual(res[1], "い")

        res = list(edic2epwing.parse_ja_alternative(" あ ｜ い "))
        self.assertEqual(res[0], "あ")
        self.assertEqual(res[1], "い")


if __name__ == "__main__":
    unittest.main()
