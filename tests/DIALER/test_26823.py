# 26823: Add a contact and verify that user is returned to the dialer
# ** Procedure
#       1-Open Dialer
#       2-Type a phone number
#       3-Tap in the add to contacts button
#       4-Tap in done button
# ** Expected Results
#       Contact is saved and user is redirected to the dialer again.

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.apps.contacts import Contacts


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)

        self.given_name = "John"
        self.family_name = "Doe"

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()
        self.dialer.enterNumber("123456789")
        self.dialer.createContactFromThisNum()

        contFields = self.contacts.get_contact_fields()
        self.contacts.replace_str(contFields['givenName'], self.given_name)
        self.contacts.replace_str(contFields['familyName'], self.family_name)

        done_button = self.UTILS.element.getElement(DOM.Contacts.done_button, "Done button")
        done_button.tap()
        time.sleep(2)

        self.UTILS.reporting.logResult('info', "displayed_app: {}".format(self.apps.displayed_app.name))
        self.UTILS.test.test(self.apps.displayed_app.name == "Phone", "The dialer app is now displayed.")
