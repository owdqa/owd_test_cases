#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)
        
        #
        # Prepare the contact we're going to insert.
        #
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact_1 = MockContact(tel = {'type': '', 'value': self.num1})
        self.contact_2 = MockContact(tel = {'type': '', 'value': self.num1})

        self.UTILS.insertContact(self.contact_1)
        self.UTILS.logComment("Using target telephone number " + self.contact_1["tel"]["value"])

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
        self.messages.createAndSendSMS( [self.contact_1["tel"]["value"]], "Test message.")
        self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Open contacts app and modify the contact used to send the SMS in the previous step
        #
        self.contacts.launch()
        self.UTILS.logComment("Using target telephone number " + self.contact_2["tel"]["value"])
        self.contacts.editContact(self.contact_1["name"], self.contact_2)
        
        #
        # Re-launch messages app.
        #
        self.messages.launch()
        
        #
        # Verify the thread now contains the name of the contact instead of the phone number
        #
        self.UTILS.logComment("Trying to open the thread with name: " + self.contact_2["name"])
        self.messages.openThread(self.contact_2["name"])
