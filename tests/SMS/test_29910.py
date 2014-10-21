#===============================================================================
# 29910: Remove a recipient (contact) from the 'To' field (n recipients)
#
# Pre-requisites:
# There are already several recipients into the 'To' field
#
# Procedure:
# 1. Open SMS app
# 2. Tap on new to create a new MMS(attach a file)
# 3. Tap on '+' icon to add a recipient (ER1)
# 4. Select a contact from the contacts list
# 5. Repeat these steps to add several contacts (>2) (ER2)
# 6. Once the contacts are into the 'To' field, tap on one of them (ER3)
# 7. Tap on Remove options (ER4)
#
# Expected results:
# ER1. The contact list is shown
# ER2. Several contacts are added successfully into 'To' field
# ER3. When tapping on a recipient, the recipient options screen is shown
# with the correct options and labels
# ER4. User is taken back to sms composer. Recipient has been removed successfully
#===============================================================================

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
        self.contacts = []
        for i in range(3):
            given_name = "Name {}".format(i)
            family_name = "Surname {}".format(i)
            contact = MockContact(givenName=given_name, familyName=family_name,
                                       name="{} {}".format(given_name, family_name))
            self.contacts.append(contact)
            self.UTILS.general.insertContact(contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        self.messages.launch()

        self.messages.startNewSMS()

        for c in self.contacts:
            self.messages.addContactToField(c["name"])

        #
        # Remove it.
        #
        self.messages.removeContactFromToField(self.contacts[1]["name"])

        #
        # Verify the contact name is not present after removal
        #
        self.messages.checkIsInToField(self.contacts[1]["name"], False)

        self.UTILS.reporting.logResult("info", "It is not the 'To' list.")
