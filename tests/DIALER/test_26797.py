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
import time

class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        self.dialer     = Dialer(self)
    
        #
        # Get details of our test contacts.
        #
        self.cont = MockContacts().Contact_1
        self.data_layer.insert_contact(self.cont)
        
        self.contact_name=self.cont["givenName"]
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch dialer app.
        #
        self.dialer.launch()
        
        x = self.UTILS.getElement(DOM.Dialer.option_bar_contacts, "Contacts option")
        x.tap()
        
        #
        # Go to the view details screen for this contact.
        #
        #self.marionette.switch_to_frame()
        #=======================================================================
        # self.marionette.switch_to_frame()
        # self.UTILS.waitForNotElements( ("xpath", "//iframe[contains(@%s, '%s')]" % \
        #                                         (DOM.Contacts.frame_locator[0], DOM.Contacts.frame_locator[1])),
        #                                 "COntacts frame")
        # self.UTILS.switchToFrame(*DOM.Dialer.frame_locator)
        # 
        # 
        #=======================================================================
        self.contacts.viewContact(self.contact_name, p_HeaderCheck=False)
        
        x = self.UTILS.getElement(DOM.Contacts.view_contact_tel_field, "Telephone number")
        p_num=x.get_attribute("value")
        x.tap()
        
        #
        # The call is tested.
        #
        time.sleep(1)
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator_calling)
        self.UTILS.waitForElements( ("xpath", DOM.Dialer.outgoing_call_numberXP % p_num),
                                    "Outgoing call found with number matching %s" % p_num)

        time.sleep(2)

        self.dialer.hangUp()
