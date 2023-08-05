from __future__ import unicode_literals

import unittest
import mock

from frododocs.tests.base import load_config, LogTestCase
from frododocs.commands import gh_deploy
from frododocs import __version__


class TestGitHubDeploy(unittest.TestCase):

    @mock.patch('subprocess.Popen')
    def test_is_cwd_git_repo(self, mock_popeno):

        mock_popeno().wait.return_value = 0

        self.assertTrue(gh_deploy._is_cwd_git_repo())

    @mock.patch('subprocess.Popen')
    def test_is_cwd_not_git_repo(self, mock_popeno):

        mock_popeno().wait.return_value = 1

        self.assertFalse(gh_deploy._is_cwd_git_repo())

    @mock.patch('subprocess.Popen')
    def test_get_current_sha(self, mock_popeno):

        mock_popeno().communicate.return_value = (b'6d98394\n', b'')

        self.assertEqual(gh_deploy._get_current_sha('.'), u'6d98394')

    @mock.patch('subprocess.Popen')
    def test_get_remote_url_ssh(self, mock_popeno):

        mock_popeno().communicate.return_value = (
            b'git@github.com:frododocs/frododocs.git\n',
            b''
        )

        expected = (u'git@', u'frododocs/frododocs.git')
        self.assertEqual(expected, gh_deploy._get_remote_url('origin'))

    @mock.patch('subprocess.Popen')
    def test_get_remote_url_http(self, mock_popeno):

        mock_popeno().communicate.return_value = (
            b'https://github.com/frododocs/frododocs.git\n',
            b''
        )

        expected = (u'https://', u'frododocs/frododocs.git')
        self.assertEqual(expected, gh_deploy._get_remote_url('origin'))

    @mock.patch('subprocess.Popen')
    def test_get_remote_url_enterprise(self, mock_popeno):

        mock_popeno().communicate.return_value = (
            b'https://notgh.com/frododocs/frododocs.git\n',
            b''
        )

        expected = (None, None)
        self.assertEqual(expected, gh_deploy._get_remote_url('origin'))

    @mock.patch('frododocs.commands.gh_deploy._is_cwd_git_repo', return_value=True)
    @mock.patch('frododocs.commands.gh_deploy._get_current_sha', return_value='shashas')
    @mock.patch('frododocs.commands.gh_deploy._get_remote_url', return_value=(None, None))
    @mock.patch('frododocs.commands.gh_deploy._check_version')
    @mock.patch('frododocs.commands.gh_deploy.ghp_import.ghp_import', return_value=(True, ''))
    def test_deploy(self, mock_import, check_version, get_remote, get_sha, is_repo):

        config = load_config(
            remote_branch='test',
        )
        gh_deploy.gh_deploy(config)

    @mock.patch('frododocs.commands.gh_deploy._is_cwd_git_repo', return_value=True)
    @mock.patch('frododocs.commands.gh_deploy._get_current_sha', return_value='shashas')
    @mock.patch('frododocs.commands.gh_deploy._get_remote_url', return_value=(None, None))
    @mock.patch('frododocs.commands.gh_deploy._check_version')
    @mock.patch('frododocs.commands.gh_deploy.ghp_import.ghp_import', return_value=(True, ''))
    @mock.patch('os.path.isfile', return_value=False)
    def test_deploy_no_cname(self, mock_isfile, mock_import, check_version, get_remote,
                             get_sha, is_repo):

        config = load_config(
            remote_branch='test',
        )
        gh_deploy.gh_deploy(config)

    @mock.patch('frododocs.commands.gh_deploy._is_cwd_git_repo', return_value=True)
    @mock.patch('frododocs.commands.gh_deploy._get_current_sha', return_value='shashas')
    @mock.patch('frododocs.commands.gh_deploy._get_remote_url', return_value=(
        u'git@', u'frododocs/frododocs.git'))
    @mock.patch('frododocs.commands.gh_deploy._check_version')
    @mock.patch('frododocs.commands.gh_deploy.ghp_import.ghp_import', return_value=(True, ''))
    def test_deploy_hostname(self, mock_import, check_version, get_remote, get_sha, is_repo):

        config = load_config(
            remote_branch='test',
        )
        gh_deploy.gh_deploy(config)

    @mock.patch('frododocs.commands.gh_deploy._is_cwd_git_repo', return_value=True)
    @mock.patch('frododocs.commands.gh_deploy._get_current_sha', return_value='shashas')
    @mock.patch('frododocs.commands.gh_deploy._get_remote_url', return_value=(None, None))
    @mock.patch('frododocs.commands.gh_deploy._check_version')
    @mock.patch('frododocs.commands.gh_deploy.ghp_import.ghp_import', return_value=(True, ''))
    def test_deploy_ignore_version_default(self, mock_import, check_version, get_remote, get_sha, is_repo):

        config = load_config(
            remote_branch='test',
        )
        gh_deploy.gh_deploy(config)
        check_version.assert_called_once()

    @mock.patch('frododocs.commands.gh_deploy._is_cwd_git_repo', return_value=True)
    @mock.patch('frododocs.commands.gh_deploy._get_current_sha', return_value='shashas')
    @mock.patch('frododocs.commands.gh_deploy._get_remote_url', return_value=(None, None))
    @mock.patch('frododocs.commands.gh_deploy._check_version')
    @mock.patch('frododocs.commands.gh_deploy.ghp_import.ghp_import', return_value=(True, ''))
    def test_deploy_ignore_version(self, mock_import, check_version, get_remote, get_sha, is_repo):

        config = load_config(
            remote_branch='test',
        )
        gh_deploy.gh_deploy(config, ignore_version=True)
        check_version.assert_not_called()

    @mock.patch('frododocs.commands.gh_deploy._is_cwd_git_repo', return_value=True)
    @mock.patch('frododocs.commands.gh_deploy._get_current_sha', return_value='shashas')
    @mock.patch('frododocs.commands.gh_deploy._check_version')
    @mock.patch('frododocs.utils.ghp_import.ghp_import')
    @mock.patch('frododocs.commands.gh_deploy.log')
    def test_deploy_error(self, mock_log, mock_import, check_version, get_sha, is_repo):
        error_string = 'TestError123'
        mock_import.return_value = (False, error_string)

        config = load_config(
            remote_branch='test',
        )

        self.assertRaises(SystemExit, gh_deploy.gh_deploy, config)
        mock_log.error.assert_called_once_with('Failed to deploy to GitHub with error: \n%s',
                                               error_string)


