#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.dialer import Dialer
import time


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.settings = Settings(self)


    def tearDown(self):


        self.UTILS.reporting.reportResults()

    def test_run(self):
        # Launch dialer app.
        self.dialer.launch()
        self.dialer.enterNumber("#31#")

         #
        # Calls the current number.
        #
        x = self.UTILS.element.getElement(DOM.Dialer.call_number_button, "Call number button")
        x.tap()

        time.sleep(5)

        x = self.UTILS.element.getElement(DOM.Dialer.message_calleID, "Message Call ID")

        self.assertEqual(x.text, "Service has been disabled", "Caller ID NOT restricted")

