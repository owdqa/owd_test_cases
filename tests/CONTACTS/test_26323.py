from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(SpreadtrumTestCase):

    def setUp(self):
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        self.test_contact = MockContact()
        self.UTILS.general.add_file_to_device('./tests/_resources/contact_face.jpg')

    def tearDown(self):
        self.UTILS.general.remove_files()
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        self.contacts.create_contact(self.test_contact, "gallery")

        self.contacts.verify_image_in_all_contacts(self.test_contact['name'])
        self.contacts.check_view_contact_details(self.test_contact, True)
