from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact

class test_main(PixiTestCase):

    test_msg = "Test."

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.messages = Messages(self)

        #
        # Prepare the contact we're going to insert.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.contact = MockContact(givenName = '', familyName = '', name = '', tel = {'type': '', 'value': self.phone_number})

        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Clear out any current messages.
        #
        self.messages.launch()

        #
        # Create SMS.
        #
        self.messages.startNewSMS()
        self.messages.addNumbersInToField([ self.contact["tel"]["value"] ])
        self.messages.enterSMSMsg(self.test_msg)

        #
        # Click send.
        #
        self.messages.sendSMS()

        #
        # Wait for the last message in this thread to be a 'received' one.
        #
        self.messages.wait_for_message()

        #
        # Verify the number is shown in the header as there is no contact name
        #
        self.messages.checkThreadHeader(str(self.contact["tel"]["value"]))
