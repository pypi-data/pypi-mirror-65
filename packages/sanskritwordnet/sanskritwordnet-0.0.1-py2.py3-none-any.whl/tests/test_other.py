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

    def test_other(self):
        """Test the Sanskrit WordNet API (other)."""

        LWN = SanskritWordNet()
        print(next(LWN.lemmatize('virtutem')))['lemma']['lemma']
        assert next(LWN.lemmatize('virtutem'))['lemma']['lemma'] == 'uirtus'
        assert next(LWN.lemmatize('dicas', 'n'))['lemma']['morpho'] == 'n-s---fn1-'
        assert next(LWN.lemmatize('dicas', 'v1spia--3-'))['lemma']['uri'] == 'd1350'

        assert next(LWN.translate('en', 'offspring'))
        assert next(LWN.translate('en', 'love', 'v'))
