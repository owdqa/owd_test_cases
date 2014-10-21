#===============================================================================
# 27753: Delete a contact and verify that the SMS list now shows the number
#
# Procedure:
# 1- Send a sms to our device from phone number who is a contact
# 2- Open SMS app
# ER1
# 3- delete the contact name who sended the last sms
# 4- Open SMS app
# ER2
#
# Expected results:
# ER1- verify that the SMS list shows the name
# ER2- verify that the SMS list now shows the phone number
#===============================================================================

from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

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
        self.contact = MockContact(tel={'type': '', 'value': self.phone_number})
        self.test_msg = "Test."

        self.UTILS.general.insertContact(self.contact)
        self.UTILS.reporting.logComment("Using target telephone number " + self.contact["tel"]["value"])
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        msgapp = self.messages.launch()
        self.messages.createAndSendSMS([self.phone_number], "Test")
        send_time = self.messages.last_sent_message_timestamp()
        self.messages.waitForReceivedMsgInThisThread(send_time=send_time)

        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        self.messages.openThread(self.contact["name"])

        #
        # Delete the contact
        #
        self.apps.kill(msgapp)
        self.contacts.launch()
        self.contacts.delete_contact(self.contact["name"])

        #
        # Go back to SMS app and try to open the thread by phone number
        #
        self.messages.launch()
        self.messages.openThread(self.contact["tel"]["value"])
