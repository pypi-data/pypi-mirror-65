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

    def test_index(self):
        """Test the Sanskrit WordNet API (index)."""

        LWN = SanskritWordNet()
        assert next(LWN.index())['lemma'] == 'Aaron'
        assert next(LWN.index(pos='v'))['lemma'] == 'abaestumo'
        assert next(LWN.index(morpho='aps---mn1-'))['lemma'] == 'abacinus'


