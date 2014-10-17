#===============================================================================
# 26865: Receive an SMS from a contact with long name
#
# 1. Receive an SMS from a contact with a long name
# 2. Go to SMS app
#
# Expected result: The SMS must be received and the name doesn't have to overlap
# the SMS text
#===============================================================================

import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from tests._mock_data.contacts import MockContact
import time


class test_main(GaiaTestCase):

    test_msg = "Test."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.messages = Messages(self)

        #
        # Prepare the contact we're going to insert.
        #
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact = MockContact(givenName='AAAAAAAAAAAAAAAALEX',
                                    familyName='SMITHXXXXXXXX',
                                    name='AAAAAAAAAAAAAAAALEX SMITHXXXXXXXX',
                                    tel={'type': 'Mobile', 'value': self.phone_number})

        self.UTILS.general.insertContact(self.contact)
        self.cp_incoming_number = self.UTILS.general.get_os_variable("GLOBAL_CP_NUMBER").split(',')
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.messages.launch()

        self.UTILS.messages.create_incoming_sms(self.contact["tel"]["value"], self.test_msg)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(self.test_msg, timeout=120)
        title = self.UTILS.statusbar.wait_for_notification_toaster_with_titles(self.cp_incoming_number, timeout=5)
        self.UTILS.statusbar.click_on_notification_title(title, DOM.Messages.frame_locator)

        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # View the details of our contact.
        #
        self.contacts.view_contact(self.contact['name'])

        #
        # Tap the sms button in the view details screen to go to the sms page.
        #
        smsBTN = self.UTILS.element.getElement(DOM.Contacts.sms_button, "Send SMS button")
        smsBTN.tap()

        time.sleep(2)
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

        self.messages.check_last_message_contents(self.test_msg)
