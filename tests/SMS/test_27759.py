from gaiatest import GaiaTestCase

import time
from OWDTestToolkit import DOM
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        self.phone_number = self.UTILS.general.get_config_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact = MockContact(tel={'type': '', 'value': ''})
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        self.messages.launch()

        # Type a message containing the required string
        self.messages.startNewSMS()
        self.messages.enterSMSMsg("Test message")

        # Search for our contact.
        self.messages.selectAddContactButton()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        # Search the contacts list for our contact.
        contact_list = self.UTILS.element.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        for c in contact_list:
            if c.text == self.contact["name"]:
                self.UTILS.reporting.logResult("info", "Tapping ...")
                c.tap()
                break

        time.sleep(2)
        self.apps.switch_to_displayed_app()
        self.messages.checkIsInToField("", True)

        # self.UTILS.element.waitForElements(DOM.Messages.contact_no_phones_msg, "Message saying this contact has no phones")
        # x = self.UTILS.element.getElement(DOM.Messages.contact_no_phones_ok, "OK button")
        # x.tap()
        #
        # self.UTILS.element.headerCheck("Select contact")
