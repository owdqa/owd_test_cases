#===============================================================================
# 26999: Verify the user can cancel the "Create new contact"
# operation from the Contacts APP returning to the SMS thread view
#
# Procedure:
# 1. Send from another device to Device under test an SMS including
# text and a number with  9 DIGITS (e.g. 666777888)
# 2. Open in Device under test the SMS APP
# 3. Search and  tap on the received SMS
# 4. In the SMS thread view long press on the highlighted phone number
# 5. In the Dialog Menu tap on the option : "Create new contact"
# 6. In the "Add form" tap on the icon "X" in order to cancel the operation
# 7. Open Contacts APP
# 8. Verify that no new contact has been added
#
# Expected results:
# The operation "Create new contact" from the selected phone number is
# cancelled by the user, he is returned to the SMS thread view and the
# contact is not created.
#===============================================================================

from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts


class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Launch messages app.
        self.messages.launch()

        # Create and send a new test message.
        test_str = "Nine 123456789 numbers."
        self.messages.create_and_send_sms([self.phone_number], test_str)
        msg = self.messages.wait_for_message()

        # Long press the emedded number link.
        tag = msg.find_element("tag name", "a")
        tag.tap()

        # Select create new contact.
        create_btn = self.UTILS.element.getElement(DOM.Messages.header_create_new_contact_btn,
                                    "Create new contact button")
        create_btn.tap()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        # Cancel the action.
        form_header = self.UTILS.element.getElement(DOM.Contacts.contact_form_header, "Cancel button")
        form_header.tap(25, 25)

        # Wait for the contacts app to go away.
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath",
                                        "//iframe[contains(@src, '{}')]".format(DOM.Contacts.frame_locator[1])),
                                        "Contacts iframe")

        # Kill the SMS app (and all others).
        self.apps.kill_all()

        # Open the contacts app.
        self.contacts.launch()

        # Verify that there are no contacts.
        self.UTILS.element.waitForElements(("xpath", "//p[contains(text(), 'No contacts')]"),
                                    "No contacts message")
