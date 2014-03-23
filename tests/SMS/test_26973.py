#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from tests._mock_data.contacts import MockContact
#import time

class test_main(GaiaTestCase):

    test_msg = "Test message."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        self.num1 = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.emailAddy = self.UTILS.general.get_os_variable("GMAIL_1_EMAIL")

        self.cont = MockContact(email = [{"type": "Personal", "value": "email1@nowhere.com"},
                               {"type": "Personal", "value": "email2@nowhere.com"},
                               {"type": "Personal", "value": "email3@nowhere.com"}])
        self.UTILS.general.insertContact(self.cont)

        self.UTILS.general.addFileToDevice('./tests/_resources/contact_face.jpg',
                                    destination='DCIM/100MZLLA')

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Make sure we have no threads (currently blocked - use _RESTART_DEVICE instead).
        #
#         self.messages.deleteAllThreads()

        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.num1], "Hello " + self.emailAddy + " old bean.")
        x = self.messages.waitForReceivedMsgInThisThread()

        #
        # Long press the email link.
        #
        link = x.find_element("tag name", "a")
        link.tap()

        #
        # Click 'Add to an existing contact'.
        #
        x = self.UTILS.element.getElement(("xpath", "//button[text()='Add to an existing contact']"),
                                   "Create new contact button")
        x.tap()

        #
        # Verify that the email is in the email field.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        x = self.UTILS.element.getElement(DOM.Contacts.view_all_contact_HM, "Search item")
        x.tap()

        self.UTILS.element.waitForElements(("xpath",
                                "//input[@type='email' and @value='{}']".format(self.emailAddy)),
                                "New email address")

        #
        # Add gallery image.
        #
        self.contacts.addGalleryImageToContact(0)


        #
        # Press the Update button.
        #
        done_button = self.UTILS.element.getElement(DOM.Contacts.edit_update_button,
                                            "'Update' button")
        done_button.tap()

        #
        # Check that the contacts iframe is now gone.
        #
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@src,'contacts')]"),
                                       "Contact app iframe")

        #
        # Now return to the SMS app.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)