"""Test some features of the command line interface of khard.

This also contains some "end to end" tests.  That means some very high level
calls to the main function and a check against the output.  These might later
be converted to proper "unit" tests.
"""
# pylint: disable=missing-docstring

# TODO We are still missing high level tests for the add-email and merge
# subcommands.  They depend heavily on user interaction and are hard to test in
# their current form.

import io
import pathlib
import shutil
import tempfile
import unittest
from unittest import mock

from ruamel.yaml import YAML

from khard import cli
from khard import config
from khard import khard

from .helpers import expectedFailureForVersion, with_vcards


def mock_stdout():
    stdout = io.StringIO()
    context_manager = mock.patch('sys.stdout', stdout)
    context_manager.getvalue = stdout.getvalue
    return context_manager


@mock.patch('sys.argv', ['TESTSUITE'])
class HelpOption(unittest.TestCase):

    def _test(self, args, expect):
        """Test the command line args and compare the prefix of the output."""
        with self.assertRaises(SystemExit):
            with mock_stdout() as stdout:
                cli.parse_args(args)
        text = stdout.getvalue()
        self.assertTrue(text.startswith(expect))

    def test_global_help(self):
        self._test(['-h'], 'usage: TESTSUITE [-h]')

    @mock.patch.dict('os.environ', KHARD_CONFIG='test/fixture/minimal.conf')
    def test_subcommand_help(self):
        self._test(['list', '-h'], 'usage: TESTSUITE list [-h]')

    def test_global_help_with_subcommand(self):
        self._test(['-h', 'list'], 'usage: TESTSUITE [-h]')


