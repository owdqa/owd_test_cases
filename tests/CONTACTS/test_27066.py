#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")

from gaiatest import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContacts

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
        self.cont1 = MockContacts().Contact_1
        self.cont2 = MockContacts().Contact_2

        #        
        # Make sure we can find both of them with a search.
        #
        self.cont1["tel"]["value"] = "123111111"
        self.cont2["tel"]["value"] = "123222222"
        
        self.data_layer.insert_contact(self.cont2)
        
        
    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
    
        #
        # Store our picture on the device.
        #
        self.UTILS.addFileToDevice('./tests/_resources/contact_face.jpg', destination='DCIM/100MZLLA')
        
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # Create our contact.
        #
        self.contacts.createNewContact(self.cont1,"gallery")
        
        #
        # Verify our contact.
        #
        self.contacts.verifyImageInAllContacts(self.cont1['name'])
        
        #
        # Search for our contacts.
        #
        self.contacts.search("12")
        self.contacts.checkSearchResults(self.cont1["givenName"])
        self.contacts.checkSearchResults(self.cont2["givenName"])
        
        #
        # Verify that the image is present for the right contact.
        #
        boolOK1 = False
        boolOK2 = True
        x = self.UTILS.getElements(DOM.Contacts.search_results_list, "Search results")
        for i in x:
            # Contact 1 (HAS an image).
            try:
                x = i.find_element("xpath", ".//p[contains(@data-search, '%s')]" % self.cont1["name"])
                if x:
                    try:
                        x = i.find_element("xpath", ".//img")
                        if x:
                            boolOK1 = True
                            break
                    except:
                        pass  
            except:
                pass
                
            # Contact 2 (Does NOT have an image).
            try:
                x = i.find_element("xpath", ".//p[contains(@data-search, '%s')]" % self.cont2["name"])
                if x:
                    try:
                        x = i.find_element("xpath", ".//img")
                        if x:
                            boolOK2 = False
                            break
                    except:
                        pass  
            except:
                pass
                
        self.UTILS.TEST(boolOK1, "Contact 1 has image displayed.")
        self.UTILS.TEST(boolOK2, "Contact 2 has no image displayed.")        
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of search results", x)
        