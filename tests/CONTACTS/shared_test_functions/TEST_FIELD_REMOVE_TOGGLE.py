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
import time


class main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)

    def tearDown(self):
        self.UTILS.reportResults()

    def field_remove_toggle_test(self, p_contact_json_obj, p_field_definition, p_item_nums=[0]):
        #
        # Imports a contact, goes to the contact, edits it and tests the required 'remove' icon
        # (on and then off).
        # p_field_num: The number of the item, for example if there's >1 phone number, then '0' would
        # be the first one etc... (defaults to zero in case there's only one item).
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
        self.UTILS.logResult("info", "Setting up contact ...")
        self.UTILS.insertContact(p_contact_json_obj)
        
        # Add image.
        self.UTILS.addFileToDevice('./tests/_resources/contact_face.jpg', destination='DCIM/100MZLLA')
        self.contacts.launch()
        self.contacts.viewContact(p_contact_json_obj['name'])
        self.contacts.pressEditContactButton()
        self.contacts.addGalleryImageToContact(0)
           
        self.UTILS.logResult("info", "Starting tests ...")
         
        #
        # Try to make sure this field section is in view (pretty hideous, but it does the job!).
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

        self.UTILS.logResult("info", "<b>For each of our items for this field, click the icon to set them to 'remove' ...</b>")
        for i in p_item_nums:
            x = self.UTILS.getElements(_field_locator, "Field being tested (item %s)" % i)[i]
            self.UTILS.TEST("removed" not in x.get_attribute("class"), "The item is NOT marked as temporarily removed.")
                        
            x = self.UTILS.getElements(_del_icon_locator, "Field reset button (item %s)" % i)[i]
            x.tap()
              
            x = self.UTILS.screenShotOnErr()
            self.UTILS.logResult("info", "Screenshot at this point:", x)
            
            x = self.UTILS.getElements(_field_locator, "Field being tested (item %s)" % i)[i]
            self.UTILS.TEST("removed" in x.get_attribute("class"), "The item IS now marked as temporarily removed.")

        self.UTILS.logResult("info", "<b>For each of our items for this field, click the icon to turn off 'remove' ...</b>")
        for i in p_item_nums:
            x = self.UTILS.getElements(_del_icon_locator, "Field reset button (item %s)" % i)[i]
            x.tap()
              
            x = self.UTILS.screenShotOnErr()
            self.UTILS.logResult("info", "Screenshot at this point:", x)
            
            x = self.UTILS.getElements(_field_locator, "Field being tested (item %s)" % i)[i]
            self.UTILS.TEST("removed" not in x.get_attribute("class"), "The item is now NOT marked as temporarily removed.")