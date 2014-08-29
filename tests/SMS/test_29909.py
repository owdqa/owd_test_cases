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
        self.contact = MockContact(givenName = "Name", familyName = "Surname",name = "Name Surname")

        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        self.messages.launch()

        self.messages.startNewSMS()

        self.messages.addContactToField(self.contact["name"])

        self.UTILS.reporting.logResult("info", "Correct name is in the 'To' list.")

