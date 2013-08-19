#
# Runs through composing and sending an email as one user, then
# receiving it as another user.
#
# As I can't see ANY different between read and unread emails in the html,
# I need to rely on a totally unique subject line to identify the precise
# message sent between the two test accounts.
#

#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from marionette import Marionette
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *
#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContacts
import time

class main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)


    def tearDown(self):
        self.UTILS.reportResults()

    def field_remove_toggle_test(self, p_field_definition):
        #
        # Imports a contact, goes to the contact, edits it and tests the required 'remove' icon
        # (on and then off).
        #
        
        _del_icon_locator   = ("xpath",DOM.Contacts.reset_field_xpath % p_field_definition)
        
        if p_field_definition == "thumbnail-action":
            #
            # The thumbnail is different from the rest.
            #
            _field_locator      = DOM.Contacts.edit_image
        else:
            _field_locator      = ("xpath", "//div[@id='%s']/div" % p_field_definition)
        
        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContacts().Contact_1
        self.data_layer.insert_contact(self.Contact_1)
        self.UTILS.addFileToDevice('./tests/_resources/contact_face.jpg', destination='DCIM/100MZLLA')
          
        self.UTILS.logResult("info", "Setting up contact ...")
        self.contacts.launch()
        self.contacts.viewContact(self.Contact_1['name'])
        self.contacts.pressEditContactButton()
        self.contacts.addGalleryImageToContact(0)
           
        self.UTILS.logResult("info", "Starting tests ...")
         
        #
        # try to make sure the field is in view (pretty hideous, but it does the job!).
        #
        try:
            self.marionette.execute_script("document.getElementById('%s').scrollIntoView();" % p_field_definition)
            self.marionette.execute_script("document.getElementById('contact-form-title').scrollIntoView();")
        except:
            pass
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point:", x)
        
        self.UTILS.checkMarionetteOK()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        
        
        x = self.UTILS.getElement(_field_locator, "Field being tested")
        self.UTILS.TEST("removed" not in x.get_attribute("class"), "The item is NOT marked as temporarily removed.")
        
        
        #
        # Toggle the 'reset' icon.
        #
        x = self.UTILS.getElement(_del_icon_locator, "Field reset button")
        x.tap()
          
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point:", x)
        
        x = self.UTILS.getElement(_field_locator, "Field being tested")
        self.UTILS.TEST("removed" in x.get_attribute("class"), "The item IS marked as temporarily removed.")
        
        x = self.UTILS.getElement(_del_icon_locator, "Field reset button")
        x.tap()
          
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point:", x)
        
        x = self.UTILS.getElement(_field_locator, "Field being tested")
        self.UTILS.TEST("removed" not in x.get_attribute("class"), "The item is NOT marked as temporarily removed.")
        
        
        