@mock.patch.dict('os.environ', KHARD_CONFIG='test/fixture/minimal.conf')
class ListingCommands(unittest.TestCase):
    """Tests for subcommands that simply list stuff."""

    def test_simple_ls_without_options(self):
        with mock_stdout() as stdout:
            khard.main(['list'])
        text = [l.strip() for l in stdout.getvalue().splitlines()]
        expected = [
            "Address book: foo",
            "Index    Name              Phone                "
            "Email                     Uid",
            "1        second contact    voice: 0123456789    "
            "home: user@example.com    testuid1",
            "2        text birthday                          "
            "                          testuid3",
            "3        third contact                          "
            "                          testuid2"]
        self.assertListEqual(text, expected)

    def test_ls_fields_like_email(self):
        with mock_stdout() as stdout:
            khard.main(['ls', '-p', '-F', 'emails.home.0,name'])
        text = stdout.getvalue().splitlines()
        expected = [
            "user@example.com\tsecond contact",
            "\ttext birthday",
            "\tthird contact",
        ]
        self.assertListEqual(text, expected)

    @mock.patch.dict('os.environ', LC_ALL='C')
    def test_simple_bdays_without_options(self):
        with mock_stdout() as stdout:
            khard.main(['birthdays'])
        text = [line.strip() for line in stdout.getvalue().splitlines()]
        expect = ["Name              Birthday",
                  "text birthday     circa 1800",
                  "second contact    01/20/18"]
        self.assertListEqual(text, expect)

    def test_parsable_bdays(self):
        with mock_stdout() as stdout:
            khard.main(['birthdays', '--parsable'])
        text = stdout.getvalue().splitlines()
        expect = ["circa 1800\ttext birthday", "2018.01.20\tsecond contact"]
        self.assertListEqual(text, expect)

    def test_simple_email_without_options(self):
        with mock_stdout() as stdout:
            khard.main(['email'])
        text = [line.strip() for line in stdout.getvalue().splitlines()]
        expect = ["Name              Type    E-Mail",
                  "second contact    home    user@example.com"]
        self.assertListEqual(text, expect)

    def test_simple_phone_without_options(self):
        with mock_stdout() as stdout:
            khard.main(['phone'])
        text = [line.strip() for line in stdout.getvalue().splitlines()]
        expect = ["Name              Type     Phone",
                  "second contact    voice    0123456789"]
        self.assertListEqual(text, expect)

    def test_simple_file_without_options(self):
        with mock_stdout() as stdout:
            khard.main(['filename'])
        text = [line.strip() for line in stdout.getvalue().splitlines()]
        expect = ["test/fixture/test.abook/contact1.vcf",
                  "test/fixture/test.abook/text-bday.vcf",
                  "test/fixture/test.abook/contact2.vcf"]
        self.assertListEqual(text, expect)

    def test_simple_abooks_without_options(self):
        with mock_stdout() as stdout:
            khard.main(['addressbooks'])
        text = stdout.getvalue().strip()
        expect = "foo"
        self.assertEqual(text, expect)

    def test_simple_details_without_options(self):
        with mock_stdout() as stdout:
            khard.main(['details', 'uid1'])
        text = stdout.getvalue()
        # Currently the FN field is not shown with "details".
        self.assertIn('Address book: foo', text)
        self.assertIn('UID: testuid1', text)

    def test_order_of_search_term_does_not_matter(self):
        with mock_stdout() as stdout1:
            khard.main(['list', 'second', 'contact'])
        with mock_stdout() as stdout2:
            khard.main(['list', 'contact', 'second'])
        text1 = [l.strip() for l in stdout1.getvalue().splitlines()]
        text2 = [l.strip() for l in stdout2.getvalue().splitlines()]
        expected = [
            "Address book: foo",
            "Index    Name              Phone                "
            "Email                     Uid",
            "1        second contact    voice: 0123456789    "
            "home: user@example.com    testuid1"]
        self.assertListEqual(text1, expected)
        self.assertListEqual(text2, expected)

    def test_case_of_search_terms_does_not_matter(self):
        with mock_stdout() as stdout1:
            khard.main(['list', 'second', 'contact'])
        with mock_stdout() as stdout2:
            khard.main(['list', 'SECOND', 'CONTACT'])
        text1 = [l.strip() for l in stdout1.getvalue().splitlines()]
        text2 = [l.strip() for l in stdout2.getvalue().splitlines()]
        expected = [
            "Address book: foo",
            "Index    Name              Phone                "
            "Email                     Uid",
            "1        second contact    voice: 0123456789    "
            "home: user@example.com    testuid1"]
        self.assertListEqual(text1, expected)
        self.assertListEqual(text2, expected)

    def test_regex_special_chars_are_not_special(self):
        with self.assertRaises(SystemExit):
            with mock_stdout() as stdout:
                khard.main(['list', 'uid.'])
        self.assertEqual(stdout.getvalue(), "Found no contacts\n")

    def test_display_post_address(self):
        with mock_stdout() as stdout:
            with with_vcards(["test/fixture/vcards/post.vcf"]):
                khard.main(['postaddress'])
        text = [line.rstrip() for line in stdout.getvalue().splitlines()]
        expected = [
            'Name                 Type    Post address',
            'With post address    home    Main Street 1',
            '                             PostBox Ext',
            '                             00000 The City',
            '                             SomeState, HomeCountry']

        self.assertListEqual(expected, text)


