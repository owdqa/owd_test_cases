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
        self.contact1 = MockContact(givenName = "Name 1", familyName = "Surname 1",name = "Name 1 Surname 1")
        self.UTILS.general.insertContact(self.contact1)
        self.contact2 = MockContact(givenName = "Name 2", familyName = "Surname 2",name = "Name 2 Surname 2")
        self.UTILS.general.insertContact(self.contact2)


    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        self.messages.launch()


        self.messages.startNewSMS()

        self.messages.addContactToField(self.contact1["name"])
        self.messages.addContactToField(self.contact2["name"])


        #
        # Remove it.
        #
        self.messages.removeContactFromToField(self.contact2["name"])

        #
        # Verify the contact name is present before removing it.
        #
        self.messages.checkIsInToField(self.contact2["name"], False)

        self.UTILS.reporting.logResult("info", "It is not the 'To' list.")