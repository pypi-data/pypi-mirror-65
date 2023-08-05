#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sanskritwordnet` package."""

import unittest
from sanskritwordnet import SanskritWordNet


class TestIndex(unittest.TestCase):
    """Tests for `sanskritwordnet` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_lemmas(self):
        """Test the Sanskrit WordNet API (sentiment analysis)."""

        # Requires authentication
        # LWN = SanskritWordNet(token='')
        # assert LWN.sentiment_analysis('odiosus es mihi').json() == [
        #     [
        #         [
        #             {
        #                 'lemma': 'odiosus', 'morpho': 'aps---mn1-', 'uri': 'o0512'
        #             },
        #             {
        #                 'lemma': 'sum', 'morpho': 'v1spia--3-', 'uri': 's3436'
        #             }
        #         ],
        #         -0.207
        #     ]
        # ]

