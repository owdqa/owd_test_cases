#
# 27735: Verify that If the name of the contact is not empty,
# no carrier information is linked to the phone, and
# phone number is shown instead of carrier as the secondary header.
#
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


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
        self.contact = MockContact(tel={'type': '', 'value': self.phone_number})

        self.UTILS.general.insertContact(self.contact)
        self.UTILS.reporting.logComment("Using target telephone number " + self.contact["tel"]["value"])
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
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
        self.marionette.switch_to_frame()
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

        #
        # Create SMS.
        #
        self.messages.enterSMSMsg(self.test_msg)

        #
        # Click send.
        #
        self.messages.sendSMS()
        send_time = self.messages.last_sent_message_timestamp()

        #
        # Wait for the last message in this thread to be a 'received' one.
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread(send_time=send_time)
        self.UTILS.test.test(returnedSMS, "A received message appeared in the thread.", True)
        self.messages.check_last_message_contents(self.test_msg)

        #
        # Examine the carrier.
        #
        expect = self.contact["tel"]["type"]
        actual = self.messages.threadType()
        self.UTILS.test.test(expect == actual, "The type is listed as: '{}' (subheader was '{}').".\
                             format(expect, actual))

        #
        # Phone Number is shown instead of carrier as the secondary header
        #
        expect = self.contact["tel"]["value"]
        actual = self.messages.threadCarrier()
        self.UTILS.test.test(expect == actual, "The telephone number is: '{}' (subheader was '{}').".\
                             format(expect, actual))
