import textwrap
import unittest

from context import filterchain
from freezegun import freeze_time

class TestFilters(unittest.TestCase):

    def test_decaying_dedup_filter_bad_regex(self):
        config = {
            'ttl_seconds': '5',
            'match': '^(badregex'
        }

        with self.assertRaises(filterchain.exceptions.ConfigurationError):
            decaying_dedup_filter = filterchain.processors.filters.DecayingDedupFilter(config)

    def test_decaying_dedup_filter(self):
        config = {
            'ttl_seconds': '5',
            'match': '^(dupe)'
        }

        decaying_dedup_filter = filterchain.processors.filters.DecayingDedupFilter(config)

        s = textwrap.dedent('''
        dupe one
        dupe two
        dupe three
        ''')


        with freeze_time('2017-04-27 00:00:00'):
            for line in s.split():
                decaying_dedup_filter.run(line)

        with freeze_time('2017-04-27 00:00:03'):
            self.assertIsNone(
                decaying_dedup_filter.run('dupe another one'),
                'Adding a matching line within TTL should noop.'
            )

        with freeze_time('2017-04-27 00:00:30'):
            self.assertEquals(
                decaying_dedup_filter.run('dupe another one another'),
                'dupe another one another',
                'Adding a matching line after TTL should pass...'
            )

        with freeze_time('2017-04-27 00:00:31'):
            self.assertIsNone(
                decaying_dedup_filter.run('dupe another one another one'),
                '... and should not pass after it is added again.'
            )


    def test_redact_filter(self):
        config = {
            'match': '(replace_me)',
            'redaction_char': '@'
        }

        redact_filter = filterchain.processors.filters.RedactFilter(config)

        self.assertEquals(
            redact_filter.run('Hello replace_me'),
            'Hello @@@@@@@@@@'
        )


    def test_remove_filter(self):
        config = {
            'ttl_seconds': '5',
            'match': '^(remove_me)'
        }

        remove_filter = filterchain.processors.filters.RemoveFilter(config)

        self.assertIsNone(
            remove_filter.run('remove_me I should not be seen'),
            'Matching lines should be removed.'
        )

        self.assertEquals(
            remove_filter.run('I should be seen'),
            'I should be seen',
            'Non-matching lines should pass.'
        )


    def test_top_n_filter(self):
        config = {
            'top_n': '3'
        }

        s = textwrap.dedent('''
        one
        one
        two
        two
        two
        three
        three
        three
        ''')

        top_n_filter = filterchain.processors.filters.TopNFilter(config)

        for line in s.split():
            top_n_filter.run(line)

        self.assertIsNone(
            top_n_filter.run('one'),
            'Lines already in the top 3 should not be returned.'
        )

        self.assertEqual(
            top_n_filter.run('foo'),
            'foo',
            'Lines not in the top 3 should be returned.'
        )

        self.assertEqual(
            top_n_filter.run('foo'),
            'foo',
            'Line not yet in the top 3 should be returned.'
        )

        top_n_filter.run('foo')

        self.assertIsNone(
            top_n_filter.run('foo'),
            'Line now in the top 3 should not be returned.'
        )
