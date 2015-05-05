from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase

import time
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(SpreadtrumTestCase):

    def setUp(self):
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        # Prepare the contact we're going to insert.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.contact = MockContact(tel={'type': '', 'value': self.phone_number})

        self.UTILS.general.insertContact(self.contact)
        self.UTILS.reporting.logComment("Using target telephone number " + self.contact["tel"]["value"])

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        # Launch messages app.
        self.messages.launch()

        # Type a message containing the required string
        self.messages.startNewSMS()
        self.messages.enterSMSMsg("Test message")

        # Search for our contact.
        self.messages.selectAddContactButton()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.contacts.search(self.contact["name"])
        self.contacts.check_search_results(self.contact["name"])

        contact_list = self.UTILS.element.getElements(DOM.Contacts.search_results_list, "Contacts search results")
        for c in contact_list:
            if c.text == self.contact["name"]:
                c.tap()
                break

        # Switch back to the sms iframe.
        self.apps.switch_to_displayed_app()

        # Now check the correct name is in the 'To' list.
        self.messages.checkIsInToField(self.contact["name"])
        self.messages.sendSMS()
