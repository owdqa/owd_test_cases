from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
import time


class test_main(PixiTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        #
        # Prepare the contact.
        #
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):

        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # View the details of our contact and make him a favourite.
        #
        self.UTILS.reporting.logResult("info", "<b>Setting up a contact in favourites ...</b>")
        self.contacts.view_contact(self.contact['name'])

        x = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (before tap)")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Contacts.details_back_button, "Back button")
        x.tap()

        self.UTILS.element.waitForElements(DOM.Contacts.favourites_section, "Favourites section")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point", x)

        self.UTILS.reporting.logResult("info", "<b>removing contact from favourites ...</b>")
        self.contacts.view_contact(self.contact['name'])

        x = self.UTILS.element.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (before tap)")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Contacts.details_back_button, "Back button")
        x.tap()

        time.sleep(1)
        self.UTILS.element.waitForNotElements(DOM.Contacts.favourites_section, "Favourites section")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot at this point", x)
