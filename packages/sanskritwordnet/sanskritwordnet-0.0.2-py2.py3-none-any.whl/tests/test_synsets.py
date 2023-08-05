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
        """Test the Sanskrit WordNet API (synsets)."""

        LWN = SanskritWordNet()
        assert LWN.synsets(pos='n', offset='04349777').get()[0]['gloss'].startswith(
            'possession of the qualities'
        )
        assert LWN.synsets(pos='n', offset='04349777').lemmas
        assert '!' in LWN.synsets(pos='n', offset='04349777').relations
        assert len(LWN.synsets(pos='p').get()) > 3
        assert LWN.synsets(pos='n', offset='04349777').sentiment['objectivity'] == 0.75
        assert LWN.synsets(gloss='warfare').search()
