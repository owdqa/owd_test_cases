#===============================================================================
# 27066: Type a number to look for a contact which has picture
#
# Pre-requisites
# To have some contacts from SIM, facebook, gmail or hotmail with picture
#
# Procedure:
# 1. Open Contacts app
# 2. Tap on Search box
# 3. Insert a phone number which matches with a contact with picture number
#
# Expected Result:
# Contacts with picture also appear on the list shown when looking for
# contacts by phone number
#===============================================================================

from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        self.contact = MockContact(tel={'type': 'Mobile', 'value': '123111111'})
        self.contact2 = MockContact(tel={'type': 'Mobile', 'value': '123222222'})

        self.UTILS.general.insertContact(self.contact2)

    def tearDown(self):
        self.UTILS.general.remove_files()
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        # Store our picture on the device.
        self.UTILS.general.add_file_to_device('./tests/_resources/contact_face.jpg')

        # Create and verify contact
        self.contacts.launch()
        self.contacts.create_contact(self.contact, "gallery")
        self.contacts.verify_image_in_all_contacts(self.contact['name'])

        # Search for our contacts.
        self.contacts.search("test")
        self.contacts.check_search_results(self.contact["givenName"])
        self.contacts.check_search_results(self.contact2["givenName"])

        # Verify that the image is present for the right contact.
        results_list = self.UTILS.element.getElements(DOM.Contacts.search_results_list, "Search results")
        tuples = zip(results_list, [self.contact, self.contact2], [True, False])
        for t in tuples:
            ok = self.verify_img_for_contact(t[0], t[1], t[2])
            self.UTILS.test.test(ok, "Image was {}found (Expected: {})".format("" if ok else "not ", t[2]))

        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of search results", screenshot)

    def verify_img_for_contact(self, result, contact, expect_image):
        """Verify if an image is present for the result list item.

        The result item must be the specified by contact.
        Return True if the contact has a image and expected_image is True.
        False otherwise.
        """
        found = False
        if result.get_attribute("data-order") == contact["name"].replace(" ", "").upper():
            try:
                img = result.find_element("css selector", "li.contact-item[data-order*='{}'] span[data-type=img]".\
                                          format(contact['givenName']))
                if "blob" in img.get_attribute("data-src"):
                    found = True
            except:
                self.UTILS.reporting.logResult("info", "No image present for contact {} |"\
                                               " The image was indeed expected".format(result.text))
        else:
            self.UTILS.test.test(False, "This contact does not appear in the list: {}".format(result.text))
        res = found == expect_image
        return res
