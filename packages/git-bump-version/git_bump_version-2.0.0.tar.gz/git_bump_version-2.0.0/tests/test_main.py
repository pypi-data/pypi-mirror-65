import os
import re
import sys
import errno
import logging
import random
import string
import git_bump_version
from six import StringIO
from mock import patch, Mock, MagicMock, PropertyMock
from pylint.lint import Run as RunPylint
from pylint.reporters.text import TextReporter
from pylint.interfaces import IReporter
from git_bump_version import GitRepository


class TestMain(object):
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup(self):
        self._logger = logging.getLogger('test')

        #Mock GitRepository
        self._git_repo_patcher = patch('git_bump_version.GitRepository')
        self._git_repo_mock = self._git_repo_patcher.start()
        self._git_repo_mock_instance = self._git_repo_mock.return_value

        #Mock stdout
        self._stdout_patcher = patch('sys.stdout', new_callable=StringIO)
        self._stdout_mock = self._stdout_patcher.start()

        #Mock stderr
        self._stderr_patcher = patch('sys.stderr', new_callable=StringIO)
        self._stderr_mock = self._stderr_patcher.start()

    def teardown(self):
        self._git_repo_patcher.stop()
        self._stdout_patcher.stop()
        self._stderr_patcher.stop()
        pass

    def gen_big_random_number(self):
        return random.randint(0, 1000)

    def gen_small_random_number(self):
        return random.randint(0, 15)

    def random_version(self):
        return self.gen_big_random_number(), self.gen_big_random_number(), self.gen_big_random_number()

    def gen_word(self):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(self.gen_small_random_number()))

    def gen_random_parameters(self, branch_prefix="release/", version_prefix=""):
        version = self.random_version()
        branch_name = '{}{}.{}'.format(branch_prefix, version[0], version[1])
        latest_tag = '{}{}.{}.{}'.format(version_prefix, version[0], version[1], version[2])
        expected_tag = '{}{}.{}.{}'.format(version_prefix, version[0], version[1], version[2] + 1)
        initial_tag = '{}{}.{}.0'.format(version_prefix, version[0], version[1])

        self._logger.info("Branch: {}".format(branch_name))
        self._logger.info("Latest Tag: {}".format(latest_tag))
        self._logger.info("Expected Tag: {}".format(expected_tag))
        self._logger.info("Initial Tag: {}".format(initial_tag))

        return branch_name, latest_tag, expected_tag, initial_tag

    def configure_git_repo_mock(self, valid_repo=True, head_tagged=False, branch_name=None, tag_found=False, latest_tag=None):
        self._git_repo_mock_instance.valid = valid_repo
        self._git_repo_mock_instance.is_head_tagged = MagicMock(return_value=head_tagged)
        self._git_repo_mock_instance.branch_name = branch_name
        self._git_repo_mock_instance.find_tag = MagicMock(return_value=(tag_found, latest_tag))
        self._git_repo_mock_instance.create_local_tag = MagicMock(return_value=None)
        self._git_repo_mock_instance.create_remote_tag = MagicMock(return_value=None)

    def verify_not_tagged(self):
        assert not self._git_repo_mock_instance.create_local_tag.called, 'create_local_tag should not have been called'
        assert not self._git_repo_mock_instance.create_remote_tag.called, 'create_remote_tag should not have been called'

    def verify_expected_tag(self, expected_tag, should_tag=True):
        if should_tag:
            self._git_repo_mock_instance.create_local_tag.assert_called_with(expected_tag)
            self._git_repo_mock_instance.create_remote_tag.assert_called_with(expected_tag)
        else:
            self.verify_not_tagged()

        assert self._stdout_mock.getvalue() == '{}\n'.format(expected_tag)

    def verify_error(self):
        assert self._stdout_mock.getvalue() == '', 'Error conditions must not log to stdout'
        assert self._stderr_mock.getvalue() != '', 'Error conditions must log to stderr'
        self.verify_not_tagged()

    def test_invalid_repo(self):
        self.configure_git_repo_mock(valid_repo=False)
        result = git_bump_version.main([])
        assert result is errno.EINVAL, 'return code should have been EINVAL'
        self.verify_error()

    def test_already_tagged(self):
        self.configure_git_repo_mock(head_tagged=True)
        result = git_bump_version.main([])
        assert result is errno.EEXIST, 'return code should have been EEXIST'
        self.verify_error()

    def test_invalid_branch_name(self):
        self.configure_git_repo_mock(branch_name='master')
        result = git_bump_version.main([])
        assert result is errno.EINVAL, 'return code should have been EINVAL'
        self.verify_error()

    def test_bump_version_defaults(self):
        branch_name, latest_tag, expected_tag, _ = self.gen_random_parameters()
        self.configure_git_repo_mock(branch_name=branch_name, tag_found=True, latest_tag=latest_tag)
        result = git_bump_version.main([])
        self.verify_expected_tag(expected_tag)
        assert result is 0, 'return code should have been 0'

    def test_bump_version_first_tag(self):
        branch_name, _, _, expected_tag = self.gen_random_parameters()
        self.configure_git_repo_mock(branch_name=branch_name, tag_found=False)
        result = git_bump_version.main([])
        self.verify_expected_tag(expected_tag)
        assert result is 0, 'return code should have been 0'

    def test_bump_version_dont_tag(self):
        branch_name, latest_tag, expected_tag, _ = self.gen_random_parameters()
        self.configure_git_repo_mock(branch_name=branch_name, tag_found=True, latest_tag=latest_tag)
        result = git_bump_version.main(['--dont_tag'])
        self.verify_expected_tag(expected_tag, should_tag=False)
        assert result is 0, 'return code should have been 0'

    def test_bump_version_custom_branch_regex(self):
        branch_regex = '^(?P<major>\d+)\.(?P<minor>\d+)'
        branch_name = '1.0/release'
        expected_tag = '1.0.0'
        self.configure_git_repo_mock(branch_name=branch_name, tag_found=False)
        result = git_bump_version.main(['--branch_regex', branch_regex])
        self.verify_expected_tag(expected_tag)
        assert result is 0, 'return code should have been 0'

    def test_bump_version_custom_version_prefix(self):
        version_prefix = self.gen_word()
        branch_name, latest_tag, expected_tag, _ = self.gen_random_parameters(version_prefix=version_prefix)
        self.configure_git_repo_mock(branch_name=branch_name, tag_found=True, latest_tag=latest_tag)
        result = git_bump_version.main(['--version_prefix', version_prefix])
        self.verify_expected_tag(expected_tag)
        assert result is 0, 'return code should have been 0'

    def test_bump_version_custom_version_prefix_first_tag(self):
        version_prefix = self.gen_word()
        branch_name, _, _, expected_tag = self.gen_random_parameters(version_prefix=version_prefix)
        self.configure_git_repo_mock(branch_name=branch_name, tag_found=False)
        result = git_bump_version.main(['--version_prefix', version_prefix])
        self.verify_expected_tag(expected_tag)
        assert result is 0, 'return code should have been 0'

    def test_bump_version_custom_branch_regex_version_prefix(self):
        branch_regex = '^(?P<major>\d+)\.(?P<minor>\d+)'
        branch_name = '8.5/release'
        version_prefix = self.gen_word()
        expected_tag = version_prefix + '8.5.4'
        self.configure_git_repo_mock(branch_name=branch_name, tag_found=True, latest_tag=version_prefix + '8.5.3')
        result = git_bump_version.main(['--version_prefix', version_prefix, '--branch_regex', branch_regex])
        self.verify_expected_tag(expected_tag)
        assert result is 0, 'return code should have been 0'


class TestReporter(TextReporter):
    __implements__ = IReporter

    def __init__(self):
        self._logger = logging.getLogger('test')
        self._output = StringIO()
        self._messages = []
        TextReporter.__init__(self, self._output)

    def handle_message(self, msg):
        self._logger.warn('File: {}, Line: {}, Column: {}, Message: {}'.format(msg.path, msg.line, msg.column, msg.msg))
        self._messages.append(msg)

    @property
    def score(self):
        match = re.search(r'Your code has been rated at (\d+\.\d+)/10', self._output.getvalue())
        score = match.group(1)
        score = float(score)
        return score * 10.0


def test_pylint():
    base = os.path.dirname(os.path.abspath(__file__))
    dirname = os.path.abspath(os.path.join(base, '../git_bump_version'))
    reporter = TestReporter()
    RunPylint([dirname], reporter=reporter, exit=False)
    score = reporter.score
    min_score = 100
    assert score >= min_score, 'pylint score {} >= {}'.format(score, min_score)
