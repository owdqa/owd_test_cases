from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts

class test_main(PixiTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        test_str = "Nine 123456789 numbers."
        self.messages.create_and_send_sms([self.phone_number], test_str)
        x = self.messages.wait_for_message()

        #
        # Long press the emedded number link.
        #
        y = x.find_element("tag name", "a")  
        y.tap()

        #
        # Select create new contact.
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_create_new_contact_btn,
                                    "Create new contact button")
        x.tap()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        #
        # Cancel the action.
        #
        x = self.UTILS.element.getElement(DOM.Contacts.edit_cancel_button, "Cancel button")
        x.tap()

        #
        # Wait for the contacts app to go away.
        #
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath",
                                        "//iframe[contains(@src, '{}')]".format(DOM.Contacts.frame_locator[1])),
                                        "Contacts iframe")

        #
        # Kill the SMS app (and all others).
        #
        self.apps.kill_all()

        #
        # Open the contacts app.
        #
        self.contacts.launch()

        #
        # Verify that there are no contacts.
        #
        self.UTILS.element.waitForElements(("xpath", "//p[contains(text(), 'No contacts')]"),
                                    "No contacts message")
