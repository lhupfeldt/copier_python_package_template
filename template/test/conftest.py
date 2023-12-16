"""Configuration file for 'pytest'"""

import re
import errno
from pathlib import Path
import shutil

from pytest import fixture


_HERE = Path(__file__).absolute().parent

_UNDERSCORE_TEST_RE = re.compile('_test$')

def _test_key_shortener(request):
    """Shorten test name while still keeping i unique"""
    key_prefix = _UNDERSCORE_TEST_RE.sub('', request.node.module.__name__)
    key_postfix = request.node.name.split('[')[0]
    tfunc_prefix = key_prefix.replace('test.', 'test_') + '_'
    return key_prefix + '.' + key_postfix.replace(tfunc_prefix, '')


@fixture(name="out_dir")
def _fixture_out_dir(request):
    """Create unique top level test directory for a test."""

    out_dir = _HERE/'out'/_test_key_shortener(request)

    try:
        shutil.rmtree(out_dir)
    except OSError as ex:
        if ex.errno != errno.ENOENT:
            raise

    return out_dir

# Add you configuration, e.g. fixtures here.