class ListingCommands2(unittest.TestCase):

    def test_list_bug_195(self):
        with with_vcards(['test/fixture/vcards/tel-value-uri.vcf']):
            with mock_stdout() as stdout:
                khard.main(['list'])
        text = [line.strip() for line in stdout.getvalue().splitlines()]
        expect = [
            "Address book: tmp",
            "Index    Name       Phone             Email    Uid",
            "1        bug 195    cell: 67545678             b"]
        self.assertListEqual(text, expect)

    def test_list_bug_243_part_1(self):
        """Search for a category with the ls command"""
        with with_vcards(['test/fixture/vcards/category.vcf']):
            with mock_stdout() as stdout:
                khard.main(['list', 'bar'])
        text = [line.strip() for line in stdout.getvalue().splitlines()]
        expect = [
            "Address book: tmp",
            "Index    Name                     Phone    "
            "Email                        Uid",
            "1        contact with category             "
            "internet: foo@example.org    c",
        ]
        self.assertListEqual(text, expect)

    def test_list_bug_243_part_2(self):
        """Search for a category with the email command"""
        with with_vcards(['test/fixture/vcards/category.vcf']):
            with mock_stdout() as stdout:
                khard.main(['email', 'bar'])
        text = [line.strip() for line in stdout.getvalue().splitlines()]
        expect = [
            "Name                     Type        E-Mail",
            "contact with category    internet    foo@example.org",
        ]
        self.assertListEqual(text, expect)

    def test_list_bug_249(self):
        with with_vcards(['test/fixture/vcards/issue249.vcf']):
            with mock_stdout() as stdout:
                # If all spaces are removed this should match "Foo Bar"
                khard.main(['list', 'oba'])
        text = [line.strip() for line in stdout.getvalue().splitlines()]
        expect = ['Address book: tmp',
                  'Index    Name       Phone    Email    Uid',
                  '1        Foo Bar                      i']
        self.assertListEqual(text, expect)


class FileSystemCommands(unittest.TestCase):
    """Tests for subcommands that interact with different address books."""

    def setUp(self):
        "Create a temporary directory with two address books and a configfile."
        self._tmp = tempfile.TemporaryDirectory()
        path = pathlib.Path(self._tmp.name)
        self.abook1 = path / 'abook1'
        self.abook2 = path / 'abook2'
        self.abook1.mkdir()
        self.abook2.mkdir()
        self.contact = self.abook1 / 'contact.vcf'
        shutil.copy('test/fixture/vcards/contact1.vcf', str(self.contact))
        config = path / 'conf'
        with config.open('w') as fh:
            fh.write("""[addressbooks]
                        [[abook1]]
                        path = {}
                        [[abook2]]
                        path = {}""".format(self.abook1, self.abook2))
        self._patch = mock.patch.dict('os.environ', KHARD_CONFIG=str(config))
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        self._tmp.cleanup()

    def test_simple_move(self):
        # just hide stdout
        with mock.patch('sys.stdout'):
            khard.main(['move', '-a', 'abook1', '-A', 'abook2', 'testuid1'])
        # The contact is moved to a filename based on the uid.
        target = self.abook2 / 'testuid1.vcf'
        # We currently only assert that the target file exists, nothing about
        # its contents.
        self.assertFalse(self.contact.exists())
        self.assertTrue(target.exists())

    def test_simple_copy(self):
        # just hide stdout
        with mock.patch('sys.stdout'):
            khard.main(['copy', '-a', 'abook1', '-A', 'abook2', 'testuid1'])
        # The contact is copied to a filename based on a new uid.
        results = list(self.abook2.glob('*.vcf'))
        self.assertTrue(self.contact.exists())
        self.assertEqual(len(results), 1)

    def test_simple_remove_with_force_option(self):
        # just hide stdout
        with mock.patch('sys.stdout'):
            # Without the --force this asks for confirmation.
            khard.main(['remove', '--force', '-a', 'abook1', 'testuid1'])
        results = list(self.abook2.glob('*.vcf'))
        self.assertFalse(self.contact.exists())
        self.assertEqual(len(results), 0)

    def test_new_contact_with_simple_user_input(self):
        old = len(list(self.abook1.glob('*.vcf')))
        # Mock user input on stdin (yaml format).
        with mock.patch('sys.stdin.isatty', return_value=False):
            with mock.patch('sys.stdin.read',
                            return_value='First name: foo\nLast name: bar'):
                # just hide stdout
                with mock.patch('sys.stdout'):
                    # hide warning about missing version in vcard
                    with self.assertLogs(level='WARNING'):
                        khard.main(['new', '-a', 'abook1'])
        new = len(list(self.abook1.glob('*.vcf')))
        self.assertEqual(new, old + 1)


