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
from OWDTestToolkit.apps import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from tests._mock_data.contacts import MockContact
import time

class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        self.contacts   = Contacts(self)
        
        self.Contact_1 = MockContact(tel = {'type': 'Mobile', 'value': '665666666'})
        self.UTILS.insertContact(self.Contact_1)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.UTILS.addFileToDevice('./tests/_resources/contact_face.jpg', destination='DCIM/100MZLLA')

        self.dialer.launch()
        self.dialer.enterNumber(self.Contact_1["tel"]["value"])
        self.dialer.callThisNumber()
        time.sleep(10)
     	self.UTILS.switchToFrame(*DOM.Dialer.frame_locator)

        self.dialer.openCallLog()

        x = self.UTILS.getElement( ("xpath", DOM.Dialer.call_log_number_xpath % self.Contact_1["tel"]["value"]),
                           "The call log for number %s" % self.Contact_1["tel"]["value"])
        x.tap()

        time.sleep(2)
        self.UTILS.switchToFrame(*DOM.Dialer.call_log_contact_name_iframe, p_viaRootFrame=False)
        
        x = self.UTILS.getElement(DOM.Contacts.view_contact_tel_field, "Telephone field")
        x.tap()
        
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator_calling)

        self.UTILS.waitForElements( ("xpath", DOM.Dialer.outgoing_call_numberXP.format(self.Contact_1["name"])),
                                    "Outgoing call found with number matching {}".format(self.Contact_1["name"]))

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of dialer", x)

        time.sleep(2)
        self.dialer.hangUp()
