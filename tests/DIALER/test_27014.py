# 27014: Do not add dialed number 
# ** Procedure
#       1. Dial the number and press "add to contact" button
#       2. Select "Cancel"
# ** Expected Results
#       2. User is taken back to the dialer
#  
import time
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact
from tests.i18nsetup import setup_translations


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
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
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Open the call log and add to our contact, cancelling the process
        self.dialer.callLog_addToContact(self.phone_number, self.test_contact["name"], cancel_process=True)

        # Check we're back in the call log.
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)
        header = ('xpath', DOM.GLOBAL.app_head_specific.format(_("Call log")))
        self.UTILS.element.waitForElements(header, "Call log header")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Final screenshot and html dump:", x)
