#===============================================================================
# 29909: Verify that the name of one recipient is shown correctly
# in 'To' field (Contact saved with name and surname)
#
# Pre-requisites:
# At least one contact saved with name and last name
#
# Procedure:
# 1. Open SMS app
# 2. Tap on new to create a new MMS(attach a file)
# 3. Tap on '+' icon to add a recipient (ER1)
# 4. Select a contact which has name and last name by tapping on
# it (ER2)
#
# Expected results:
# ER1. When tapping on '+' the contact list is shown. It is possible
# to select any contact
# ER2. The contact is added into the 'To' field. The name is shown fine
# on that field
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        # Prepare the contact we're going to insert.
        self.contact = MockContact(givenName="Name", familyName="Surname", name="Name Surname")
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        self.messages.launch()

        self.messages.startNewSMS()

        self.messages.addContactToField(self.contact["name"])

        self.UTILS.reporting.logResult("info", "Correct name is in the 'To' list.")
