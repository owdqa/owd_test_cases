#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")

from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        #
        # Get details of our test contacts.
        #
        self.contact = MockContact(tel={'type': 'Mobile', 'value': '123111111'})
        self.contact2 = MockContact(tel={'type': 'Mobile', 'value': '123222222'})

        #
        # Make sure we can find both of them with a search.
        #
        self.UTILS.general.insertContact(self.contact2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Store our picture on the device.
        #
        self.UTILS.general.addFileToDevice('./tests/_resources/contact_face.jpg', destination='DCIM/100MZLLA')

        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Create our contact.
        #
        self.contacts.create_contact(self.contact, "gallery")

        #
        # Verify our contact.
        #
        self.contacts.verify_image_in_all_contacts(self.contact['name'])

        #
        # Search for our contacts.
        #
        self.contacts.search("12")
        self.contacts.check_search_results(self.contact["givenName"])
        self.contacts.check_search_results(self.contact2["givenName"])

        #
        # Verify that the image is present for the right contact.
        #
        boolOK1 = False
        boolOK2 = True
        results_list = self.UTILS.element.getElements(DOM.Contacts.search_results_list, "Search results")

        for result in results_list:
            if result.get_attribute("data-order") == self.contact["name"].replace(" ", ""):
                # Contact 1
                try:
                    img = result.find_element("xpath", "//span[@data-type='img']")
                    if ("blob" in img.get_attribute("data-src")):
                        boolOK1 = True
                except:
                    self.UTILS.reporting.logResult("info", "No image present for contact {} | The image was indeed expected".format(result.text))

            elif result.get_attribute("data-order") == self.contact2["name"].replace(" ", ""):
                # Contact 2
                try:
                    img = result.find_element("xpath", "//span[@data-type='img']")
                    if not ("blob" in img.get_attribute("data-src")):
                        boolOK2 = False
                except:
                    self.UTILS.reporting.logResult("info", "No image present for contact {} | NO image expected".format(result.text))
                    boolOK2 = True
            else:
                self.UTILS.test.TEST(False, "This contact does not appear in the list: {}".format(result.text))

        self.UTILS.test.TEST(boolOK1, "Contact 1 has image displayed.")
        self.UTILS.test.TEST(boolOK2, "Contact 2 has no image displayed.")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of search results", x)
