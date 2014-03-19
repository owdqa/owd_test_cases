#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from tests._mock_data.contacts import MockContact
import time


class test_main(GaiaTestCase):

    link = "owdqatestone@gmail.com"
    test_msg = "Test " + link + " this."


    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        #
        # Insert a contact without email addresses
        # 
        self.UTILS.general.addFileToDevice('./tests/_resources/contact_face.jpg',
                                    destination='DCIM/100MZLLA')
        self.contact = MockContact(email = {'type': 'Personal', 'value': ''})

        self.UTILS.general.insertContact(self.contact)
   
        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.target_telNum)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self): 
        #
        # Launch messages app.
        #
        self.messages.launch()
  
        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.target_telNum], self.test_msg)
  
        #
        # Wait for the last message in this thread to be a 'received' one
        # and click the link.
        #
        x = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.test.TEST(x, "Received a message.", True)

        a=x.find_element("tag name", "a")

        a.tap()

        #
        # Press 'add to existing contact' button.
        #
        w = self.UTILS.element.getElement(DOM.Messages.header_add_to_contact_btn,
                                    "Add to existing contact button")
        w.tap()
    
        #
        # Switch to Contacts app.
        #
        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        #
        # Select the contact.
        #
        z = self.UTILS.element.getElement(DOM.Contacts.view_all_contact_JS, "Search item")
        z.tap()   
 
        #
        # Fill out all the other details.
        #
        contFields = self.contacts.getContactFields()

        #
        # Put the contact details into each of the fields (this method
        # clears each field first).
        #

        for key, value in contFields.items():
            self.contact.replaceStr(value, self.contact[key] + "bis")

        self.contacts.addGalleryImageToContact(0)
    
        #
        # Add another email address.
        #
        self.contacts.addAnotherEmailAddress(self.contact["email"]["value"])

        #
        # Press the Done button.
        #
        done_button = self.UTILS.element.getElement(DOM.Contacts.done_button, "'Done' button")
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