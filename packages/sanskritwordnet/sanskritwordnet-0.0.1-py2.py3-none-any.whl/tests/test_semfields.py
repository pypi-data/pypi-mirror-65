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

    def test_semfield(self):
        """Test the Sanskrit WordNet API (semfields)."""

        LWN = SanskritWordNet()
        assert LWN.semfields(code='611').get()[0]['english'].startswith('Human anatomy')
        assert len(next(LWN.semfields(code='611').lemmas)['lemmas']) > 1
        assert len(next(LWN.semfields(code='611').synsets)['synsets']) > 1
        assert LWN.semfields(english='anatomy').search()[0]['code'] == '581.4'
