from __future__ import unicode_literals

import os
import tempfile
import unittest
import mock

import frododocs
from frododocs.theme import Theme

abs_path = os.path.abspath(os.path.dirname(__file__))
frododocs_dir = os.path.abspath(os.path.dirname(frododocs.__file__))
frododocs_templates_dir = os.path.join(frododocs_dir, 'templates')
theme_dir = os.path.abspath(os.path.join(frododocs_dir, 'themes'))


def get_vars(theme):
    """ Return dict of theme vars. """
    return dict([(k, theme[k]) for k in iter(theme)])


class ThemeTests(unittest.TestCase):

    def test_simple_theme(self):
        theme = Theme(name='frododocs')
        self.assertEqual(
            theme.dirs,
            [os.path.join(theme_dir, 'frododocs'), frododocs_templates_dir]
        )
        self.assertEqual(theme.static_templates, set(['404.html', 'sitemap.xml']))
        self.assertEqual(get_vars(theme), {
            'include_search_page': False,
            'search_index_only': False,
            'highlightjs': True,
            'hljs_style': 'github',
            'hljs_languages': [],
            'shortcuts': {'help': 191, 'next': 78, 'previous': 80, 'search': 83}
        })

    def test_custom_dir(self):
        custom = tempfile.mkdtemp()
        theme = Theme(name='frododocs', custom_dir=custom)
        self.assertEqual(
            theme.dirs,
            [
                custom,
                os.path.join(theme_dir, 'frododocs'),
                frododocs_templates_dir
            ]
        )

    def test_custom_dir_only(self):
        custom = tempfile.mkdtemp()
        theme = Theme(name=None, custom_dir=custom)
        self.assertEqual(
            theme.dirs,
            [custom, frododocs_templates_dir]
        )

    def static_templates(self):
        theme = Theme(name='frododocs', static_templates='foo.html')
        self.assertEqual(
            theme.static_templates,
            set(['404.html', 'sitemap.xml', 'foo.html'])
        )

    def test_vars(self):
        theme = Theme(name='frododocs', foo='bar', baz=True)
        self.assertEqual(theme['foo'], 'bar')
        self.assertEqual(theme['baz'], True)
        self.assertTrue('new' not in theme)
        self.assertRaises(KeyError, lambda t, k: t[k], theme, 'new')
        theme['new'] = 42
        self.assertTrue('new' in theme)
        self.assertEqual(theme['new'], 42)

    @mock.patch('frododocs.utils.yaml_load', return_value=None)
    def test_no_theme_config(self, m):
        theme = Theme(name='frododocs')
        self.assertEqual(m.call_count, 1)
        self.assertEqual(theme.static_templates, set(['sitemap.xml']))

    def test_inherited_theme(self):
        m = mock.Mock(side_effect=[
            {'extends': 'readthedocs', 'static_templates': ['child.html']},
            {'static_templates': ['parent.html']}
        ])
        with mock.patch('frododocs.utils.yaml_load', m) as m:
            theme = Theme(name='frododocs')
            self.assertEqual(m.call_count, 2)
            self.assertEqual(
                theme.dirs,
                [
                    os.path.join(theme_dir, 'frododocs'),
                    os.path.join(theme_dir, 'readthedocs'),
                    frododocs_templates_dir
                ]
            )
            self.assertEqual(
                theme.static_templates, set(['sitemap.xml', 'child.html', 'parent.html'])
            )
