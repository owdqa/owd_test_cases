#
# TC_MMSTC_COMPT_009b
# Recipient Name

from gaiatest import GaiaTestCase

from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.gallery import Gallery


class test_main(GaiaTestCase):

    test_msg = "Test."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)
        self.gallery = Gallery(self)

        #
        # Import contact (adjust to the correct number).
        #
        self.test_num = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.cont = MockContact(tel={"type": "Mobile", "value": self.test_num})
        self.UTILS.reporting.logComment("Using target telephone number " + self.cont["tel"]["value"])

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.general.add_file_to_device('./tests/_resources/imgd.jpg', destination='DCIM/100MZLLA')

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create a new SMS
        #
        self.messages.startNewSMS()

        #
        # Insert the phone number in the To field
        #
        self.messages.addNumbersInToField([self.test_num])

        #
        # Create MMS.
        #
        self.messages.enterSMSMsg(self.test_msg)

        self.messages.create_mms_image()
        self.gallery.click_on_thumbnail_at_position_mms(0)

        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()
        send_time = self.messages.last_sent_message_timestamp()

        #
        # Open contacts app and create a contact with the same phone number used to send the MMS in the
        # previous step
        #
        self.contacts.launch()
        self.contacts.create_contact(self.cont)

        #
        # Switch back to the messages app.
        #
        self.UTILS.home.goHome()
        self.messages.launch()

        #
        # Verify the thread now contains the name of the contact instead of the phone number
        #
        self.UTILS.reporting.logComment("Trying to open the thread with name: " + self.cont["name"])
        self.messages.openThread(self.cont["name"])
        self.messages.wait_for_message(send_time)
