#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from tests._mock_data.contacts import MockContact
import time

class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        #
        # Prepare the contact we're going to insert.
        #
        self.num1 = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact = MockContact(tel = {'type': '', 'value': self.num1})

        self.UTILS.general.insertContact(self.contact)
        self.UTILS.reporting.logComment("Using target telephone number " + self.contact["tel"]["value"])

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Type a message containing the required string 
        #
        self.messages.startNewSMS()
        self.messages.enterSMSMsg("Test message")

        #
        # Search for our contact.
        #
        orig_iframe = self.messages.selectAddContactButton()
        self.contacts.search(self.contact["name"])
        self.contacts.check_search_results(self.contact["name"])

        x = self.UTILS.element.getElements(DOM.Contacts.search_results_list, "Contacts search results")
        for i in x:
            if i.text == self.contact["name"]:
                i.tap()
                break

        #
        # Switch back to the sms iframe.
        #
        self.marionette.switch_to_frame()
        self.UTILS.iframe.switchToFrame("src",orig_iframe)

        #
        # Now check the correct name is in the 'To' list.
        #
        self.messages.checkIsInToField(self.contact["name"])
        self.messages.sendSMS()

        #
        # Receiving the message is not part of the test, so just wait a 
        # few seconds for the returned sms in case it messes up the next test.
        #
        time.sleep(5)
