#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste

import unittest
from click.testing import CliRunner

from biofaker import biofaker
from biofaker import cli


class TestBiofaker(unittest.TestCase):
    """Tests for `biofaker` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_cli(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        self.assertEqual(0, result.exit_code)
        self.assertIn("biofaker.cli.main",
                      result.output)

    def test_cli_help(self):
        """Test the CLI help."""
        runner = CliRunner()
        result = runner.invoke(cli.main, ["--help"])
        self.assertEqual(0, result.exit_code)
        self.assertIn("--help  Show this message and exit.",
                      result.output)
