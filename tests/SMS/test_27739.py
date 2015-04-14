from OWDTestToolkit.firec_testcase import FireCTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
import time

class test_main(FireCTestCase):

    test_msg = "Test."

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        #
        # Put the phone into airplane mode.
        #
        self.UTILS.statusbar.toggleViaStatusBar('airplane')

    def tearDown(self):
        self.UTILS.statusbar.toggleViaStatusBar('airplane')
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
  
        #
        # Open sms app 
        #
        self.messages.launch()

        #
        # Create a new SMS
        #
        self.messages.startNewSMS()

        #
        # Insert the phone number in the To field
        #
        self.messages.addNumbersInToField([self.UTILS.general.get_config_variable("phone_number", "custom")])

        #
        # Create SMS.
        #
        self.messages.enterSMSMsg(self.test_msg)

        #
        # Click send.
        #
        self.messages.sendSMS(check=False)
        #
        # Check that popup appears.
        #
        self.messages.checkAirplaneModeWarning()
