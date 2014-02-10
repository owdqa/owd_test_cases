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
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        self.contacts   = Contacts(self)
        
        self.cont1 = MockContacts().Contact_1
                
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.UTILS.addFileToDevice('./tests/_resources/contact_face.jpg', destination='DCIM/100MZLLA')
        self.contacts.launch()
        self.contacts.createNewContact(self.cont1,"gallery")

        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        
        self.dialer.launch()
        self.dialer.enterNumber(self.cont1["tel"]["value"])
        self.dialer.callThisNumber()
        time.sleep(2)
        self.dialer.hangUp()
        
        self.dialer.openCallLog()

        x = self.UTILS.getElement( ("xpath", DOM.Dialer.call_log_number_xpath % self.cont1["tel"]["value"]),
                           "The call log for number %s" % self.cont1["tel"]["value"])
        x.tap()

        time.sleep(2)
        self.UTILS.switchToFrame(*DOM.Dialer.call_log_contact_name_iframe, p_viaRootFrame=False)
        
        x = self.UTILS.getElement(DOM.Contacts.view_contact_tel_field, "Telephone field")
        x.tap()
        
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator_calling)

        self.UTILS.waitForElements( ("xpath", DOM.Dialer.outgoing_call_numberXP % self.cont1["name"]),
                                    "Outgoing call found with number matching %s" % self.cont1["name"])

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of dialer", x)

        time.sleep(2)
        self.dialer.hangUp()
