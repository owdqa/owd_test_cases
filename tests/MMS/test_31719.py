#
# TC_MMSTC_COMPT_015b
# USIM Addresses
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
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.contacts   = Contacts(self)
        self.gallery    = Gallery(self)
        
        #
        # Import contact (adjust the correct number).
        #
        self.Contact_1 = MockContacts().Contact_1
        self.Contact_1["tel"]["value"] = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Using target telephone number " + self.Contact_1["tel"]["value"])

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):

        #
        # Load files into the device.
        #
        self.UTILS.addFileToDevice('./tests/_resources/imgd.jpg', destination='DCIM/100MZLLA')

        self.contacts.launch()
        self.contacts.createNewContact(self.Contact_1)

        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Type a message containing the required string 
        #
        self.messages.startNewSMS()
        self.messages.enterSMSMsg("Test")

        self.messages.createMMSImage()
        self.gallery.clickThumbMMS(0)
        
        #
        # Search for our contact.
        #
        orig_iframe = self.messages.selectAddContactButton()
        self.contacts.search(self.Contact_1["name"])
        self.contacts.checkSearchResults(self.Contact_1["name"])

        x = self.UTILS.getElements(DOM.Contacts.search_results_list, "Contacts search results")
        for i in x:
            if i.text == self.Contact_1["name"]:
                i.tap()
                break
        
        #
        # Switch back to the sms iframe.
        #
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame("src",orig_iframe)
        
        #
        # Now check the correct name is in the 'To' list.
        #
        self.messages.checkIsInToField(self.Contact_1["name"])
        self.messages.sendSMS()
        
        #
        # Receiving the message is not part of the test, so just wait a 
        # few seconds for the returned sms in case it messes up the next test.
        #
        time.sleep(5)