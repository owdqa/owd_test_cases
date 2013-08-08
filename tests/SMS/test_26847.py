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
from tests._mock_data.contacts import MockContacts

class test_main(GaiaTestCase):
    
    _TestMsg     = "Test message."
    _RESTART_DEVICE = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        
        
        #
        # Prepare the contact we're going to insert.
        #
        self.contact_1 = MockContacts().Contact_1
        self.contact_2 = MockContacts().Contact_2
        self.contact_3 = MockContacts().Contact_longName
        
        #
        # Add this contact (quick'n'dirty method - we're just testing sms, no adding a contact).
        #
        self.data_layer.insert_contact(self.contact_1)
        self.data_layer.insert_contact(self.contact_2)
        self.data_layer.insert_contact(self.contact_3)
        
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
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
        self.messages.createAndSendSMS([self.contact_1["tel"]["value"]], self._TestMsg)
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        self.messages.createAndSendSMS([self.contact_2["tel"]["value"]], self._TestMsg)
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        self.messages.createAndSendSMS([self.contact_3["tel"]["value"]], self._TestMsg)
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        
        #
        # Delete all threads, except the last one.
        #
        x = self.UTILS.getElement(DOM.Messages.edit_threads_button, "Edit threads button")
        x.tap()
        
        x = self.UTILS.getElements(DOM.Messages.threads, "Message thread checkboxes")
        for i in range(0,len(x)-1):
            x[i].tap()
        
        self.messages.deleteSelectedThreads()
        
        #
        # Check there is now only 1 thread.
        #
        x = self.UTILS.getElements(DOM.Messages.threads, "Message thread checkboxes")
        self.UTILS.TEST(len(x) == 1, "Only 1 thread is left after deleting the other two.")
        
