from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact

class test_main(GaiaTestCase):

    test_msg = "Test."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        #
        # Prepare the contact we're going to import.
        #
        tlf = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.contact = MockContact(tel={'type': 'Mobile', 'value': tlf})

        self.UTILS.reporting.logComment("Using target telephone number " + self.contact["tel"]["value"])

        #
        # Add this contact (quick'n'dirty method - we're just testing sms, 
        # no adding a contact).
        #
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        self.messages.create_and_send_sms([self.contact["tel"]["value"]], self.test_msg)
