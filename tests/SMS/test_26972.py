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
    
    _TestMsg     = "Test message."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.contacts   = Contacts(self)
        self.email      = Email(self)
        
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.emailAddy  = self.UTILS.get_os_variable("GMAIL_1_EMAIL")
        self.emailE     = self.UTILS.get_os_variable("GMAIL_2_EMAIL")
        self.emailP     = self.UTILS.get_os_variable("GMAIL_2_PASS")
        self.emailU     = self.UTILS.get_os_variable("GMAIL_2_USER")
        
        self.UTILS.addFileToDevice('./tests/_resources/contact_face.jpg', destination='DCIM/100MZLLA')
        
        self.cont = MockContact()
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.UTILS.getNetworkConnection()
        
        self.email.launch()
        self.email.setupAccount(self.emailU, self.emailE, self.emailP)
    
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
        self.messages.createAndSendSMS([self.num1], "Hello " + self.emailAddy + " old bean.")
        x = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Long press the email link.
        #
        _link = x.find_element("tag name", "a")
        _link.tap()
        
        #
        # Click 'create new contact'.
        #
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        x = self.UTILS.getElement( ("xpath", "//button[text()='Create new contact']"),
                                   "Create new contact button")
        x.tap()
        
        #
        # Verify that the email is in the email field.
        #
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        x = self.UTILS.getElement(DOM.Contacts.email_field, "Email field")
        x_txt = x.get_attribute("value")
        self.UTILS.TEST(x_txt == self.emailAddy, "Email is '" + self.emailAddy + "' (it was '" + x_txt + "')")
        
        #
        # Fill out all the other details.
        #
        
        #
        # Put the contact details into each of the fields (this method
        # clears each field first).
        #
        self._changeField('givenName'   , self.cont["givenName"])
        self._changeField('familyName'  , self.cont["familyName"])
        self._changeField('tel'         , self.cont["tel"]["value"])
        self._changeField('street'      , self.cont["adr"]["streetAddress"])
        self._changeField('zip'         , self.cont["adr"]["postalCode"])
        self._changeField('city'        , self.cont["adr"]["locality"])
        self._changeField('country'     , self.cont["adr"]["countryName"])
        self.contacts.addGalleryImageToContact(0)

        #
        # Check the fields have been updated correctly.
        #

        #
        # Add another email address.
        #
        self.contacts.addAnotherEmailAddress(self.cont["email"]["value"])
        
        #
        # Press the Done button.
        #
        done_button = self.UTILS.getElement(DOM.Contacts.done_button, "'Done' button")
        done_button.tap()

        #
        # Check that the contacts iframe is now gone.
        #
        self.marionette.switch_to_frame()
        self.UTILS.waitForNotElements( ("xpath", "//iframe[contains(@src,'contacts')]"),
                                       "Contact app iframe")
        
        #
        # Now return to the SMS app.
        #
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        

    def _changeField(self, p_field, p_valObj):
        #
        # To try and get around marionette issues I'm resetting Marionette every time here.
        #
        self.UTILS.checkMarionetteOK()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        contFields = self.contacts.getContactFields()
        self.contacts.replaceStr(contFields[p_field] , p_valObj)
