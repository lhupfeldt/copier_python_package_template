"""Configuration file for 'pytest'"""

import re
import errno
from pathlib import Path
import shutil

from pytest import fixture


_HERE = Path(__file__).absolute().parent

_UNDERSCORE_TEST_RE = re.compile('_test$')

def _test_key_shortener(key_prefix, key_postfix):
    prefix = _UNDERSCORE_TEST_RE.sub('', key_prefix).replace('test.', 'test_') + '_'
    return key_prefix + '.' + key_postfix.replace(prefix, '')


def _test_node_shortener(request):
    """Shorten test node name while still keeping it unique"""
    return _test_key_shortener(request.node.module.__name__, request.node.name.split('[')[0])


@fixture(name="out_dir")
def _fixture_out_dir(request):
    """Create unique top level test directory for a test."""

    out_dir = _HERE/'out'/_test_node_shortener(request)

    try:
        shutil.rmtree(out_dir)
    except OSError as ex:
        if ex.errno != errno.ENOENT:
            raise

    return out_dir

# Add you configuration, e.g. fixtures here.
