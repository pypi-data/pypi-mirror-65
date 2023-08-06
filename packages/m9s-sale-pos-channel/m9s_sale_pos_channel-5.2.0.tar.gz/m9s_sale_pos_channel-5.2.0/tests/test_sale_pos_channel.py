# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class SalePosChannelTestCase(ModuleTestCase):
    'Test Sale Pos Channel module'
    module = 'sale_pos_channel'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            SalePosChannelTestCase))
    return suite
