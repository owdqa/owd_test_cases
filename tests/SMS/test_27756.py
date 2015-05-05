#===============================================================================
# 27756: Send a new SMS using the option of reduced list of favourite contacts
#
# Pre-requisites:
# The favourite contacts list contains some value.
#
# Procedure:
# 1- Open SMS app
# 2- Introduce a valid sms text
# 3- Open the favourite Contact list window
# 4- Select a favourite contact
# 5- Press send button
#
# Expected results:
# The user sends a sms successfully
#===============================================================================

import time
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        # Import some contacts.
        # Set the one we'll match to have a valid phone number.
        self.contact_1 = MockContact(tel={"type": "Mobile",
                        "value": self.UTILS.general.get_config_variable("phone_number", "custom")})
        self.contact_2 = MockContact()
        self.contact_3 = MockContact(givenName="AAAAAAAAAAAAAAAALEX",
                                    familyName="SMITHXXXXXXXX",
                                    name="AAAAAAAAAAAAAAAALEX SMITHXXXXXXXX")
        self.contact_4 = MockContact(tel=[{"type": "Mobile 1", "carrier": "MoviStar1", "value": "444444444"},
                                    {"type": "Mobile 2", "carrier": "MoviStar2", "value": "555555555"},
                                    {"type": "Mobile 3", "carrier": "MoviStar3", "value": "666666666"}])
        self.contact_5 = MockContact(email=[{"type": "", "value": "email1@nowhere.com"},
                                    {"type": "", "value": "email2@nowhere.com"},
                                    {"type": "", "value": "email3@nowhere.com"}])

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
        self.test_msg = "Test message at {}".format(time.time())

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Launch messages app.
        self.messages.launch()

        # Type a message containing the required string
        self.messages.startNewSMS()
        self.messages.enterSMSMsg(self.test_msg)

        # Search for our contact in the favourites section.
        self.messages.selectAddContactButton()

        self.UTILS.reporting.debug("*** Looking for contact named {}".format(self.contact_1['givenName']))
        self.UTILS.iframe.switch_to_frame(*DOM.Contacts.frame_locator)
        cont = self.UTILS.element.getElement((DOM.Contacts.favourite_by_name[0],
                                             DOM.Contacts.favourite_by_name[1].format(self.contact_1['givenName'])),
                                             "Favourite contact", timeout=20)
        cont.tap()
        self.UTILS.iframe.switch_to_frame(*DOM.Messages.frame_locator)

        # Now check the correct name is in the 'To' list.
        self.messages.checkIsInToField(self.contact_1["name"])
        self.messages.sendSMS()
        send_time = self.messages.last_sent_message_timestamp()
        self.messages.wait_for_message(send_time=send_time)
        self.messages.check_last_message_contents(self.test_msg)
