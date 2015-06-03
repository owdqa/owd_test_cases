from gaiatest import GaiaTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
import time

class test_main(GaiaTestCase):

    test_msg = "Test."

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        # Put the phone into airplane mode.
        self.data_layer.set_setting('airplaneMode.enabled', True)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Open sms app 
        self.messages.launch()

        # Create a new SMS
        self.messages.startNewSMS()

        # Insert the phone number in the To field
        self.messages.addNumbersInToField([self.UTILS.general.get_config_variable("phone_number", "custom")])

        # Create SMS.
        self.messages.enterSMSMsg(self.test_msg)

        # Click send.
        self.messages.sendSMS()
        time.sleep(3)

        # Check that popup appears.
        self.messages.checkAirplaneModeWarning()
