#
# TC_MMSTC_COMPT_015b
# USIM Addresses
#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContact
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps import Contacts
from OWDTestToolkit.apps.gallery import Gallery
import time

class test_main(GaiaTestCase):
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)
        self.gallery = Gallery(self)
        
        #
        # Import contact (adjust to the correct number).
        #
        self.test_num = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.cont = MockContact(tel={"type": "Mobile", "value": self.test_num})

        #
        # TODO - delete this line if you manage to get it working
        #
        self.UTILS.insertContact(self.cont)
        
        self.UTILS.logComment("Using target telephone number " + self.cont["tel"]["value"])

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Load files into the device.
        #
        self.UTILS.addFileToDevice('./tests/_resources/imga.jpg',
                                    destination='DCIM/100MZLLA')

        #
        # TODO - uncommnent
        #
        # self.contacts.launch()
        # self.contacts.createNewContact(self.cont)

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
        time.sleep(5)
        orig_iframe = self.messages.selectAddContactButton()
        time.sleep(5)
        self.contacts.search(self.cont["name"])
        self.contacts.checkSearchResults(self.cont["name"])

        x = self.UTILS.getElements(DOM.Contacts.search_results_list, "Contacts search results")
        for i in x:
            if i.text == self.cont["name"]:
                self.UTILS.logComment("WOLOLOOOOOO")
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
        self.messages.checkIsInToField(self.cont["name"])
        self.messages.sendSMS()
        
        #
        # Receiving the message is not part of the test, so just wait a 
        # few seconds for the returned sms in case it messes up the next test.
        #
        time.sleep(5)