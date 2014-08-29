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
        # Import some contacts.
        #
        # Set the one we'll match to have a valid phone number.
        self.contact_1 = MockContact(tel={"type": "Mobile",
                        "value": self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")})
        self.contact_2 = MockContact()
        self.contact_3 = MockContact(givenName="AAAAAAAAAAAAAAAALEX",
                                    familyName="SMITHXXXXXXXX",
                                    name="AAAAAAAAAAAAAAAALEX SMITHXXXXXXXX")
        self.contact_4 = MockContact(tel=[{"type": "Mobile 1", "carrier": "MoviStar1", "value": "444444444"},
                                    {"type": "Mobile 2", "carrier": "MoviStar2", "value": "555555555"},
                                    {"type": "Mobile 3", "carrier": "MoviStar3", "value": "666666666"}])
        self.contact_5 = MockContact([{"type": "", "value": "email1@nowhere.com"},
                                    {"type": "", "value": "email2@nowhere.com"},
                                    {"type": "", "value": "email3@nowhere.com"})])


        # Set a couple of them to be favorites (including the one we'll use).
        self.contact_1["category"] = "favorite"
        self.contact_2["category"] = "favorite"

        # Insert all the contacts.
        self.UTILS.general.insertContact(self.contact_1)
        self.UTILS.general.insertContact(self.contact_2)
        self.UTILS.general.insertContact(self.contact_3)
        self.UTILS.general.insertContact(self.contact_4)
        self.UTILS.general.insertContact(self.contact_5)

        self.UTILS.reporting.logComment("Using target telephone number " + self.contact_1["tel"]["value"])

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

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
        # Search for our contact in the favourites section.
        #
        orig_iframe = self.messages.selectAddContactButton()

        x = self.UTILS.element.getElement(DOM.Contacts.favourite_JS,
                                  "'" + self.contact_1['name'] + "' in the favourites section")
        x.tap()

        #
        # Switch back to the sms iframe.
        #
        self.marionette.switch_to_frame()
        self.UTILS.iframe.switchToFrame("src",orig_iframe)

        #
        # Now check the correct name is in the 'To' list.
        #
        self.messages.checkIsInToField(self.contact_1["name"])
        self.messages.sendSMS()

        #
        # Receiving the message is not part of the test, so just wait a 
        # few seconds for the returned sms in case it messes up the next test.
        #
        time.sleep(5)
