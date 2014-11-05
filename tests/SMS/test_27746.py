#
# 27746: Verify that If the name of the contact is not empty, the type of the
# phone and the phone carrier (as defined in the address book) as the secondary
# header
#
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        #
        # Prepare the contact we're going to insert.
        #
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact = MockContact(tel={'type': '', 'value': self.phone_number})

        self.UTILS.general.insertContact(self.contact)
        self.UTILS.reporting.logComment("Using target telephone number " + self.contact["tel"]["value"])

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Send a message to create a thread (use number, not name as this
        # avoids some blocking bugs just now).
        #
        self.messages.createAndSendSMS([self.contact["tel"]["value"]],
                                        "Test message.")
        send_time = self.messages.last_sent_message_timestamp()
        self.messages.waitForReceivedMsgInThisThread(send_time=send_time)

        #
        # Examine the carrier.
        #
        expect = self.contact["tel"]["type"]
        actual = self.messages.threadType()
        self.UTILS.test.test(expect == actual, "The type is listed as: '{}' (subheader was '{}').".\
                             format(expect, actual))

        expect = self.contact["tel"]["value"]
        actual = self.messages.threadCarrier()
        self.UTILS.test.test(expect == actual, "The carrier is listed as: '{}' (subheader was '{}').".\
                             format(expect, actual))
