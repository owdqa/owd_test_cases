#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        self.messages   = Messages(self)

        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContact(tel = [{'type': 'Mobile', 'value': '11111111'}, {'type': 'Mobile', 'value': '222222222'}] )

        #
        # We're not testing adding a contact, so just stick one 
        # into the database.
        #
        self.UTILS.insertContact(self.Contact_1)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # Select our contact.
        #
        #
        # View the details of our contact.
        #
        self.contacts.viewContact(self.Contact_1['name'])

        #
        # Tap the 2nd sms button (index=1) in the view details screen to go to the sms page.
        #
        smsBTN = self.UTILS.getElement( ("id", DOM.Contacts.sms_button_specific_id % 1), 
                                        "2nd send SMS button")
        smsBTN.tap()

        #
        # Switch to the 'Messages' app frame (or marionette will still be watching the
        # 'Contacts' app!).
        #
        self.marionette.switch_to_frame()
#         self.UTILS.waitForElements(("xpath", "//iframe[@src='" + DOM.Messages.frame_locator[1] + "']"), 
#                                    "Messaging app frame", False, 20)
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        time.sleep(3)

        #
        # TEST: this automatically opens the 'send SMS' screen, so
        # check the correct name is in the header of this sms.
        #
        self.UTILS.headerCheck("1 recipient")

        #
        # Check this is the right number.
        #
        self.messages.checkIsInToField(self.Contact_1["name"])
        self.messages.checkNumberIsInToField(self.Contact_1["tel"][1]["value"])
