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
        
        self.num  = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        
        self.cont = MockContacts().Contact_1
        self.cont["tel"]["value"] = self.num
        self.data_layer.insert_contact(self.cont)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Create a call log.
        #
        self.dialer.launch()
        self.dialer.enterNumber(self.num)
        self.dialer.callThisNumber()
        time.sleep(2)
        self.dialer.hangUp()
         
        #
        # Open the call log and tap on this number.
        #
        self.dialer.openCallLog()
        
        x = self.UTILS.getElement( ("xpath", DOM.Dialer.call_log_number_xpath % self.num), "Number field for %s" % self.num)
        
        boolOK = False
        try:
            y = x.find_element("xpath", "//span[@class='primary-info-main' and contains(text(), '%s')]" % self.cont["name"])
            if y:
                boolOK = True
        except:
            pass
        
        self.UTILS.TEST(boolOK, "Contact name is displayed in call log.")
        
        self.UTILS.logResult("info", "Tapping this entry in the call log ...")
        
        x.tap()
        
        #
        # Verify that we are taken to view this contact.
        #
        self.UTILS.switchToFrame(*DOM.Dialer.call_log_contact_name_iframe, p_viaRootFrame=False)
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Contact view screenshot", x)
        
        self.UTILS.waitForElements( ("xpath", DOM.Dialer.call_log_number_cont_highlight % self.num),
                                   "Number %s highlighted" % self.num)
        