class MiscCommands(unittest.TestCase):
    """Tests for other subcommands."""

    @mock.patch.dict('os.environ', KHARD_CONFIG='test/fixture/minimal.conf')
    def test_simple_show_with_yaml_format(self):
        with mock_stdout() as stdout:
            khard.main(["show", "--format=yaml", "uid1"])
        # This implicitly tests if the output is valid yaml.
        yaml = YAML(typ="base").load(stdout.getvalue())
        # Just test some keys.
        self.assertIn('Address', yaml)
        self.assertIn('Birthday', yaml)
        self.assertIn('Email', yaml)
        self.assertIn('First name', yaml)
        self.assertIn('Last name', yaml)
        self.assertIn('Nickname', yaml)

    @expectedFailureForVersion(3, 5)
    @mock.patch.dict('os.environ', KHARD_CONFIG='test/fixture/minimal.conf')
    def test_simple_edit_without_modification(self):
        with mock.patch('subprocess.Popen') as popen:
            # just hide stdout
            with mock.patch('sys.stdout'):
                khard.main(["edit", "uid1"])
        # The editor is called with a temp file so how to we check this more
        # precisely?
        popen.assert_called_once()

    @mock.patch.dict('os.environ', KHARD_CONFIG='test/fixture/minimal.conf',
                     EDITOR='editor')
    def test_edit_source_file_without_modifications(self):
        with mock.patch('subprocess.Popen') as popen:
            # just hide stdout
            with mock.patch('sys.stdout'):
                khard.main(["edit", "--format=vcard", "uid1"])
        popen.assert_called_once_with(['editor',
                                       'test/fixture/test.abook/contact1.vcf'])


@mock.patch.dict('os.environ', KHARD_CONFIG='test/fixture/minimal.conf')
class CommandLineDefaultsDoNotOverwriteConfigValues(unittest.TestCase):

    @staticmethod
    def _with_contact_table(args, **kwargs):
        args = cli.parse_args(args)
        options = '\n'.join('{}={}'.format(key, kwargs[key]) for key in kwargs)
        conf = config.Config(io.StringIO('[addressbooks]\n[[test]]\npath=.\n'
                                         '[contact table]\n' + options))
        return cli.merge_args_into_config(args, conf)

    def test_group_by_addressbook(self):
        conf = self._with_contact_table(['list'], group_by_addressbook=True)
        self.assertTrue(conf.group_by_addressbook)


@mock.patch.dict('os.environ', KHARD_CONFIG='test/fixture/minimal.conf')
class CommandLineArguemtsOverwriteConfigValues(unittest.TestCase):

    @staticmethod
    def _merge(args):
        args, _conf = cli.parse_args(args)
        # This config file just loads all defaults from the config.spec.
        conf = config.Config(io.StringIO('[addressbooks]\n[[test]]\npath=.'))
        return cli.merge_args_into_config(args, conf)

    def test_sort_is_picked_up_from_arguments(self):
        conf = self._merge(['list', '--sort=last_name'])
        self.assertEqual(conf.sort, 'last_name')

    def test_display_is_picked_up_from_arguments(self):
        conf = self._merge(['list', '--display=last_name'])
        self.assertEqual(conf.display, 'last_name')

    def test_reverse_is_picked_up_from_arguments(self):
        conf = self._merge(['list', '--reverse'])
        self.assertTrue(conf.reverse)

    def test_group_by_addressbook_is_picked_up_from_arguments(self):
        conf = self._merge(['list', '--group-by-addressbook'])
        self.assertTrue(conf.group_by_addressbook)

    def test_search_in_source_is_picked_up_from_arguments(self):
        conf = self._merge(['list', '--search-in-source-files'])
        self.assertTrue(conf.search_in_source_files)

#    def test_strict_is_picked_up_from_arguments(self):
#        conf = self._merge(['list', '--strict'])
#        self.assertTrue(conf.strict)


if __name__ == "__main__":
    unittest.main()
