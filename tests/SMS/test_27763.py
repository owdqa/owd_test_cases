from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.utils.contacts import MockContact


class test_main(PixiTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        #
        # Prepare the contact we're going to insert.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.contact = MockContact(tel={'type': '', 'value': self.phone_number})

        self.UTILS.general.insertContact(self.contact)
        self.UTILS.reporting.logComment("Using target telephone number " + self.contact["tel"]["value"])

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Send a message to create a thread (use number, not name as this
        # avoids some blocking bugs just now). 
        #
        self.messages.create_and_send_sms( [self.contact["tel"]["value"]], "Test message.")
        returnedSMS = self.messages.wait_for_message()

        #
        # Examine the header.
        #
        self.UTILS.element.headerCheck(self.contact["name"])
