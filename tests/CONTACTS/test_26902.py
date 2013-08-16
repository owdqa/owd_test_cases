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
 
        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContacts().Contact_1
        self.data_layer.insert_contact(self.Contact_1)
        self.UTILS.addFileToDevice('./tests/_resources/contact_face.jpg', destination='DCIM/100MZLLA')
          
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):

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
            self.marionette.execute_script("document.getElementById('%s').scrollIntoView();" % "thumbnail-action")
            self.marionette.execute_script("document.getElementById('contact-form-title').scrollIntoView();")
        except:
            pass
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point:", x)
        
        self.UTILS.checkMarionetteOK()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        x = self.UTILS.getElement(DOM.Contacts.edit_image, "Image")
        self.UTILS.TEST("removed" not in x.get_attribute("class"), "The item is NOT marked as temporarily removed.")
        
        #
        # Toggle the 'reset' icon.
        #
        x = self.UTILS.getElement(("xpath",DOM.Contacts.reset_field_xpath % "thumbnail-action"), "Photo reset button")
        x.tap()
          
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point:", x)
        
        x = self.UTILS.getElement(DOM.Contacts.edit_image, "Image")
        self.UTILS.TEST("removed" in x.get_attribute("class"), "The item IS marked as temporarily removed.")
        
        x = self.UTILS.getElement(("xpath",DOM.Contacts.reset_field_xpath % "thumbnail-action"), "Photo reset button")
        x.tap()
          
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point:", x)
        
        x = self.UTILS.getElement(DOM.Contacts.edit_image, "Image")
        self.UTILS.TEST("removed" not in x.get_attribute("class"), "The item is NOT marked as temporarily removed.")
        
        
        