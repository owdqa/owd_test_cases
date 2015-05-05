from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact
import time


class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.messages = Messages(self)

        # Get details of our test contacts.
        self.contact = MockContact(tel=[{'type': 'Mobile', 'value': '11111111'},
                                    {'type': 'Mobile', 'value': '222222222'}])
        """
        We're not testing adding a contact, so just stick one
        into the database.
        """

        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Launch contacts app.
        self.contacts.launch()

        # Select our contact.

        # View the details of our contact.
        self.contacts.view_contact(self.contact['name'])

        # Tap the 2nd sms button (index=1) in the view details screen to go to the sms page.
        smsBTN = self.UTILS.element.getElement(("id", DOM.Contacts.sms_button_specific_id.format(1)),
                                        "2nd send SMS button")
        smsBTN.tap()
        """
        Switch to the 'Messages' app frame (or marionette will still be watching the
        'Contacts' app!).
        """

        self.marionette.switch_to_frame()
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        time.sleep(3)
        """
        test: this automatically opens the 'send SMS' screen, so
        check the correct name is in the header of this sms.
        """

        self.UTILS.element.headerCheck("1 recipient")

        # Check this is the right number.
        self.messages.checkIsInToField(self.contact["name"])
        self.messages.checkNumberIsInToField(self.contact["tel"][1]["value"])
