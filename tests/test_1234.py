import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer

import sys
sys.path.insert(1, "./")
from tests.i18nsetup import setup_translations


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        _ = setup_translations(self)

        self.phone_number = "649779117"

    def tearDown(self):
        self.data_layer.set_setting("airplaneMode.enabled", False)
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()
        self.dialer.enterNumber(self.phone_number)
        # self.dialer.call_this_number()
        self.dialer.call_this_number_and_hangup(delay=15)