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
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps import Messages
from OWDTestToolkit.apps import Contacts
from tests._mock_data.contacts import MockContact
import time


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
        self.contact = MockContact(tel = [{'type': 'Mobile', 'value': '11111111'}, {'type': 'Mobile', 'value': '222222222'}] )

        #
        # We're not testing adding a contact, so just stick one
        # into the database.
        #
        self.UTILS.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # View the details of our contact.
        #
        self.contacts.viewContact(self.contact['name'])

        #
        # Tap the 2nd sms button (index=1) in the view details screen to go to the sms page.
        #
        smsBTN = self.UTILS.getElement( ("id", DOM.Contacts.sms_button_specific_id % 0), 
                                        "1st send SMS button")
        smsBTN.tap()

        #
        # Switch to the 'Messages' app frame (or marionette will still be watching the
        # 'Contacts' app!).
        #
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        time.sleep(2)

        #
        # TEST: this automatically opens the 'send SMS' screen, so
        # check the correct name is in the header of this sms.
        #
        self.UTILS.headerCheck("1 recipient")

        #
        # Check this is the right number.
        #
        self.messages.checkIsInToField(self.contact["name"])
        self.messages.checkNumberIsInToField(self.contact["tel"][0]["value"])
