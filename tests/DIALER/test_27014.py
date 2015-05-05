# 27014: Do not add dialed number 
# ** Procedure
#       1. Dial the number and press "add to contact" button
#       2. Select "Cancel"
# ** Expected Results
#       2. User is taken back to contact info
#  
import time
import sys
sys.path.insert(1, "./")
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact
from tests.i18nsetup import setup_translations


class test_main(SpreadtrumTestCase):

    def setUp(self):
        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)
        _ = setup_translations(self)

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.test_contact = MockContact()
        self.UTILS.general.insertContact(self.test_contact)

        # Generate an entry in the call log
        self.dialer.launch()
        self.dialer.callLog_clearAll()
        self.dialer.createMultipleCallLogEntries(self.phone_number, 1)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        # Open the call log and add to our contact, cancelling the process
        self.dialer.callLog_addToContact(self.phone_number, self.test_contact["name"], cancel_process=True)

        # Check we're back in the call log.
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)
        call_info_header = self.UTILS.element.getElement(DOM.Dialer.call_info_title, "Call info header")
        self.UTILS.test.test(call_info_header.text == self.phone_number, "We are back to call info screen")
