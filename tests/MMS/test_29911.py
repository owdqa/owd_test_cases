#===============================================================================
# 29911: All recipients are shown fine (recipients are contacts and
# numbers entered manually) in the sms thread
#
# Pre-requisites:
# Import several contacts into the addressbook from different sources.
#
# Procedure:
# 1. Open SMS app
# 2. Tap on new to create a new MMS(attach a file)
# 3. Tap on '+' icon to add a recipient. Repeat this step several times
# selecting contacts from different sources. (ER1)
# 4. Tap on To field and add a number manually
# 5. Write something and send the sms
# 6. Open the sms thread then tap on the header (ER2)
#
# Expected results:
# ER1. All contacts are added correctly into the 'To' field
# ER2. The header shows the number of recipients.
# Each recipient is shown correctly with his name and surname, phone number
# and type, picture.
# Numbers of recipients not stored as contacts are shown ok too.
#===============================================================================

import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        #
        # Import contact (adjust to the correct number).
        #
        self.test_num = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact1 = MockContact(givenName="Name 1", familyName="Surname 1",
                                    name="Name 1 Surname 1", tel={"type": "Mobile", "value": self.test_num})
        self.UTILS.reporting.logComment("Using target telephone number " + self.contact1["tel"]["value"])
        self.UTILS.general.insertContact(self.contact1)

        self.contact2 = MockContact(givenName="Name 2", familyName="Surname 2", name="Name 2 Surname 2",
                                    tel={"type": "Mobile", "value": self.test_num})
        self.UTILS.general.insertContact(self.contact2)
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        self.call_number = self.UTILS.general.get_os_variable("TARGET_CALL_NUMBER")
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.messages.launch()

        self.messages.startNewSMS()

        self.messages.addContactToField(self.contact1["name"])
        self.messages.addContactToField(self.contact2["name"])

        #
        # Insert the phone number in the To field
        #
        self.messages.addNumbersInToField([self.call_number])

        #
        # Enter the message.
        #
        self.UTILS.reporting.logResult("info", "Enter the message.")
        self.messages.enterSMSMsg("Test 29911")

        #
        # Send the message.
        #
        self.messages.sendSMS()
        self.UTILS.reporting.logResult("info", "Send the message.")

        #
        # Verify the number is shown in the header as there is no contact name
        #
        self.messages.openThread(self.call_number)
        self.messages.checkThreadHeader(self.call_number)

        self.UTILS.reporting.logResult("info", "Verify the number is shown in the header as there is no contact name")

        #
        # Return to main SMS page.
        #
        self.messages.closeThread()

        #
        # Verify the thread now contains the name of the contact instead of the phone number
        #
        self.UTILS.reporting.logResult("info", "Trying to open the thread with name: " + self.contact1["name"])
        self.messages.openThread(self.contact1["name"])
        self.messages.checkThreadHeaderWithNameSurname(self.contact1["name"])
