from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(PixiTestCase):

    def setUp(self):
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)
        self.contact = MockContact(tel=[{'type': 'Mobile', 'value': '11111111'},
                                        {'type': 'Mobile', 'value': '222222222'}])

        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        self.messages.launch()

        # Type a message containing the required string
        self.messages.startNewSMS()
        self.messages.enterSMSMsg("Test message")

        # Search for our contact.
        self.messages.selectAddContactButton()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.contacts.search(self.contact['name'])
        self.contacts.select_search_result_several_phones(self.contact['name'], 0)
