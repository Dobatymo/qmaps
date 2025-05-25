from unittest import TestCase

from genutility.test import parametrize

from qmaps.base import jsrepr


class BaseTest(TestCase):
    @parametrize(
        (None, "null"),
        ("str", "'str'"),
    )
    def test_jsrepr(self, obj, truth):
        result = jsrepr(obj)
        self.assertEqual(truth, result)