class TestGitHubDeployLogs(LogTestCase):

    @mock.patch('subprocess.Popen')
    def test_frododocs_newer(self, mock_popeno):

        mock_popeno().communicate.return_value = (b'Deployed 12345678 with FrodoDocs version: 0.1.2\n', b'')

        with self.assertLogs('frododocs', level='INFO') as cm:
            gh_deploy._check_version('gh-pages')
        self.assertEqual(
            cm.output, ['INFO:frododocs.commands.gh_deploy:Previous deployment was done with FrodoDocs '
                        'version 0.1.2; you are deploying with a newer version ({})'.format(__version__)]
        )

    @mock.patch('subprocess.Popen')
    def test_frododocs_older(self, mock_popeno):

        mock_popeno().communicate.return_value = (b'Deployed 12345678 with FrodoDocs version: 10.1.2\n', b'')

        with self.assertLogs('frododocs', level='ERROR') as cm:
            self.assertRaises(SystemExit, gh_deploy._check_version, 'gh-pages')
        self.assertEqual(
            cm.output, ['ERROR:frododocs.commands.gh_deploy:Deployment terminated: Previous deployment was made with '
                        'FrodoDocs version 10.1.2; you are attempting to deploy with an older version ({}). Use '
                        '--ignore-version to deploy anyway.'.format(__version__)]
        )

    @mock.patch('subprocess.Popen')
    def test_version_unknown(self, mock_popeno):

        mock_popeno().communicate.return_value = (b'No version specified\n', b'')

        with self.assertLogs('frododocs', level='WARNING') as cm:
            gh_deploy._check_version('gh-pages')
        self.assertEqual(
            cm.output,
            ['WARNING:frododocs.commands.gh_deploy:Version check skipped: No version specificed in previous deployment.']
        )
