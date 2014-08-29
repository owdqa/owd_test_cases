#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
import time
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        #
        # Create test contacts.
        #
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

        self.data_layer.connect_to_wifi()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        #
        # Launch contacts app.
        #
        self.contacts.launch()
        x = self.UTILS.element.getElement(DOM.Contacts.settings_button, "Settings button")
        x.tap()
        time.sleep(2)

        x = self.UTILS.element.getElement(DOM.Contacts.import_contacts, "Import button")
        x.tap()
        time.sleep(2)

        #
        # Press the Gmail button and go to the gmail frame.
        #
        x = self.UTILS.element.getElement(DOM.Contacts.gmail_button, "Gmail button")
        x.tap()

        self.UTILS.reporting.logResult("info", "Check that the gmail login frame is present ...")
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForElements(("xpath", "//iframe[contains(@{}, '{}')]".\
                                    format(DOM.Contacts.gmail_frame[0], DOM.Contacts.gmail_frame[1])),
                                   "Gmail login iframe")
        x = self.UTILS.element.getElement(DOM.Contacts.import_cancel_login, "Cancel button")
        x.tap()

        self.UTILS.reporting.logResult("info", "Check that the gmail login frame is no longer present ...")
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@{}, '{}')]".\
                                       format(DOM.Contacts.gmail_frame[0], DOM.Contacts.gmail_frame[1])),
                                      "Gmail login iframe")

        self.UTILS.reporting.logResult("info", "Check that the contacts app is now visible again ...")
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        self.UTILS.element.waitForElements(DOM.Contacts.import_contacts_header, "Import contacts header")

        #
        # Press the cancel icon.
        #
        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot and details", x)
