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
from tests.mock_data.contacts import MockContacts
import time

class test_19181(GaiaTestCase):
    _Description = "[CONTACTS] Remove a photo,a phone number, an email, an address and a comment from a contact and restore the phone number and the comment."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
 
        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContacts().Contact_1
        self.data_layer.insert_contact(self.Contact_1)
        self.UTILS.addFileToDevice('./tests/resources/contact_face.jpg', destination='DCIM/100MZLLA')
          
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):

        #
        # Launch contacts app.
        #
        self.UTILS.logResult("info", "Setting up contact ...")
        self.contacts.launch()
        
        #
        # View our contact.
        #
        self.contacts.viewContact(self.Contact_1['name'])
          
        #
        # Edit our contact.
        #
        self.contacts.pressEditContactButton()
           
        self.UTILS.logResult("info", "Starting tests ...")
         
        self.check_Field(True , "phone"    , "number_0"         , "number")
        self.check_Field(True , "email"    , "email_0"          , "email")
        self.check_Field(True , "address"  , "streetAddress_0"  , "streetAddress")
        self.check_Field(True , "comment"  , "note_0"           , "note")
         
        # NOTE: for some reason the photo has to tested alone or it screws up the text tests.
        self.contacts.pressCancelEditButton()
        self.contacts.pressEditContactButton()
        self.contacts.addGalleryImageToContact(0)
        self.check_Field(False, "photo", "thumbnail-action")

    def check_Field(self, p_text, p_fieldName, p_fieldId, p_resetBtnName=""):
        #
        # Test a text field: default, with reset enabled, with reset disabled.
        #
        
        #
        # try to make sure the field is in view (pretty hideous, but it does the job!).
        #
        try:
            self.marionette.execute_script("document.getElementById('" + p_fieldId + "').scrollIntoView();")
            self.marionette.execute_script("document.getElementById('contact-form-title').scrollIntoView();")
        except:
            pass
        
        self.UTILS.logResult("info", " ")
        self.UTILS.logResult("info", "*** '" + p_fieldName + "': default (before testing 'reset' mode) ... ***")
        self.check_kbd_appears(p_resetBtnName, p_fieldName, True) if p_text else self.check_photo_tap(True)
        
        self.UTILS.logResult("info", " ")
        self.UTILS.logResult("info", "*** '" + p_fieldName + "': switching 'reset' mode ON ... ***")
        self.toggle_reset_button(p_fieldName)
        self.check_kbd_appears(p_resetBtnName, p_fieldName, False) if p_text else self.check_photo_tap(False)
        
        self.UTILS.logResult("info", " ")
        self.UTILS.logResult("info", "*** '" + p_fieldName + "': switching 'reset' mode OFF ... ***")
        self.toggle_reset_button(p_fieldName)
        self.check_kbd_appears(p_resetBtnName, p_fieldName, True) if p_text else self.check_photo_tap(True)

        self.UTILS.logResult("info", " ")

        
    def toggle_reset_button(self, p_el):
        #
        # Press reset button on the required fields ...
        #
        reset_btn = DOM.Contacts.reset_field_xpath
        
        if p_el == "photo":
            x = self.UTILS.getElement(("xpath",reset_btn % "thumbnail-action"), "Photo reset button")
            x.tap()
          
        if p_el == "phone":
            x = self.UTILS.getElement(("xpath",reset_btn % "add-phone-0"), "Phone reset button")
            x.tap()
          
        if p_el == "email":
            x = self.UTILS.getElement(("xpath",reset_btn % "add-email-0"), "Email reset button")
            x.tap()
           
        if p_el == "address":
            x = self.UTILS.getElement(("xpath",reset_btn % "add-address-0"), "Address reset button")
            x.tap()
           
        if p_el == "comment":
            x = self.UTILS.getElement(("xpath",reset_btn % "add-note-0"), "Comment reset button")
            x.tap()
        
    def check_photo_tap(self, p_boolEditable):
        time.sleep(1)
        
        # Check tapping photo (same link for add and edit)
        _comment = "Photo is " + ("not " if not p_boolEditable else "")
        x = self.UTILS.getElement(DOM.Contacts.add_photo, "Photo")
        x.tap()
        time.sleep(1)
             
        self.marionette.switch_to_frame()
             
        boolED=False
        try:
            x = self.marionette.find_element(*DOM.Contacts.photo_from_gallery)
            x = self.marionette.find_element(*DOM.Contacts.cancel_photo_source)
            x.tap()
            boolED = True
        except:
            boolED=False
        self.UTILS.TEST(boolED == p_boolEditable, _comment + "editable.")
            
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

        
    def check_kbd_appears(self, p_elItem, p_desc, p_KBD_displayed):
        time.sleep(1)
        #
        # Taps the field and checks to see if the keyboard appears.
        # When marionette "is_enabled()" is working , we can forget all this.
        #
        _comment = "The " + p_desc + " field can " + ("not " if not p_KBD_displayed else "") + "be edited."

        x = self.UTILS.getElement(("id", "%s_0" % p_elItem), "Field for " + p_desc)
    
        # ROY - from here on does the keyboard verification .....
        # The problem is that the keyboard frame is always present
        # once it's been launched, so I need a way to either KILL
        # the keyboard, or see what's currently displayed.
        x.click()
        
        boolKBD=False
        self.marionette.switch_to_frame()
        x = self.marionette.find_element("xpath", 
                                         "//iframe[@" + DOM.GLOBAL.keyboard_iframe[0]+ \
                                         "='" + DOM.GLOBAL.keyboard_iframe[1] + "']")
        if x.is_displayed():
            boolKBD = True
        else:
            boolKBD=False
        self.UTILS.TEST(boolKBD == p_KBD_displayed, _comment)
         
        #
        # Return to the contacts iframe.
        #
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
         
        #
        # Tap the header to remove the keyboard.
        #
        x = self.marionette.find_element(*DOM.GLOBAL.app_head)
        x.click()
        
        
        
        
