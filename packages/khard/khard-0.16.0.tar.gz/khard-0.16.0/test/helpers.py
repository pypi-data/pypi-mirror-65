"""Helper functions for the tests."""
# pylint: disable=invalid-name

import contextlib
import os
import shutil
import sys
import tempfile
import unittest

import vobject


def expectedFailureForVersion(major, minor):
    "A decorator to mark a test as an expected failure for one python version."
    if sys.version_info.major == major and sys.version_info.minor == minor:
        return unittest.expectedFailure
    return lambda x: x


def create_test_vcard(**kwargs):
    """Create a simple vcard for tests."""
    vcard = vobject.vCard()
    if 'fn' not in kwargs:
        kwargs['fn'] = 'Test vCard'
    if 'version' not in kwargs:
        kwargs['version'] = '3.0'
    for key, value in kwargs.items():
        vcard.add(key.upper()).value = value
    return vcard


class with_vcards(contextlib.ContextDecorator):
    """Context manager to create a temporary khard configuration.

    The given vcards will be copied to the only address book in the
    configuration which will be called "tmp".
    """

    def __init__(self, vcards):
        self.tempdir = None
        self.config = None
        self.vcards = vcards
        self.mock = None

    def __enter__(self):
        self.tempdir = tempfile.TemporaryDirectory()
        for card in self.vcards:
            shutil.copy(card, self.tempdir.name)
        with tempfile.NamedTemporaryFile("w", delete=False) as config:
            config.write("""[general]
                            editor = editor
                            merge_editor = merge_editor
                            [addressbooks]
                            [[tmp]]
                            path = {}
                            """.format(self.tempdir.name))
        self.config = config
        self.mock = unittest.mock.patch.dict('os.environ',
                                             KHARD_CONFIG=config.name)
        self.mock.start()
        return self

    def __exit__(self, _a, _b, _c):
        self.mock.stop()
        os.unlink(self.config.name)
        self.tempdir.cleanup()
        return False
