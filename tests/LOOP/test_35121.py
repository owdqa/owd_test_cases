#===============================================================================
# 35121: Verify that, if the selected contact has no e-mail or phone number the
# option video and audio call are not present
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.loop import Loop


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.loop = Loop(self)
        #
        # Get details of our test contacts.
        #
        self.contact = MockContact()
        self.contact['tel'] = None
        self.contact['email'] = None
        self.UTILS.general.insertContact(self.contact)
        self.data_layer.connect_to_wifi()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        self.contacts.view_contact(self.contact['name'])
        self.wait_for_element_not_present(DOM.Contacts.view_contact_hello_option[0],
                                                 DOM.Contacts.view_contact_hello_option[1].format("audio"), timeout=5)
        self.UTILS.reporting.info("No audio call button present, as expected")
        self.wait_for_element_not_present(DOM.Contacts.view_contact_hello_option[0],
                                                 DOM.Contacts.view_contact_hello_option[1].format("video"), timeout=5)
        self.UTILS.reporting.info("No video call button present, as expected")
