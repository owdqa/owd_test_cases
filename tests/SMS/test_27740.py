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

class test_main(GaiaTestCase):
    
    _fake_num    = "12435"
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        
        # Start with no SMS.
        self.data_layer.delete_all_sms()
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Send a message to an invalid number to create a thread with just an
        # outgoing message..
        #
        msg_text = str(time.time())
        self.messages.createAndSendSMS([self._fake_num], msg_text)
         
        #
        # Click ok in the alert.
        #
        x = self.UTILS.getElement(DOM.Messages.service_unavailable_ok, "Service unavailable - OK button")
        x.tap()

        #
        # Return to the threads view.
        #
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        #
        # Get the preview txt for our test.
        #
        preview_text = self.messages.getThreadText(self._fake_num)
        
        self.UTILS.TEST(preview_text in msg_text, 
                        "Preview text (" + preview_text + ") is in the original message text(" + msg_text + ").")
        
