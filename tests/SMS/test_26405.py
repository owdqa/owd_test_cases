#===============================================================================
# 26405: Press cancel button in the screen to select a contact phone number
#
# Procedure:
# 1- Open sms app
# 2- Press new sms button
# 3- Press select contact button
# 4- Select a contact with 2 phone numbers
# ER1
# Press cancel button
# ER2
#
# Expected results:
# ER1 User accesses to selection of contact phone number
# ER2 User exits the selection of contact phone number and no phone number
# is added
#===============================================================================

from gaiatest import GaiaTestCase

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
        self.contact = MockContact(tel=[{'type': 'Mobile', 'value': '111111111'},
                                        {'type': 'Mobile', 'value': '222222222'}])

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
        self.contacts.search(self.contact['name'])
        self.contacts.select_search_result_several_phones(self.contact['name'],
                                                          self.contact['tel'][0]['value'], cancel=True)
