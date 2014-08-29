#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from tests._mock_data.contacts import MockContact

class test_main(GaiaTestCase):

   #
    # Restart device to starting with wifi and 3g disabled.
    #
    _RESTART_DEVICE = True


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

        #
        # Import contact (adjust to the correct number).
        #
        self.test_num = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact1 = MockContact(givenName = "Name 1", familyName = "Surname 1",name = "Name 1 Surname 1", tel={"type": "Mobile", "value": self.test_num})
        self.UTILS.reporting.logComment("Using target telephone number " + self.contact1["tel"]["value"])
        self.UTILS.general.insertContact(self.contact1)

        self.contact2 = MockContact(givenName = "Name 2", familyName = "Surname 2",name = "Name 2 Surname 2")
        self.UTILS.general.insertContact(self.contact2)

        #
        # Establish which phone number to use.
        #
        self.num2 = "646816713"
        #self.num2 = self.UTILS.general.get_os_variable("GLOBAL_WP_NUMBER")


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
        self.messages.addNumbersInToField([self.num2])


        #
        # Enter the message.
        #
        self.UTILS.reporting.logResult("info", "Enter the message.")
        self.messages.enterSMSMsg("Test 29911")

        #
        # Send the message.
        #
        self.messages.sendSMS()
        self.UTILS.reporting.logResult("info","Send the message.")

        #
        # Verify the number is shown in the header as there is no contact name
        #
        self.messages.openThread(self.num2)
        self.messages.checkThreadHeader(self.num2)

        self.UTILS.reporting.logResult("info", "Verify the number is shown in the header as there is no contact name")

         #
        # Return to main SMS page.
        #
        self.messages.closeThread()

         #
        # Verify the thread now contains the name of the contact instead of the phone number
        #
        self.UTILS.reporting.logResult("info","Trying to open the thread with name: " + self.contact1["name"])
        self.messages.openThread(self.contact1["name"])
        self.messages.checkThreadHeaderWithNameSurname(self.contact1["name"])
        self.UTILS.reporting.logResult("info", "Test correctly finished")