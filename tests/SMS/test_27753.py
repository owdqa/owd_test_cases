#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *
import time

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContacts

class test_main(GaiaTestCase):
    
    _TestMsg     = "Test."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        self.messages   = Messages(self)
        
        #
        # Prepare the contact we're going to insert.
        #
        self.contact_1 = MockContacts().Contact_1

        #
        # Establish which phone number to use.
        #
        self.num = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact_1["tel"]["value"] = self.num
        self.UTILS.logComment("Using target telephone number " + self.contact_1["tel"]["value"])
        
        #
        # Import this contact (quick'n'dirty method - we're just testing sms, no adding a contact).
        #
        self.data_layer.insert_contact(self.contact_1)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        msgapp = self.messages.launch()
        self.messages.createAndSendSMS([self.num], "Test")
        self.messages.waitForReceivedMsgInThisThread()
        
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        self.messages.openThread(self.contact_1["name"])
        
        #
        # Delete the contact
        #
        self.apps.kill(msgapp)
        self.contacts.launch()
        self.contacts.deleteContact(self.contact_1["name"])
        
        #
        # Go back to SMS app and try to open the thread by phone number
        #
        self.messages.launch()
        self.messages.openThread(self.contact_1["tel"]["value"])

