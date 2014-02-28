#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import *
#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContacts
import time


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.dialer = Dialer(self)
        self.settings = Settings(self)


    def tearDown(self):


        self.UTILS.reportResults()

    def test_run(self):
        # Launch dialer app.
        self.dialer.launch()
        self.dialer.enterNumber("#31#")

         #
        # Calls the current number.
        #
        x = self.UTILS.getElement(DOM.Dialer.call_number_button, "Call number button")
        x.tap()

        time.sleep(5)

        x = self.UTILS.getElement(DOM.Dialer.message_calleID, "Message Call ID")

        self.UTILS.assertEqual(x.text, "Service has been disabled", "Caller ID NOT restricted")

