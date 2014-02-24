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
        self.messages   = Messages(self)
        
        #
        # Prepare the contact we're going to insert.
        #
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.Contact_1 = MockContact(tel = {'type': '', 'value': self.num1})

        self.UTILS.insertContact(self.Contact_1)
        self.UTILS.logComment("Using target telephone number " + self.Contact_1["tel"]["value"])

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Send a message to create a thread (use number, not name as this
        # avoids some blocking bugs just now). 
        #
        self.messages.createAndSendSMS( [self.Contact_1["tel"]["value"]], "Test message.")
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Examine the carrier.
        #
        x = self.UTILS.getElement(DOM.Messages.type_and_carrier_field, "Type and carrier information")
        
        expect = self.Contact_1["tel"]["type"]
        actual = self.messages.threadType()
        self.UTILS.TEST(expect == actual, "The type is listed as: '" + expect + "' (subheader was '" + actual + "').")
        
        expect = self.Contact_1["tel"]["value"]
        actual = self.messages.threadCarrier()
        self.UTILS.TEST(expect == actual, "The carrier is listed as: '" + expect + "' (subheader was '" + actual + "').")